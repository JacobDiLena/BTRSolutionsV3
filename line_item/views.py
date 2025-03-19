from django.shortcuts import render
from django.views.generic import ListView,DetailView,CreateView,TemplateView
from django.views.generic.edit import UpdateView,DeleteView
from django.urls import reverse_lazy
from .models import Income,FixedExpense,VariableExpense,Spending,Assets,Liabilities
from django.contrib.auth.mixins import LoginRequiredMixin,UserPassesTestMixin
from django.db.models import Sum
from django import forms
# Create your views here.



class NetWorthCalculatorView(LoginRequiredMixin,TemplateView):
    template_name = 'networth_calculator.html'
    
    def get_context_data(self,**kwargs):
        context = super().get_context_data(**kwargs)
        context['assets'] = Assets.objects.all()
        context['total_assets'] = Assets.objects.aggregate(total=Sum('amount'))['total'] or 0
        context['total_liabilities'] = Liabilities.objects.aggregate(total=Sum('amount'))['total'] or 0
        context['liabilities'] = Liabilities.objects.all()
        context['networth'] = context['total_assets'] - context['total_liabilities']
        return context




class LiabilitiesDetailView(LoginRequiredMixin,DetailView):
    model = Liabilities
    template_name = 'liabilities_detail.html'




class LiabilitiesDeleteView(LoginRequiredMixin,DeleteView):
    model = Liabilities
    template_name = 'liabilities_delete.html'
    success_url = reverse_lazy('liabilities_list')




class LiabilitiesUpdateView(LoginRequiredMixin,UpdateView):
    model = Liabilities
    template_name = 'liabilities_edit.html'
    success_url = reverse_lazy('liabilities_list')
    fields = ('title','amount',)






class LiabilitiesCreateView(LoginRequiredMixin,CreateView):
    model = Liabilities
    template_name = 'liabilities_new.html'
    fields = ('title','amount',)
    success_url = reverse_lazy('liabilities_list')




class LiabilitiesListView(LoginRequiredMixin,ListView):
    model = Liabilities
    template_name = 'liabilities_list.html'

    def get_context_data(self,**kwargs):
        context = super().get_context_data(**kwargs)
        context['liabilities'] = Liabilities.objects.all()
        context['total_liabilities'] = Liabilities.objects.aggregate(total=Sum('amount'))['total'] or 0
        return context




class AssetsDetailView(LoginRequiredMixin,DetailView):
    model = Assets
    template_name = 'assets_detail.html'



class AssetsDeleteView(LoginRequiredMixin,DeleteView):
    model = Assets
    template_name = 'assets_delete.html'
    success_url = reverse_lazy('assets_list')




class AssetsUpdateView(LoginRequiredMixin,UpdateView):
    model = Assets
    template_name = 'assets_new.html'
    fields = ('title','asset_type','amount',)
    success_url = reverse_lazy('assets_list')


class AssetsCreateView(LoginRequiredMixin,CreateView):
    model = Assets
    template_name = 'assets_new.html'
    fields = ('title','asset_type','amount',)
    success_url = reverse_lazy('assets_list')



class AssetsListView(LoginRequiredMixin,ListView):
    model = Assets
    template_name = 'assets_list.html'

    def get_context_data(self,**kwargs):
        context = super().get_context_data(**kwargs)
        context['assets'] = Assets.objects.all()
        context['total_assets'] = Assets.objects.aggregate(total=Sum('amount'))['total'] or 0
        return context
        

class SnapshotView(LoginRequiredMixin,TemplateView):
    template_name = 'snapshot.html'
    '''def get_queryset(self):
        return Income.objects.filter(user=self.request.user)'''


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['incomes'] = Income.objects.all()
        context['variable_expenses'] = VariableExpense.objects.all()
        context['total_variable_expenses'] = VariableExpense.objects.aggregate(total=Sum('starting_amount'))['total'] or 0
        context['fixed_expenses'] = FixedExpense.objects.all()
        context['total_income'] = Income.objects.aggregate(total=Sum('amount'))['total'] or 0
        context['total_fixed_expenses_sum']= FixedExpense.objects.aggregate(total=Sum('amount'))['total'] or 0
        variable_expenses_summary = []
        variable_expenses = VariableExpense.objects.all()
        for expenses in variable_expenses:
            total_spent = Spending.objects.filter(associated_variable_expense = expenses).aggregate(total=Sum('amount'))['total'] or 0
            remaining_amount = expenses.starting_amount - total_spent
            variable_expenses_summary.append({
            'title':expenses.title,
            'starting_amount' : expenses.starting_amount,
            'total_spent' : total_spent,
            'remaining_amount' : remaining_amount,
            'pk':expenses.pk
            
        })

        context['variable_expenses_summary'] = variable_expenses_summary
        total_remaining_amount = 0
        total_starting_amount = 0
        for expenses in variable_expenses_summary:
            total_remaining_amount += expenses['remaining_amount']
            total_starting_amount += expenses['starting_amount']
        context['total_variable_expenses_sum'] = total_remaining_amount
        context['total_variable_starting_amount_sum'] = total_starting_amount
        context['ending_savings'] = context['total_income'] - context['total_fixed_expenses_sum'] - context['total_variable_expenses_sum']

        return context






