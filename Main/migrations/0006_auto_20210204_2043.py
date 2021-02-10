# Generated by Django 3.1.5 on 2021-02-04 19:43

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Main', '0005_auto_20210204_2039'),
    ]

    operations = [
        migrations.AlterField(
            model_name='investmentinfo',
            name='insurance_account_percentage',
            field=models.CharField(default=50, max_length=100, validators=[django.core.validators.RegexValidator('^\\d{1,100}$')]),
        ),
        migrations.AlterField(
            model_name='investmentinfo',
            name='investment_account_percentage',
            field=models.CharField(default=50, max_length=100, validators=[django.core.validators.RegexValidator('^\\d{1,100}$')]),
        ),
        migrations.AlterField(
            model_name='investmentinfo',
            name='savings_account_percentage',
            field=models.CharField(default=50, max_length=100, validators=[django.core.validators.RegexValidator('^\\d{1,100}$')]),
        ),
    ]
