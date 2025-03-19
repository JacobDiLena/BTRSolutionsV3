from django.db import models
from django.urls import reverse

# Create your models here.
class Business(models.Model):
    sunbiz_id = models.CharField(max_length = 255)
    business_name = models.CharField(max_length=255)
    Unique_ID = models.CharField(max_length=255,default='0')
    email = models.EmailField(default=' ')
    last_updated = models.DateTimeField(auto_now=True)
    drivers_license = models.FileField(upload_to='drivers-licenses/',null=True,blank=True)
    OWNERSHIP_TYPE_CHOICES = [
        ('Individual','Individual'),
        ('Partnership','Partnership'),
        ('Corporation','Corporation'),
        ('Other','Other')
    ]
    BUSINESS_INDUSTRY_CHOICES = [
        ('Energy','Energy'),
        ('Construction','Construction'),
        ('Hospitality','Hospitality'),
        ('Information','Information'),
        ('Manufacturing','Manufacturing'),
        ('Education','Education'),
        ('Entertainment','Entertainment'),
        ('Finance','Finance'),
        ('Insurance','Insurance'),
        ('Transportation','Transportation'),
        ('Law','Law'),
        ('Other','Other'),
    ]

    CORP_TYPE = [
        ('S-Corp','S-Corp'),
        ('C-Corp','C-Corp'),
        ('N/A','N/A')
    ]

    WHOLESALE_RETAIL_CHOICES = [
        ('Wholesale','Wholesale'),
        ('Retail','Retail'),
        ('N/A','N/A'),
    ]
    Ownership_Type = models.CharField(choices=OWNERSHIP_TYPE_CHOICES,max_length=255,default='Other')
    Number_of_Pumps = models.PositiveIntegerField(default=0)
    Number_of_Seats = models.PositiveIntegerField(default=0)
    Number_of_Trucks = models.PositiveIntegerField(default=0)
    Number_of_Employees = models.PositiveIntegerField(default=0)
    Business_Industry = models.CharField(choices=BUSINESS_INDUSTRY_CHOICES,max_length=255,default='Other')
    Corporation_Type = models.CharField(choices=CORP_TYPE,max_length=255,default='N/A')
    Squarefootage_of_Workspace = models.PositiveIntegerField(default=0)
    Wholesale_or_Retail = models.CharField(choices=WHOLESALE_RETAIL_CHOICES,max_length=255,default='N/A')
    Average_Inventory_Value = models.FloatField(default=0)
    Status = models.CharField(default='A',max_length=255)

    #last_updated = models.DateTimeField(auto_now=True)
    def __str__(self):
        return self.sunbiz_id
    
    @property
    def get_btr(self):
        pumps = self.Number_of_Pumps*10
        seats = self.Number_of_Seats*0.45
        trucks = self.Number_of_Trucks*100
        employees = self.Number_of_Employees*0.10
        if self.Business_Industry == 'Transportation':
            industry = 30
        else:
            industry = 15
        if self.Corporation_Type == 'S-Corp':
            corp = 15
        elif self.Corporation_Type == 'C-Corp':
            corp = 20
        else:
            corp = 0
        if self.Squarefootage_of_Workspace <=800:
            sqft_tax = 45
        elif self.Squarefootage_of_Workspace > 800 and self.Squarefootage_of_Workspace <= 1999:
            sqft_tax = 75
        elif self.Squarefootage_of_Workspace >= 2000:
            sqft_tax = self.sqft * 0.05
        
        total_btr = pumps+seats+trucks+employees+industry+corp+sqft_tax

        return total_btr
        

        

