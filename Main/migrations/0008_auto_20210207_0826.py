# Generated by Django 3.1.5 on 2021-02-07 07:26

import Main.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Main', '0007_auto_20210204_2100'),
    ]

    operations = [
        migrations.AlterField(
            model_name='investmentinfo',
            name='insurance_account_percentage',
            field=models.CharField(default=25, max_length=100, validators=[Main.models.valid_pct]),
        ),
        migrations.AlterField(
            model_name='investmentinfo',
            name='investment_account_percentage',
            field=models.CharField(default=25, max_length=100, validators=[Main.models.valid_pct]),
        ),
        migrations.AlterField(
            model_name='investmentinfo',
            name='savings_account_percentage',
            field=models.CharField(default=50, max_length=100, validators=[Main.models.valid_pct]),
        ),
    ]
