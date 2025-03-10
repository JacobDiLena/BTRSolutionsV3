from django import forms
from .models import V1QuickInvoicesRequest

class InvoiceForm(forms.ModelForm):
    class Meta:
        model = V1QuickInvoicesRequest
        fields = ['Email',
                  'Cell_Phone',
                  ]
