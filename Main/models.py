from django.db import models
from django.contrib.auth.models import User
from django.core.validators import RegexValidator
from django.core.exceptions import ValidationError

from . import fields

# Create your models here.

class InvestmentInfo(models.Model):
   user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
   monthly_income = models.DecimalField(decimal_places=2, max_digits=10)
   monthly_expenses = models.DecimalField(decimal_places=2, max_digits=10)
   date_created = models.DateTimeField(auto_now_add=True,null=True)
   savings_account_percentage = fields.IntegerRangeField(default=50, min_value=1, max_value=100)
   insurance_account_percentage = fields.IntegerRangeField(default=25, min_value=1, max_value=100)
   investment_account_percentage = fields.IntegerRangeField(default=25, min_value=1, max_value=100)

   @property
   def get_available_balance(self):
      available_balance = self.monthly_income - self.monthly_expenses
      return available_balance

   @property
   def savings_account_balance(self):
      savings_balance = (self.get_available_balance/100) * self.savings_account_percentage
      return savings_balance 

   @property
   def insurance_account_balance(self):
      insurance_balance = (self.get_available_balance/100) * self.insurance_account_percentage
      return insurance_balance

   @property
   def investment_account_balance(self):
      investment_balance = (self.get_available_balance/100) * self.insurance_account_percentage
      return investment_balance


   @property
   def get_total_amount(self):
      query_list_1 = Savings.objects.filter(user=self.user)
      query_list_2 = Insurances.objects.filter(user=self.user)
      query_list_3 = Investments.objects.filter(user=self.user)
      total_amount = 0
      for query in query_list_1:
         total_amount += query.amount
      for query in query_list_2:
         total_amount += query.amount
      for query in query_list_3:
         total_amount += query.amount
      return total_amount

   @property
   def get_total_percentage(self):
      query_list_1 = Savings.objects.filter(user=self.user)
      query_list_2 = Insurances.objects.filter(user=self.user)
      query_list_3 = Investments.objects.filter(user=self.user)
      total_percentage = 0
      for query in query_list_1:
         total_percentage += query.percentage
      for query in query_list_2:
         total_percentage += query.percentage
      for query in query_list_3:
         total_percentage += query.percentage
      return total_percentage

     

   def __str__(self):
      return self.user.username + " Investment Info "



class Savings(models.Model):
   INVESTMENT_MARKETS = (
      ('Family Support', 'Family Support'),
      ('Major Purchases', 'Major Purchases'),
      ('Vacation', 'Vacation'),
      ('Repairs', 'Repairs')
   )
   user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
   investmentInfo = models.ForeignKey(InvestmentInfo, on_delete=models.CASCADE, null=True)
   name = models.CharField(default="Savings",editable=False, max_length=50 )
   created_at = models.DateTimeField(auto_now_add=True, null=True)
   investmentMarkets = models.CharField(max_length=50, choices=INVESTMENT_MARKETS)
   amount = models.DecimalField(decimal_places=2, max_digits=10)
   percentage = fields.IntegerRangeField(min_value=1, max_value=100, null=True)
  
   @property
   def get_savings_percentage(self):
      percentage = InvestmentInfo.objects.filter(user=self.user)[0].savings_account_percentage
      return percentage

   class Meta:
      verbose_name = 'Saving'
      verbose_name_plural = 'Savings'

   def __str__(self):
      return self.user.username + " Savings "

 
   

class Insurances(models.Model):
   INVESTMENT_MARKETS = (
      ('Whole Life', 'Whole Life'),
      ('LTCA rider', 'LTCA rider'),
      ('SWL', 'SWL'),
   )
   user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
   investmentInfo = models.ForeignKey(InvestmentInfo, on_delete=models.CASCADE, null=True)
   name = models.CharField(default="Insurance",editable=False, max_length=50 )
   created_at = models.DateTimeField(auto_now_add=True, null=True)
   investmentMarkets = models.CharField(max_length=50, choices=INVESTMENT_MARKETS)
   amount = models.DecimalField(decimal_places=2, max_digits=10)
   percentage = fields.IntegerRangeField(min_value=1, max_value=100, null=True)  

   class Meta:
      verbose_name = 'Insurance'
      verbose_name_plural = 'Insurances'

   def __str__(self):
      return self.user.username + " Insurances "




class Investments(models.Model):
   INVESTMENT_MARKETS = (
      ('Mutual Funds', 'Mutual Funds'),
      ('Stocks', 'Stocks'),
      ('Bonds', 'Bonds'),
      ('ETFs', 'ETFs')
   )
   user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
   investmentInfo = models.ForeignKey(InvestmentInfo, on_delete=models.CASCADE, null=True)
   name = models.CharField(default="Investment",editable=False, max_length=50 )
   created_at = models.DateTimeField(auto_now_add=True, null=True)
   investmentMarkets = models.CharField(max_length=50, choices=INVESTMENT_MARKETS)
   amount = models.DecimalField(decimal_places=2, max_digits=10)
   percentage = fields.IntegerRangeField(min_value=1, max_value=100, null=True)

   class Meta:
      verbose_name = 'Investment'
      verbose_name_plural = 'Investments'

   def __str__(self):
      return self.user.username + " Investments "
