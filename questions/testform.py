from django import forms
from .models import Business

class BusinessForm(forms.ModelForm):
    class Meta:
        model = Business
        fields = ['sunbiz_id','Unique_ID']

class BusinessEdit(forms.ModelForm):
    class Meta:
        model = Business
        fields = ['email',
                  'Ownership_Type',
                  'Number_of_Pumps',
                  'Number_of_Seats',
                  'Number_of_Trucks',
                  'Number_of_Employees',
                  'Business_Industry',
                  'Corporation_Type',
                  'Squarefootage_of_Workspace',
                  'Wholesale_or_Retail',
                  'Average_Inventory_Value',
                  'drivers_license'

                  
                  ]
        widgets = {
            'drivers_license': forms.ClearableFileInput(attrs={'multiple': False}),
        }
