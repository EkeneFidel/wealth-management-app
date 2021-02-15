from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.template import context, loader, RequestContext
from django.urls import reverse
from django.core.exceptions import ObjectDoesNotExist
import math



from .forms import UserForm, InvestmentForm, ShowInvestmentForm, ShowSavingForm, ShowInsuranceForm
from .models import InvestmentInfo, Savings, Insurances, Investments


# Create your views here.
def indexView(request):
   return render(request, 'Main/index.html', {})

   
def registerView(request):
   if request.method == 'POST':
      form = UserForm(request.POST)
      if form.is_valid():
         user = form.save(commit=False)
         username = form.cleaned_data['username']
         password = form.cleaned_data['password']
         user.set_password(password)
         user.save()
         messages.info(request, "Thanks for registering. You are now logged in.")
         login(request, user)
         return redirect(('/dashboard/'+ username + '/'))
   else:
      form = UserForm()
   return render(request, 'Main/register.html', {'form':form})



def loginView(request):
   if request.method == 'POST':
         username = request.POST.get('username')
         password = request.POST.get('password')
         user = authenticate(username=username, password=password)
         if user:
               if user.is_active:
                  login(request,user)
                  return redirect('/dashboard/'+ username + '/')
                  # return render(request,'Main/dashboard.html')
               else:
                  messages.error(request, 'Your account has been disabled')
                  return render(request,'Main/login.html')
         else:
               messages.error(request, 'Invalid login')
               return render(request,'Main/login.html')
   else:
      return render(request, 'Main/login.html', {})


#---------------------------------------- DASHBOARD VIEW -------------------------------------------------- 

@login_required
def dashboardView(request):
   
   try:
      investments = InvestmentInfo.objects.get(user=request.user)
   except ObjectDoesNotExist as e:
      investments = InvestmentInfo.objects.filter(user=request.user)
   savings = Savings.objects.filter(user=request.user)
   invest = Investments.objects.filter(user=request.user)
   insurance = Insurances.objects.filter(user=request.user)

   
   context = {
      'investments': investments,
      'savings': savings,
      'invest': invest,
      'insurance': insurance  
      
   }
   return render(request, 'Main/dashboard.html', context)


@login_required
def logoutView(request):
   logout(request)
   return redirect('/')


@login_required
def createInvestmetView(request):
   if request.method == 'GET':
      form = InvestmentForm()
      return render(request, "Main/create_investment.html", {'form':form})
   else:
      username = request.POST.get('username')
      form = InvestmentForm(request.POST)
      if form.is_valid():
         investment = form.save(commit=False)
         investment.user = request.user
         investment.save()
         form.save_m2m()
      return redirect(('/dashboard/'+ request.user.username + '/'))



# -----------------------------------ADD SAVINGS VIEW--------------------------------------------


@login_required
def addSavingsView(request):
   investmentinfo = InvestmentInfo.objects.get(user=request.user)
   investinfo = InvestmentInfo.objects.select_related('user').get(user=request.user)

   savings = Savings.objects.filter(user=request.user)
   choices_savings = Savings._meta.get_field('investmentMarkets').choices

   if request.method == 'GET': 

      form1 = ShowSavingForm()
      context = {'form1':form1,
               'savings':savings,
               'choices':choices_savings}
         
      return render(request, "Main/add_savings.html", context)
   else:
      form1 = ShowSavingForm(request.POST)
      context = {'form1':form1,
               'savings':savings,
               'choices':choices_savings}

      amount = request.POST['amount']
      total_savings = 0
      for saving in savings:
         total_savings += saving.amount
      total_savings = float(total_savings)
      total_savings += float(amount)
      print(total_savings, investmentinfo.savings_account_balance, amount)
      if total_savings > investmentinfo.savings_account_balance:
         messages.error(request, "Amount exceeds current balance for investments")
         return render(request,  "Main/add_savings.html", context) 


      percentage = math.ceil((float(amount)/float(investmentinfo.savings_account_balance))*100.00)
      total_percentage = 0
      for saving in savings:
         total_percentage += saving.percentage
      total_percentage = float(total_percentage)
      total_percentage += percentage
      print(total_percentage, investmentinfo.savings_account_percentage, percentage)
      if total_percentage > investmentinfo.savings_account_percentage:
         messages.error(request, "Percentage exceeds remaining percentage for investments")
         return render(request,  "Main/add_savings.html", context) 


      username = request.user.username
      if form1.is_valid():
         saving = form1.save(commit=False)
         saving.user = request.user
         saving.save()
         savings = Savings.objects.filter(user=request.user)
         percentage = math.ceil((float(amount)/float(investmentinfo.savings_account_balance))*100.00)
         for object in savings:
            object.investmentInfo = investinfo 
            object.percentage = percentage 
            object.save()
         
         
      return redirect(('/dashboard/'+ username + '/'))