# Income
class IncomeListView(LoginRequiredMixin,ListView):
    model = Income
    template_name = 'income_list.html'
    '''def get_queryset(self):
        return Income.objects.filter(user=self.request.user)'''
    def get_context_data(self,**kwargs):
        context = super().get_context_data(**kwargs)
        context['total_income'] = Income.objects.aggregate(total=Sum('amount'))['total'] or 0
        context['incomes'] = Income.objects.all()

        return context







class IncomeDetailView(LoginRequiredMixin,DetailView):
    model = Income
    template_name = 'income_detail.html'
    '''def get_queryset(self):
        return Income.objects.filter(user=self.request.user)'''

    



class IncomeUpdateView(LoginRequiredMixin,UpdateView):
    model = Income
    fields = ('title','amount','pay_date','paid')
    template_name = 'income_edit.html'
    success_url = reverse_lazy('income_list')
    '''def get_queryset(self):
        return Income.objects.filter(user=self.request.user)'''

    '''def test_func(self):
        obj = self.get_object()
        return obj.author == self.request.user'''




class IncomeDeleteView(LoginRequiredMixin,DeleteView):
    model = Income
    template_name = 'income_delete.html'
    success_url = reverse_lazy('income_list')
    '''def get_queryset(self):
        return Income.objects.filter(user=self.request.user)'''
    
    '''def test_func(self):
        obj = self.get_object()
        return obj.author == self.request.user'''


class IncomeCreateView(LoginRequiredMixin,CreateView):
    model = Income
    template_name = 'income_new.html'
    fields = ('title','amount','pay_date','paid')
    success_url = reverse_lazy('income_list')
    '''def get_queryset(self):
        return Income.objects.filter(user=self.request.user)'''

    '''def form_valid(self,form):
        form.instance.author = self.request.user
        return super().form_valid(form)'''
    

    



# Fixed Expenses
    


    

class FixedExpensesListView(LoginRequiredMixin,ListView):
    model = FixedExpense
    template_name = 'fixed_expenses_list.html'
    '''def get_queryset(self):
        return FixedExpense.objects.filter(user=self.request.user)'''

    def get_context_data(self,**kwargs):
        context = super().get_context_data(**kwargs)
        context['total_fixed_expenses_sum']= FixedExpense.objects.aggregate(total=Sum('amount'))['total'] or 0
        context['paid_fixed_expenses_sum'] = FixedExpense.objects.filter(paid=True).aggregate(total=Sum('amount'))['total'] or 0
        context['unpaid_fixed_expenses_sum'] = FixedExpense.objects.filter(paid=False).aggregate(total=Sum('amount'))['total'] or 0
        context['fixed_expenses'] = FixedExpense.objects.all()

        return context







class FixedExpensesDetailView(LoginRequiredMixin,DetailView):
    model = FixedExpense
    template_name = 'fixed_expenses_detail.html'
    '''def get_queryset(self):
        return FixedExpense.objects.filter(user=self.request.user)'''



class FixedExpensesUpdateView(LoginRequiredMixin,UpdateView):
    model = FixedExpense
    fields = ('title','amount','date','paid')
    template_name = 'fixed_expenses_edit.html'
    success_url = reverse_lazy('fixed_expenses_list')
    '''def get_queryset(self):
        return FixedExpense.objects.filter(user=self.request.user)'''

    '''def test_func(self):
        obj = self.get_object()
        return obj.author == self.request.user'''




class FixedExpensesDeleteView(LoginRequiredMixin,DeleteView):
    model = FixedExpense
    template_name = 'fixed_expenses_delete.html'
    success_url = reverse_lazy('fixed_expenses_list')
    '''def get_queryset(self):
        return FixedExpense.objects.filter(user=self.request.user)'''
    '''def test_func(self):
        obj = self.get_object()
        return obj.author == self.request.user'''


class FixedExpensesCreateView(LoginRequiredMixin,CreateView):
    model = FixedExpense
    template_name = 'fixed_expenses_new.html'
    fields = ('title','amount','date','paid')
    success_url = reverse_lazy('fixed_expenses_list')
    '''def get_queryset(self):
        return FixedExpense.objects.filter(user=self.request.user)'''

    '''def form_valid(self,form):
        form.instance.author = self.request.user
        return super().form_valid(form)'''


