from django.shortcuts import render
from django.views.generic.edit import FormView,CreateView,UpdateView
from django.views.generic import DetailView,ListView,TemplateView
from django.urls import reverse_lazy
from .testform import BusinessForm,BusinessEdit
from .models import Business
import pandas as pd
from django.http import HttpResponse
from openpyxl import Workbook
from django.views import View
from datetime import datetime

df = pd.read_csv('/Users/jd/Desktop/btr/questions/Pembroke Park Data w Emails.csv')

sunbiz_ids_data = df['Corporation Number']
business_names_data = df['Corporation Name']
status_data = df['Status']
filing_type_data = df['Filing Type']
unique_id_data = df['Unique ID']

sunbiz_ids = []
business_names = []
statuses = []
filing_types = []
unique_ids = []


for x in sunbiz_ids_data:
    sunbiz_ids.append(x)
for y in business_names_data:
    business_names.append(y)
for z in status_data:
    statuses.append(z)
for a in filing_type_data:
    filing_types.append(a)
for b in unique_id_data:
    unique_ids.append(b)

Business_Dict = {
    'sunbiz_id':sunbiz_ids,
    'business_names':business_names,
    'statuses':statuses,
    'filing_types':filing_types,
    'unique_ids':unique_ids
}

'''for x in range(len(Business_Dict['sunbiz_id'])):
    new_row = Business(sunbiz_id=Business_Dict['sunbiz_id'][x], business_name=Business_Dict['business_names'][x], Status=Business_Dict['statuses'][x],Unique_ID=Business_Dict['unique_ids'][x])#filing_type=Business_Dict['filing_types'][x])
    # Save the instance to the database
    new_row.save()'''


# Create your views here.

'''class BusinessForm(FormView):
    template_name = 'questions.html'
    success_url = reverse_lazy('home')
'''

'''class BusinessForm(CreateView):
    model = Business
    form_class = BusinessForm
    template_name = 'questions.html'
    success_url = reverse_lazy('results')


    def form_valid(self,form):
        business_name = form.cleaned_data['business_name']


        context = self.get_context_data(form=form)
        context['business_name'] = business_name
        context['businesses'] = Business.objects.all() 
            return self.render_to_response(context)'''

class BusinessEditView(UpdateView):
    model = Business
    template_name = 'business_edit.html'
    form_class=BusinessEdit
    success_url = reverse_lazy('business_form_input')
    context_object_name = 'business'
    def form_valid(self, form):
        response = super().form_valid(form)
        return response

class DriversLicenseListView(ListView):
    model = Business
    template_name = 'drivers_licenses.html'
    context_object_name = 'businesses'


class BusinessResults(FormView,ListView):
    model = Business
    template_name = 'questions.html'
    context_object_name = 'objects'
    form_class = BusinessForm
    success_url  = reverse_lazy('business_edit')
    object_list = Business.objects.none()

    def get_queryset(self):
        queryset = Business.objects.none()
        form = BusinessForm(self.request.GET)
        if form.is_valid():
            sunbiz_id = form.cleaned_data.get('sunbiz_id')
            unique_id = form.cleaned_data.get('Unique_ID')
            if sunbiz_id and unique_id:            
                queryset = Business.objects.filter(sunbiz_id=sunbiz_id,Unique_ID=unique_id)
        return queryset
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = BusinessForm(self.request.GET)
        

        return context



class BusinessTemplateView(TemplateView):
    template_name = 'business_template.html'

class BusinessExportView(View):

    def get(self, request, *args, **kwargs):
        response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
        response['Content-Disposition'] = 'attachment; filename="Businesses.xlsx"'

        wb = Workbook()
        ws = wb.active
        ws.title = "Businesses"

        # Add headers
        headers = ["Sunbiz ID", "Business Name", "Ownership Type","BTR","Unique_ID","Last Updated"]
        ws.append(headers)

        # Add data from the model
        for obj in Business.objects.all():
            ws.append([obj.sunbiz_id, obj.business_name, obj.Ownership_Type,obj.get_btr,obj.Unique_ID,obj.last_updated.replace(tzinfo=None)])

        wb.save(response)
        return response


'''rows = Business.objects.all()
for row in rows:
    row.delete()'''
       

# Create your views here.
