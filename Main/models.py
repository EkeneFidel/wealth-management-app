from django.db import models
from django.contrib.auth.models import User
from django.core.validators import RegexValidator
from django.core.exceptions import ValidationError


# Create your models here.
def valid_pct(value):
   if value.endswith("%"):
      return float(value[:-1])/100
   else:
      try:
         return float(value)
      except ValueError:          
         raise ValidationError(
            ('%(value)s is not a valid pct'),
               params={'value': value},
         )

class InvestmentInfo(models.Model):
   user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
   monthly_income = models.FloatField()
   monthly_expenses = models.FloatField()
   date_created = models.DateTimeField(auto_now_add=True,null=True)
   savings_account_percentage = models.CharField(default=50, max_length=100, validators=[valid_pct])
   insurance_account_percentage = models.CharField(default=25, max_length=100, validators=[valid_pct])
   investment_account_percentage = models.CharField(default=25, max_length=100, validators=[valid_pct])

   @property
   def get_available_balance(self):
      available_balance = self.monthly_income - self.monthly_expenses
      return available_balance

   def savings_account_balance(self):
      return self.get_available_balance() * self.savings_account_percentage

   def insurance_account_balance(self):
      return self.get_available_balance() * self.insurance_account_percentage

   def investment_account_balance(self):
      return self.get_available_balance() * self.insurance_account_percentage

   def __str__(self):
      return self.user.username + " Investment Info " + str(self.pk)


