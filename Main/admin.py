from django.contrib import admin

# Register your models here.
from .models import InvestmentInfo, Savings, Investments, Insurances, Category, SubCategory

admin.site.register(InvestmentInfo)
admin.site.register(Savings)
admin.site.register(Investments)
admin.site.register(Insurances)
admin.site.register(Category)


@admin.register(SubCategory)
class SubCategoryAdmin(admin.ModelAdmin):
    list_display = ("name", "category")
