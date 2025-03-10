from django.db import models
from questions.models import Business
from django.conf import settings
import datetime as dt
import uuid

# Existing models
class ItemList4(models.Model):
    name = models.CharField(default='Business Tax Receipt Invoice', max_length=255)
    amount = models.FloatField(default=0.0)  # Might have to be int

class V1QuickInvoicesRequest(models.Model):
    Business = models.ForeignKey(Business, on_delete=models.CASCADE)
    Email = models.EmailField(default='email@domain.com')
    created_at = models.DateTimeField(auto_now_add=True)
    title = models.CharField(max_length=64, default='BTR Invoice Title')
    due_date = models.DateField(default=dt.date(2024, 12, 31))
    item_list = models.ForeignKey(ItemList4, on_delete=models.CASCADE)
    allow_overpayment = models.BooleanField(default=False)
    bank_funded_only_override = models.BooleanField(default=True)
    allow_partial_payment = models.BooleanField(default=False)
    amount_due = models.FloatField(default=0.0)
    item_header = models.CharField(default='Item Header', max_length=255)
    item_footer = models.CharField(default='Item Footer', max_length=255)
    notification_days_before_due_date = models.IntegerField(default=3)
    notification_days_after_due_date = models.IntegerField(default=7)
    send_text_to_pay = models.BooleanField(default=True)
    Cell_Phone = models.CharField(default='123-456-7890', max_length=10)
    notification_on_due_date = models.BooleanField(default=True)

# Updated Payment model for capturing Stripe payment details via webhook
class Payment(models.Model):
    token = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    stripe_session_id = models.CharField(max_length=255, blank=True, null=True)
    customer_email = models.EmailField(blank=True, null=True)
    amount = models.IntegerField(default=0)  # store amount in cents
    created_at = models.DateTimeField(auto_now_add=True)
    # Optionally, link the payment to a specific invoice request.
    invoice = models.ForeignKey(V1QuickInvoicesRequest, on_delete=models.SET_NULL, blank=True, null=True)

    # New fields to store card details
    card_brand = models.CharField(max_length=50, blank=True, null=True)
    card_last4 = models.CharField(max_length=4, blank=True, null=True)

    def __str__(self):
        return f"Payment {self.token} - ${self.amount / 100:.2f}"
