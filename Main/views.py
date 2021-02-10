from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.template import context, loader, RequestContext
from django.urls import reverse
from django.core.exceptions import ObjectDoesNotExist



from .forms import UserForm, InvestmentForm
from .models import InvestmentInfo


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

@login_required
def dashboardView(request):
   try:
      investments = InvestmentInfo.objects.get(user=request.user)
   except ObjectDoesNotExist as e:
      investments = InvestmentInfo.objects.filter(user=request.user)
   context = {
      'investments': investments,
      
   }
   return render(request, 'Main/dashboard.html', context)

def logoutView(request):
   logout(request)
   return redirect('/')

def createInvestmetView(request):
   if request.method == 'GET':
      form = InvestmentForm()
      return render(request, "Main/create_investment.html", {'form':form})
   else:
      form = InvestmentForm(request.POST)
      if form.is_valid():
         investment = form.save(commit=False)
         investment.user = request.user
         investment.save()
         form.save_m2m()
      return redirect('/dashboard/')

def showInvestmentView(request):
   investments = InvestmentInfo.objects.filter(user=request.user)
   return render(request, 'Main/dashboard_post_invest.html', {'investments':investments})

      
