from django.urls import path
from django.conf.urls import re_path, url
from . import views

urlpatterns = [
    path('', views.indexView, name='index_url'),
    path('register/', views.registerView, name='register_url'),
    path('login/', views.loginView, name='login_url'),
    path('logout/', views.logoutView, name='logout_url'),
    re_path(r'^dashboard/', views.dashboardView, name='dashboard_url'),
    path('edit-savings/<int:id>', views.editSavingsView, name='edit_savings_url'),
    path('delete-savings/<int:id>', views.saving_delete, name='delete_savings_url'),

    path('edit-investments/<int:id>', views.editInvestmentView, name='edit_investments_url'),
    path('delete-investments/<int:id>', views.investment_delete, name='delete_investments_url'),

    path('edit-insurances/<int:id>', views.editInsuranceView, name='edit_insurances_url'),
    path('delete-insurances/<int:id>', views.insurance_delete, name='delete_insurances_url'),

    path('investment/', views.createInvestmetView, name='investment_url'), 
    path('edit-investment/<int:id>', views.investment_info_edit, name='investment_goals_edit'), 
    path('delete-investment-info/<int:id>', views.investment_info_delete, name='investment_goals_delete'), 
    path('pie-chart', views.pie_chart, name='pie_chart'),
    path('bucket-pie-chart', views.bucket_pie_chart, name='bucket_pie_chart'),
    path('market-pie-chart', views.market_pie_chart, name='market_pie_chart'),
    ]