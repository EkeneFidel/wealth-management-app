# Generated by Django 3.1.5 on 2021-02-12 09:24

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Main', '0030_auto_20210212_1021'),
    ]

    operations = [
        migrations.AlterField(
            model_name='savings',
            name='investmentInfo',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='Main.investmentinfo'),
        ),
    ]
