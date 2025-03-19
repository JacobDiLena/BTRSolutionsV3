import stripe
from io import BytesIO
from django.conf import settings
from django.shortcuts import redirect, render
from django.views import View
from django.http import HttpResponse
import logging
from django.views.decorators.csrf import csrf_exempt
from .models import Payment  # Import your custom Payment model

logger = logging.getLogger(__name__)
stripe.api_key = settings.STRIPE_SECRET_KEY

class CreateCheckoutSessionView(View):
    def post(self, request, *args, **kwargs):
        total_amount = 1000  # $10.00 in cents

        # If the user is authenticated, create a Stripe customer using their email and name.
        if request.user.is_authenticated:
            email = request.user.email
            name = request.user.get_full_name() or request.user.username
            try:
                stripe_customer = stripe.Customer.create(
                    email=email,
                    name=name,
                )
                customer_id = stripe_customer.id
            except Exception as e:
                logger.error("Error creating Stripe customer: %s", e)
                customer_id = None
        else:
            customer_id = None

        # Create an initial Payment record with a custom token.
        payment = Payment.objects.create(
            customer_email=request.user.email if request.user.is_authenticated else "guest@example.com",
            amount=total_amount,
        )

        # Prepare the checkout session data.
        session_data = {
            'payment_method_types': ['card'],
            'line_items': [{
                'price_data': {
                    'currency': 'usd',
                    'unit_amount': total_amount,
                    'product_data': {'name': 'Total Balance Payment'},
                },
                'quantity': 1,
            }],
            'mode': 'payment',
            'success_url': request.build_absolute_uri(f'/payment/success/?token={payment.token}'),
            'cancel_url': request.build_absolute_uri('/payment/cancel/'),
        }
        # If a customer was created, pass the customer ID; otherwise use the email fallback.
        if customer_id:
            session_data['customer'] = customer_id
        else:
            session_data['customer_email'] = request.user.email if request.user.is_authenticated else "guest@example.com"

        checkout_session = stripe.checkout.Session.create(**session_data)

        # Save the Stripe session ID in our Payment record.
        payment.stripe_session_id = checkout_session.id
        payment.save()

        logger.debug("Created checkout session: %s", checkout_session)
        return redirect(checkout_session.url)

def payment_success(request):
    token = request.GET.get('token')
    logger.debug("Payment success view called with token: %s", token)
    try:
        payment = Payment.objects.get(token=token)
        logger.debug("Retrieved Payment record: %s", payment)
    except Payment.DoesNotExist:
        logger.error("Payment record not found for token: %s", token)
        payment = None

    context = {'payment': payment}
    return render(request, 'payment/success.html', context)

def download_receipt(request):
    token = request.GET.get('token')
    if not token:
        return HttpResponse("Missing payment token.", status=400)
    try:
        payment = Payment.objects.get(token=token)
    except Payment.DoesNotExist:
        return HttpResponse("Payment not found.", status=404)
    
    customer_email = payment.customer_email if payment.customer_email else 'customer@example.com'
    amount_dollars = payment.amount / 100

    # Generate a simple PDF receipt using ReportLab.
    from reportlab.pdfgen import canvas
    buffer = BytesIO()
    p = canvas.Canvas(buffer)
    p.setFont("Helvetica", 16)
    p.drawString(100, 800, "Payment Receipt")
    p.setFont("Helvetica", 12)
    p.drawString(100, 770, f"Customer Email: {customer_email}")
    p.drawString(100, 750, f"Amount Paid: ${amount_dollars:.2f}")
    p.drawString(100, 730, "Thank you for your payment!")
    p.showPage()
    p.save()
    
    buffer.seek(0)
    response = HttpResponse(buffer, content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="receipt.pdf"'
    return response

def payment_cancel(request):
    return render(request, 'payment/cancel.html')

def payment_page(request):
    return render(request, 'payment/payment.html')

@csrf_exempt
def stripe_webhook(request):
    payload = request.body
    sig_header = request.META.get('HTTP_STRIPE_SIGNATURE')
    webhook_secret = settings.STRIPE_WEBHOOK_SECRET
    event = None

    try:
        event = stripe.Webhook.construct_event(payload, sig_header, webhook_secret)
    except ValueError as e:
        logger.error("Invalid payload: %s", e)
        return HttpResponse(status=400)
    except stripe.error.SignatureVerificationError as e:
        logger.error("Invalid signature: %s", e)
        return HttpResponse(status=400)

    if event.get('type') == 'checkout.session.completed':
        session = event['data']['object']
        try:
            payment = Payment.objects.get(stripe_session_id=session['id'])
        except Payment.DoesNotExist:
            logger.error("Payment record not found for session id: %s", session['id'])
            return HttpResponse(status=200)

        # Update the Payment record with the customer's email.
        payment.customer_email = session['customer_details'].get('email', 'not provided')
        
        # Retrieve PaymentIntent details to get card info.
        payment_intent_id = session.get('payment_intent')
        if payment_intent_id:
            try:
                pi = stripe.PaymentIntent.retrieve(payment_intent_id)
                if pi.charges and pi.charges.data:
                    charge = pi.charges.data[0]
                    card_info = charge.payment_method_details.get('card', {})
                    payment.card_brand = card_info.get('brand')
                    payment.card_last4 = card_info.get('last4')
            except Exception as e:
                logger.error("Error retrieving PaymentIntent %s: %s", payment_intent_id, e)
        
        payment.save()
        logger.debug("Webhook updated Payment: email=%s, card_brand=%s, card_last4=%s",
                     payment.customer_email, payment.card_brand, payment.card_last4)

    return HttpResponse(status=200)
