from django.contrib import admin

# Register your models here.
from .models import InvestmentInfo, Savings, Investments, Insurances

admin.site.register(InvestmentInfo)
admin.site.register(Savings)
admin.site.register(Investments)
admin.site.register(Insurances)