# Variable Expenses
class VariableExpensesListView(LoginRequiredMixin,ListView):
    model = VariableExpense
    template_name = 'variable_expenses_list.html'
    '''def get_queryset(self):
        return VariableExpense.objects.filter(user=self.request.user)'''

    def get_context_data(self,**kwargs):
        context = super().get_context_data(**kwargs)

        variable_expenses_summary = []
        variable_expenses=VariableExpense.objects.all()
        for expenses in variable_expenses:
            total_spent = Spending.objects.filter(associated_variable_expense = expenses).aggregate(total=Sum('amount'))['total'] or 0
            remaining_amount = expenses.starting_amount - total_spent
            variable_expenses_summary.append({
            'title':expenses.title,
            'starting_amount' : expenses.starting_amount,
            'total_spent' : total_spent,
            'remaining_amount' : remaining_amount,
            'pk':expenses.pk
            
        })

        context['variable_expenses_summary'] = variable_expenses_summary
        total_remaining_amount = 0
        total_starting_amount = 0
        for expenses in variable_expenses_summary:
            total_remaining_amount += expenses['remaining_amount']
            total_starting_amount += expenses['starting_amount']
        context['total_variable_expenses_sum'] = total_remaining_amount
        context['total_variable_starting_amount_sum'] = total_starting_amount
        
  

        return context
    
   







class VariableExpensesDetailView(LoginRequiredMixin,DetailView):
    model = VariableExpense
    template_name = 'variable_expenses_detail.html'
    fields = ('title','starting_amount','amount_left',)
    '''def get_queryset(self):
        return VariableExpense.objects.filter(user=self.request.user)'''
    



class VariableExpensesUpdateView(LoginRequiredMixin,UpdateView):
    model = VariableExpense
    fields = ('title','starting_amount',)
    template_name = 'variable_expenses_edit.html'
    success_url = reverse_lazy('variable_expenses_list')
    '''def get_queryset(self):
        return VariableExpense.objects.filter(user=self.request.user)'''
    '''def test_func(self):
        obj = self.get_object()
        return obj.author == self.request.user'''




class VariableExpensesDeleteView(LoginRequiredMixin,DeleteView):
    model = VariableExpense
    template_name = 'variable_expenses_delete.html'
    success_url = reverse_lazy('variable_expenses_list')
    '''def get_queryset(self):
        return VariableExpense.objects.filter(user=self.request.user)'''
    '''def test_func(self):
        obj = self.get_object()
        return obj.author == self.request.user'''


class VariableExpensesCreateView(LoginRequiredMixin,CreateView):
    model = VariableExpense
    template_name = 'variable_expenses_new.html'
    fields = ('title','starting_amount',)
    success_url = reverse_lazy('variable_expenses_list')
    '''def get_queryset(self):
        return VariableExpense.objects.filter(user=self.request.user)'''

    '''def form_valid(self,form):
        form.instance.author = self.request.user
        return super().form_valid(form)'''
    

# Spending
    
class SpendingListView(LoginRequiredMixin,ListView):
    model = Spending
    template_name = 'spending_list.html'
    '''def get_queryset(self):
        return Spending.objects.filter(user=self.request.user)'''

    def get_context_data(self,**kwargs):
        context = super().get_context_data(**kwargs)
        context['spendings'] = Spending.objects.all()
        context['total_spending_sum']= Spending.objects.aggregate(total=Sum('amount'))['total'] or 0

        return context






class SpendingDetailView(LoginRequiredMixin,DetailView):
    model = Spending
    template_name = 'spending_detail.html'
    '''def get_queryset(self):
        return Spending.objects.filter(user=self.request.user)'''
    
    



class SpendingUpdateView(LoginRequiredMixin,UpdateView):
    model = Spending
    fields = ('associated_variable_expense','amount',)
    template_name = 'spending_edit.html'
    success_url = reverse_lazy('spending_list')
    '''def get_queryset(self):
        return Spending.objects.filter(user=self.request.user)'''

    '''def test_func(self):
        obj = self.get_object()
        return obj.author == self.request.user'''




class SpendingDeleteView(LoginRequiredMixin,DeleteView):
    model = Spending
    template_name = 'spending_delete.html'
    success_url = reverse_lazy('spending_list')
    '''def get_queryset(self):
        return Spending.objects.filter(user=self.request.user)'''
    '''def test_func(self):
        obj = self.get_object()
        return obj.author == self.request.user'''


class SpendingCreateView(LoginRequiredMixin,CreateView):
    model = Spending
    template_name = 'spending_new.html'
    fields = ('associated_variable_expense','amount',)
    success_url = reverse_lazy('spending_list')
    
    '''def get_form(self, form_class=None):
        form = super().get_form(form_class)
        form.fields['associated_variable_expense'].queryset = VariableExpense.objects.filter(user=self.request.user)
        return form

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)'''
    

    '''def get_queryset(self):
        return Spending.objects.filter(user=self.request.user)'''

    '''def form_valid(self,form):
        form.instance.author = self.request.user
        return super().form_valid(form)'''

