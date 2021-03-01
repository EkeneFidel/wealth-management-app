from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.template import context, loader, RequestContext
from django.urls import reverse
from django.core.exceptions import ObjectDoesNotExist
import math
import json




from .forms import UserForm, InvestmentForm, ShowInvestmentForm, ShowSavingForm, ShowInsuranceForm, EditInvestmentForm
from .models import InvestmentInfo, Savings, Insurances, Investments, SubCategory, Category


# Create your views here.
def indexView(request):
   if request.user.is_authenticated:
      return redirect(('/dashboard/'+ request.user.username + '/'))
   else:
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
   
   categories = Category.objects.all()
   sub_categories = SubCategory.objects.all()
   cats = []
   for category in categories:
      cats.append(category)
   
   arr_length = len(cats)
   context = {
      'investments': investments,
      'savings': savings,
      'invest': invest,
      'insurance': insurance,
      'categories':categories,
      'sub_categories':sub_categories,
      'cats':cats,
      'arr_length':arr_length
      # 'count':count    
      
   }
   return render(request, 'Main/dashboard.html', context)


   # ------------------------------------------------------------------------------------------------------------


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
      form = InvestmentForm(request.POST)
      username = request.POST.get('username')
      monthly_income = request.POST.get('monthly_income')
      monthly_income = float(monthly_income)

      monthly_expenses = request.POST.get('monthly_expenses')
      monthly_expenses = float(monthly_expenses)
      if monthly_expenses > monthly_income:
         messages.error(request, "Monthly expenses is more than monthly income")
         return render(request, "Main/create_investment.html", {'form':form})

      savings_percentage = 50
      insurance_percentage = 25
      investment_percentage = 25

      form = InvestmentForm(request.POST)
      if form.is_valid():
         investment = form.save(commit=False)
         investment.user = request.user
         investment.savings_account_percentage = savings_percentage
         investment.insurance_account_percentage = insurance_percentage
         investment.investment_account_percentage = investment_percentage
         investment.save()
         form.save_m2m()

      categories = Category.objects.all()
      sub_categories = SubCategory.objects.all()
      investment = InvestmentInfo.objects.get(user=request.user)
      total_amount_savings = investment.savings_account_balance
      total_amount_insurance = investment.insurance_account_balance
      total_amount_investment = investment.investment_account_balance

      savings_count = 0.0
      insurance_count = 0.0
      investment_count = 0.0

      for sub_category in sub_categories:
         if sub_category.category.name.lower() == 'savings':
            savings_count += 1
         if sub_category.category.name.lower() == 'insurances':
            insurance_count += 1
         if sub_category.category.name.lower() == 'investments':
            investment_count += 1



      for sub_category in sub_categories:
         if sub_category.category.name.lower() == "savings":
            amount =  math.floor(float(total_amount_savings)/savings_count)
            user = request.user
            investmentInfo =  InvestmentInfo.objects.select_related('user').get(user=request.user)
            percentage = amount/float(investmentInfo.get_available_balance) * 100
            sub_category_a = sub_category
            s = Savings.objects.create(user=user, amount=amount, percentage=percentage, sub_category=sub_category_a)
            s.save()


         
         if sub_category.category.name.lower() == 'insurances':
            amount =  math.floor(float(total_amount_insurance)/insurance_count)
            user = request.user
            investmentInfo =  InvestmentInfo.objects.select_related('user').get(user=request.user)
            percentage = amount/float(investmentInfo.get_available_balance) * 100
            sub_category_a = sub_category
            ins = Insurances.objects.create(user=user, amount=amount, percentage=percentage, sub_category=sub_category_a)
            ins.save()

         if sub_category.category.name.lower() == 'investments':
            amount =  math.floor(float(total_amount_investment)/investment_count)
            user = request.user
            investmentInfo =  InvestmentInfo.objects.select_related('user').get(user=request.user)
            percentage = amount/float(investmentInfo.get_available_balance) * 100
            category = sub_category.category
            sub_category_a = sub_category
            inv = Investments.objects.create(user=user, amount=amount, percentage=percentage, sub_category=sub_category_a)
            inv.save()
      return redirect(('/dashboard/'+ request.user.username + '/'))



# -----------------------------------ADD SAVINGS VIEW--------------------------------------------


