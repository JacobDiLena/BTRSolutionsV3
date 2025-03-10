# payment/urls.py
from django.urls import path
from .views import (
    payment_page,
    CreateCheckoutSessionView,
    payment_success,
    payment_cancel,
    download_receipt,
    stripe_webhook,
)

urlpatterns = [
    path('', payment_page, name='payment-page'),
    path('create-checkout-session/', CreateCheckoutSessionView.as_view(), name='create-checkout-session'),
    path('success/', payment_success, name='payment-success'),
    path('cancel/', payment_cancel, name='payment-cancel'),
    path('download-receipt/', download_receipt, name='download-receipt'),
    path('webhook/', stripe_webhook, name='stripe-webhook'),
]
