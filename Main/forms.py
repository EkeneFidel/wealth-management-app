from django.contrib.auth.models import User
from django import forms
from django.forms import fields
from .models import InvestmentInfo, Savings, Insurances, Investments





class UserForm(forms.ModelForm):
   username = forms.CharField(max_length=100)
   email = forms.EmailField()
   password = forms.CharField(widget=forms.PasswordInput)
   confirm_password = forms.CharField(widget=forms.PasswordInput)
   
   class Meta:
      model = User
      fields = ['username','first_name','last_name', 'email', 'password']

   def clean(self):
      cleaned_data = super(UserForm, self).clean()
      password = cleaned_data.get("password")
      confirm_password = cleaned_data.get("confirm_password")

      if password != confirm_password:
         raise forms.ValidationError(
               "passwords do not match"
         )

   
class InvestmentForm(forms.ModelForm):

   class Meta:
      model = InvestmentInfo
      fields = ('monthly_income', 'monthly_expenses')

   def __init__(self, *args, **kwargs):
        super(InvestmentForm, self).__init__(*args, **kwargs)
        self.fields['monthly_expenses'].label = "Estimated monthly expenses"


class EditInvestmentForm(forms.ModelForm):

   class Meta:
      model = InvestmentInfo
      fields = ('monthly_income', 'monthly_expenses', 'savings_account_percentage', 'insurance_account_percentage', 'investment_account_percentage')

   def __init__(self, *args, **kwargs):
        super(EditInvestmentForm, self).__init__(*args, **kwargs)
        self.fields['monthly_expenses'].label = "Estimated monthly expenses"


class ShowSavingForm(forms.ModelForm):
   class Meta:
      model = Savings
      fields = ('amount',)

      
class ShowInsuranceForm(forms.ModelForm):
   class Meta:
      model = Insurances
      fields = ('amount',)


class ShowInvestmentForm(forms.ModelForm):
   class Meta:
      model = Investments
      fields = ('amount',)