@login_required
def editSavingsView(request, id):
   investmentinfo = InvestmentInfo.objects.get(user=request.user)
   investinfo = InvestmentInfo.objects.select_related('user').get(user=request.user)

   saving = Savings.objects.get(pk=id)
   savings = Savings.objects.filter(user = request.user)

   if request.method == 'GET': 

      form1 = ShowSavingForm()
      context = {'form1':form1,
               'saving':saving}
         
      return render(request, "Main/edit_savings.html", context)
   else:
      form1 = ShowSavingForm(request.POST, instance=saving)
      context = {'form1':form1,
               'saving':saving}
      amount = request.POST['amount']
      amount = float(amount)
      total_savings = 0
      for savings in savings:
         total_savings += savings.amount
      total_savings = float(total_savings)
      total_savings -= float(saving.amount)
      total_savings += float(amount)

      if total_savings > investmentinfo.savings_account_balance:
         messages.error(request, "Amount exceeds current balance for savings")
         return render(request,  "Main/edit_savings.html", context) 


      percentage = math.floor(amount)/float(investinfo.get_available_balance) * 100
      username = request.user.username
      if form1.is_valid():
         messages.success(request, "Edited successfully")
         saving = form1.save(commit=False)
         saving.user = request.user
         saving.percentage = percentage
         saving.save()
        
         
      return redirect(('/dashboard/'+ username + '/'))



# -----------------------------------ADD INVESTMENT VIEW--------------------------------------------


@login_required
def editInvestmentView(request, id):
   investmentinfo = InvestmentInfo.objects.get(user=request.user)
   investinfo = InvestmentInfo.objects.select_related('user').get(user=request.user)

   investment = Investments.objects.get(pk=id)
   investments = Investments.objects.filter(user=request.user)
   
   if request.method == 'GET': 
   
      form2 = ShowInvestmentForm()
      context = {'form2':form2,
               'investment':investment}
         
      return render(request, "Main/edit_investments.html", context)
   else:
      form2 = ShowInvestmentForm(request.POST, instance=investment)
      context = {'form2':form2,
               'investment':investment}
      amount = request.POST['amount']
      amount = float(amount)

      total_investments = 0
      for investments in investments:
         total_investments += investments.amount
      total_investments = float(total_investments)
      total_investments -= float(investment.amount)
      total_investments += float(amount)

      if total_investments > investmentinfo.investment_account_balance:
         messages.error(request, "Amount exceeds current balance for investments")
         return render(request,  "Main/edit_investments.html", context) 


      percentage = math.floor(amount)/float(investinfo.get_available_balance) * 100
      username = request.user.username
      if form2.is_valid():
         invest = form2.save(commit=False)
         invest.user = request.user
         invest.percentage = percentage
         invest.save()
         
         
         
      return redirect(('/dashboard/'+ username + '/'))



# -----------------------------------INSURANCE VIEW--------------------------------------------

@login_required
def editInsuranceView(request, id):
   investmentinfo = InvestmentInfo.objects.get(user=request.user)
   investinfo = InvestmentInfo.objects.select_related('user').get(user=request.user)

   insurance = Insurances.objects.get(pk=id)
   insurances = Insurances.objects.filter(user=request.user)

   if request.method == 'GET': 
         
      form3 = ShowInsuranceForm()
      context = {'form3':form3,
               'insurance':insurance}
         
      return render(request, "Main/edit_insurances.html", context)
   else:
      form3 = ShowInsuranceForm(request.POST, instance=insurance)
      context = {'form3':form3,
               'insurance':insurance}

      amount = request.POST['amount']
      amount = float(amount)
      total_insurances = 0
      for insurances in insurances:
         total_insurances += insurance.amount
      total_insurances = float(total_insurances)
      total_insurances -= float(insurance.amount)
      total_insurances += float(amount)

      if total_insurances > investmentinfo.insurance_account_balance:
         messages.error(request, "Amount exceeds current balance for Insurance")
         return render(request,  "Main/edit_insurances.html", context) 


      percentage = math.floor(amount)/float(investinfo.get_available_balance) * 100
      username = request.user.username
      if form3.is_valid():
         insure = form3.save(commit=False)
         insure.user = request.user
         insure.percentage = percentage
         insure.save()
         
         
      return redirect(('/dashboard/'+ username + '/'))