# -----------------------------------ADD INVESTMENT VIEW--------------------------------------------


@login_required
def addInvestmentView(request):
   investmentinfo = InvestmentInfo.objects.get(user=request.user)
   investinfo = InvestmentInfo.objects.select_related('user').get(user=request.user)

   investments = Investments.objects.filter(user=request.user)
   choices_investments = Investments._meta.get_field('investmentMarkets').choices

   if request.method == 'GET': 
   
      form2 = ShowInvestmentForm()
      context = {'form2':form2,
               'investments':investments,
               'choices':choices_investments}
         
      return render(request, "Main/add_investments.html", context)
   else:
      form2 = ShowInvestmentForm(request.POST)
      context = {'form2':form2,
               'investments':investments,
               'choices':choices_investments}

      amount = request.POST['amount']
      total_investments = 0
      for investment in investments:
         total_investments += investment.amount
      total_investments = float(total_investments)
      total_investments += float(amount)
      print(total_investments, investmentinfo.investment_account_balance, amount)
      if total_investments > investmentinfo.investment_account_balance:
         messages.error(request, "Amount exceeds current balance for investments")
         return render(request,  "Main/add_investments.html", context) 


      percentage = math.ceil((float(amount)/float(investmentinfo.investment_account_balance))*100.00)
      total_percentage = 0
      for investment in investments:
         total_percentage += investment.percentage
      total_percentage = float(total_percentage)
      total_percentage += float(percentage)
      
      if total_percentage > investmentinfo.investment_account_percentage:
         messages.error(request, "Percentage exceeds remaining percentage for Investments")
         return render(request,  "Main/add_investments.html", context) 


      username = request.user.username
      if form2.is_valid():
         invest = form2.save(commit=False)
         invest.user = request.user
         invest.save()
         investments = Investments.objects.filter(user=request.user)
         percentage = math.ceil((float(amount)/float(investmentinfo.investment_account_balance))*100.00)
         for object in investments:
            object.investmentInfo = investinfo
            object.percentage = percentage 
            object.save()
         
         
      return redirect(('/dashboard/'+ username + '/'))



# -----------------------------------INSURANCE VIEW--------------------------------------------

@login_required
def addInsuranceView(request):
   investmentinfo = InvestmentInfo.objects.get(user=request.user)
   investinfo = InvestmentInfo.objects.select_related('user').get(user=request.user)

   insurances = Insurances.objects.filter(user=request.user)
   choices_insurances = Insurances._meta.get_field('investmentMarkets').choices

   if request.method == 'GET': 
         
      form3 = ShowInsuranceForm()
      context = {'form3':form3,
               'insurances':insurances,
               'choices':choices_insurances}
         
      return render(request, "Main/add_insurances.html", context)
   else:
      form3 = ShowInsuranceForm(request.POST)
      context = {'form3':form3,
               'insurances':insurances,
               'choices':choices_insurances}

      amount = request.POST['amount']
      total_insurances = 0
      for insurance in insurances:
         total_insurances += insurance.amount
      total_insurances = float(total_insurances)
      total_insurances += float(amount)
      print(total_insurances, investmentinfo.insurance_account_percentage, amount)
      if total_insurances > investmentinfo.insurance_account_percentage:
         messages.error(request, "Amount exceeds current balance for Insurance")
         return render(request,  "Main/add_insurances.html", context) 


      percentage = math.ceil((float(amount)/float(investmentinfo.insurance_account_balance))*100.00)
      total_percentage = 0
      for insurance in insurances:
         total_percentage += insurance.percentage
      total_percentage = float(total_percentage)
      total_percentage += float(percentage)
      if total_percentage > investmentinfo.insurance_account_percentage:
         messages.error(request, "Percentage exceeds remaining percentage for Insurance")
         return render(request,  "Main/add_insurance.html", context) 


      username = request.user.username
      if form3.is_valid():
         invest = form3.save(commit=False)
         invest.user = request.user
         invest.save()
         insurances = Insurances.objects.filter(user=request.user)
         percentage = math.ceil((float(amount)/float(investmentinfo.insurance_account_balance))*100.00)
         for object in insurances:
            object.investmentInfo = investinfo 
            object.percentage = percentage 
            object.save()
         
         
      return redirect(('/dashboard/'+ username + '/'))
   

      
