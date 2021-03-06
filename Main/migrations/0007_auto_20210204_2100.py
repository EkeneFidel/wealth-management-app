# Generated by Django 3.1.5 on 2021-02-04 20:00

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Main', '0006_auto_20210204_2043'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='investmentinfo',
            name='avaliable_to_invest',
        ),
        migrations.RemoveField(
            model_name='investmentinfo',
            name='end_date',
        ),
        migrations.RemoveField(
            model_name='investmentinfo',
            name='insurance_account',
        ),
        migrations.RemoveField(
            model_name='investmentinfo',
            name='investment_account',
        ),
        migrations.RemoveField(
            model_name='investmentinfo',
            name='savings_account',
        ),
        migrations.RemoveField(
            model_name='investmentinfo',
            name='start_date',
        ),
        migrations.AlterField(
            model_name='investmentinfo',
            name='insurance_account_percentage',
            field=models.CharField(default=25, max_length=100, validators=[django.core.validators.RegexValidator('^\\d{1,100}$')]),
        ),
        migrations.AlterField(
            model_name='investmentinfo',
            name='investment_account_percentage',
            field=models.CharField(default=25, max_length=100, validators=[django.core.validators.RegexValidator('^\\d{1,100}$')]),
        ),
    ]