def investment_info_edit(request, id):
   investments = InvestmentInfo.objects.get(pk=id)
   if request.method == 'GET':
      form = EditInvestmentForm()
      context = {
         'investments': investments,
         'form':form
      }
      return render(request, "Main/edit_investment_goals.html", context)
   else:
      username = request.POST.get('username')
      monthly_income = request.POST.get('monthly_income')
      monthly_income = float(monthly_income)

      monthly_expenses = request.POST.get('monthly_expenses')
      monthly_expenses = float(monthly_expenses)

      savings_account_percentage = request.POST.get('savings_account_percentage')
      savings_account_percentage = float(savings_account_percentage)

      insurance_account_percentage = request.POST.get('insurance_account_percentage')
      insurance_account_percentage = float(insurance_account_percentage)

      investment_account_percentage = request.POST.get('investment_account_percentage')
      investment_account_percentage = float(investment_account_percentage)

      form = EditInvestmentForm(request.POST, instance=investments) 
      if form.is_valid():
         messages.success(request, "Updated successfully")
         investment = form.save(commit=False)
         investment.user = request.user
         investment.savings_account_percentage = savings_account_percentage
         investment.insurance_account_percentage = insurance_account_percentage
         investment.investment_account_percentage = investment_account_percentage
         investment.monthly_expenses = monthly_expenses
         investment.monthly_income = monthly_income
         investment.save()

         investment_info = InvestmentInfo.objects.get(pk=id)

         total_amount_savings = investment.savings_account_balance
         savings = Savings.objects.filter(user = request.user)

         if not savings:
            sub_categories = SubCategory.objects.all()
            savings_count = 0.0
            for sub_category in sub_categories:
               if sub_category.category.name.lower() == 'savings':
                  savings_count += 1
            for sub_category in sub_categories:
               if sub_category.category.name.lower() == "savings":
                  amount =  math.floor(float(total_amount_savings)/savings_count)
                  user = request.user
                  investmentInfo =  InvestmentInfo.objects.select_related('user').get(user=request.user)
                  percentage = amount/float(investmentInfo.get_available_balance) * 100
                  sub_category_a = sub_category
                  s = Savings.objects.create(user=user, amount=amount, percentage=percentage, sub_category=sub_category_a)
                  s.save()

         else:
            for saving in savings:
               saving.user = request.user
               saving.investmentInfo =  InvestmentInfo.objects.select_related('user').get(user=request.user)
               saving.amount =  math.floor(float(total_amount_savings)/savings.count())
               saving.percentage = saving.amount/float(investment_info.get_available_balance) * 100
               saving.sub_category = saving.sub_category
               saving.save()


         total_amount_insurance = investment.insurance_account_balance
         insurances = Insurances.objects.filter(user = request.user)


         if not insurances:
            sub_categories = SubCategory.objects.all()
            insurance_count = 0.0
            for sub_category in sub_categories:
               if sub_category.category.name.lower() == 'insurances':
                  insurance_count += 1
            for sub_category in sub_categories:
               if sub_category.category.name.lower() == "insurances":
                  amount =  math.floor(float(total_amount_insurance)/insurance_count)
                  user = request.user
                  investmentInfo =  InvestmentInfo.objects.select_related('user').get(user=request.user)
                  percentage = amount/float(investmentInfo.get_available_balance) * 100
                  sub_category_a = sub_category
                  ins = Insurances.objects.create(user=user, amount=amount, percentage=percentage, sub_category=sub_category_a)
                  ins.save()
         else:
            for insurance in insurances:
               insurance.user = request.user
               insurance.investmentInfo =  InvestmentInfo.objects.select_related('user').get(user=request.user)
               insurance.amount =  math.floor(float(total_amount_insurance)/insurances.count())
               insurance.percentage = insurance.amount/float(investment_info.get_available_balance) * 100
               insurance.sub_category = insurance.sub_category
               insurance.save()


         total_amount_investment = investment.investment_account_balance
         investments = Investments.objects.filter(user = request.user)

         if not investments:
            sub_categories = SubCategory.objects.all()
            investment_count = 0.0
            for sub_category in sub_categories:
               if sub_category.category.name.lower() == 'investments':
                  investment_count += 1
            for sub_category in sub_categories:
               if sub_category.category.name.lower() == "investments":
                  amount =  math.floor(float(total_amount_investment)/investment_count)
                  user = request.user
                  investmentInfo =  InvestmentInfo.objects.select_related('user').get(user=request.user)
                  percentage = amount/float(investmentInfo.get_available_balance) * 100
                  sub_category_a = sub_category
                  inv = Investments.objects.create(user=user, amount=amount, percentage=percentage, sub_category=sub_category_a)
                  inv.save()
         else:
            for investment in investments:
               investment.user = request.user
               investment.investmentInfo =  InvestmentInfo.objects.select_related('user').get(user=request.user)
               investment.amount =  math.floor(float(total_amount_investment)/investments.count())
               investment.percentage = investment.amount/float(investment_info.get_available_balance) * 100
               investment.sub_category = investment.sub_category
               investment.save()

      return redirect(('/dashboard/'+ request.user.username + '/'))     



