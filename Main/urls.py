from django.urls import path
from django.conf.urls import re_path
from . import views

urlpatterns = [
    path('', views.indexView, name='index_url'),
    path('register/', views.registerView, name='register_url'),
    path('login/', views.loginView, name='login_url'),
    path('logout/', views.logoutView, name='logout_url'),
    re_path(r'^dashboard/', views.dashboardView, name='dashboard_url'),
    re_path(r'dashboard1/$', views.showInvestmentView, name='dashboard_post_invest_url'),
    path('investment/', views.createInvestmetView, name='investment_url'),
    ]