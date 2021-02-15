from django.urls import path
from django.conf.urls import re_path
from . import views

urlpatterns = [
    path('', views.indexView, name='index_url'),
    path('register/', views.registerView, name='register_url'),
    path('login/', views.loginView, name='login_url'),
    path('logout/', views.logoutView, name='logout_url'),
    re_path(r'^dashboard/', views.dashboardView, name='dashboard_url'),
    path('add-savings/', views.addSavingsView, name='add_savings_url'),
    path('add-investments/', views.addInvestmentView, name='add_investments_url'),
    path('add-insurances/', views.addInsuranceView, name='add_insurances_url'),
    path('investment/', views.createInvestmetView, name='investment_url'), 
    ]