def investment_info_delete(request, id):
   investment_info = InvestmentInfo.objects.filter(user=request.user)
   savings = Savings.objects.filter(user=request.user)
   insurances = Insurances.objects.filter(user=request.user)
   investments = Investments.objects.filter(user=request.user)
   investment_info.delete()
   savings.delete()
   insurances.delete()
   investments.delete()
   
   messages.success(request, "Investment deleted" )
   return redirect(('/dashboard/'+ request.user.username + '/'))     


def saving_delete(request, id):
   saving = Savings.objects.get(pk=id)
   saving.delete()
   messages.success(request, "Saving deleted" )
   return redirect(('/dashboard/'+ request.user.username + '/'))     


def insurance_delete(request, id):
   insurance = Insurances.objects.get(pk=id)
   insurance.delete()
   messages.success(request, "Insurance deleted" )
   return redirect(('/dashboard/'+ request.user.username + '/'))     


def investment_delete(request, id):
   investment = Investments.objects.get(pk=id)
   investment.delete()
   messages.success(request, "Investment deleted" )
   return redirect(('/dashboard/'+ request.user.username + '/'))     


def pie_chart(request):
   investment_info = InvestmentInfo.objects.get(user=request.user)
   labels = []
   data = []

   def get_monthly_income(investment_info):
      return investment_info.monthly_income

   def get_monthly_expenses(investment_info):
      return investment_info.monthly_expenses

   def get_allocated_amount(investment_info):
      return investment_info.get_total_amount

   def get_available_amount(investment_info):
      return investment_info.available_to_invest
   

   labels.append('Expenses')
   labels.append('Allocated')
   labels.append('Available')

   data.append(float(get_monthly_expenses(investment_info)))
   data.append(float(get_allocated_amount(investment_info)))
   data.append(float(get_available_amount(investment_info)))

   if 0 in data:
      data.remove(0)

   return JsonResponse(data={
        'labels': labels,
        'data': data,
    })


def bucket_pie_chart(request):
   labels = set()
   data = []
   savings = Savings.objects.filter(user = request.user)
   current_savings_balance = 0
   for saving in savings:
      amount_savings = float(saving.amount)
      current_savings_balance += amount_savings
      labels.add(saving.name)
   data.append(current_savings_balance)

   insurances = Insurances.objects.filter(user = request.user)
   current_insurances_balance = 0
   for insurance in insurances:
      amount_insurance = float(insurance.amount)
      current_insurances_balance += amount_insurance
      labels.add(insurance.name)
   data.append(current_insurances_balance)

   investments = Investments.objects.filter(user = request.user)
   current_investments_balance = 0
   for investment in investments:
      amount_investment = float(investment.amount)
      current_investments_balance += amount_investment
      labels.add(investment.name)
   data.append(current_investments_balance)
   labels = list(labels)
   
   if 0 in data:
      data.remove(0)

   return JsonResponse(data={
        'labels': labels,
        'data': data,
    })



def market_pie_chart(request):
   labels = []
   data = []
   savings = Savings.objects.filter(user = request.user)
   for saving in savings:
      amount_savings = float(saving.amount)
      data.append(amount_savings)
      labels.append(str(saving.sub_category))

   insurances = Insurances.objects.filter(user = request.user)
   current_insurances_balance = 0
   for insurance in insurances:
      amount_insurance = float(insurance.amount)
      data.append(amount_insurance)
      labels.append(str(insurance.sub_category))

   investments = Investments.objects.filter(user = request.user)
   current_investments_balance = 0
   for investment in investments:
      amount_investment = float(investment.amount)
      data.append(amount_investment)
      labels.append(str(investment.sub_category))

   if 0 in data:
      data.remove(0)

 
   return JsonResponse(data={
        'labels': labels,
        'data': data,
    })


   