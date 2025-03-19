from django.db import models
from django.conf import settings
from django.contrib.auth import get_user_model
from django.conf import settings
from django.urls import reverse
# Create your models here.

class Liabilities(models.Model):
    title = models.CharField(max_length = 255)
    amount = models.FloatField()
    date = models.DateField(auto_now_add = True)




class Assets(models.Model):

    ASSET_TYPE_CHOICES = [
        ('Cash', 'Cash'),
        ('Real Estate', 'Real Estate'),
        ('Property', 'Property'),
        ('Retirement Account','Retirement Account'),

    ]
    title = models.CharField(max_length=255)
    user = models.ForeignKey(settings.AUTH_USER_MODEL,null=True,on_delete=models.CASCADE)
    asset_type = models.CharField(
        choices=ASSET_TYPE_CHOICES,
        max_length = 255
    )
    amount = models.FloatField()
    date = models.DateField(auto_now_add = True)

    def __str__(self):
        return self.title
    
class Income(models.Model):
    title = models.CharField(max_length=255)
    user = models.ForeignKey(settings.AUTH_USER_MODEL,null=True,on_delete=models.CASCADE)

    amount = models.FloatField()
    
    pay_date = models.DateField(blank=True,null=True,)
    
    

    paid = models.BooleanField(null=False,blank=False,default=False)
    '''author = models.ForeignKey(
        get_user_model(),
        on_delete=models.CASCADE,
        
    )'''
    def __str__(self):
        return self.title
    
    def get_absolute_url(self):
        return reverse('income_detail')

class FixedExpense(models.Model):
    title = models.CharField(max_length=255)
    user = models.ForeignKey(settings.AUTH_USER_MODEL,null=True,on_delete=models.CASCADE)

    amount = models.FloatField()
    date = models.DateField(blank=True,null=True)

    
    

    paid = models.BooleanField(null=False,blank=False,default=False)

    def __str__(self):
        return self.title
    
    def get_absolute_url(self):
        return reverse('fixed_expenses_detail')   


class VariableExpense(models.Model):
    title = models.CharField(max_length=255)
    user = models.ForeignKey(settings.AUTH_USER_MODEL,null=True,on_delete=models.CASCADE)

    starting_amount = models.FloatField()

    
    

    
    def __str__(self):
        return self.title
    
    def get_absolute_url(self):
        return reverse('variable_expenses_detail')
    

class Spending(models.Model):
    associated_variable_expense = models.ForeignKey(
        VariableExpense,
        on_delete = models.CASCADE,
        
    )
    amount = models.FloatField()

    date = models.DateField(auto_now_add = True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL,null=True,on_delete=models.CASCADE)



    def __str__(self):
        return self.associated_variable_expense
    
    def get_absolute_url(self):
        return reverse('spending_detail')

    

 






