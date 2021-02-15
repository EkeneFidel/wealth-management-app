# Generated by Django 3.1.5 on 2021-02-12 08:33

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Main', '0025_auto_20210212_0932'),
    ]

    operations = [
        migrations.AlterField(
            model_name='insurances',
            name='investmentInfo',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='Main.investmentinfo'),
        ),
        migrations.AlterField(
            model_name='investments',
            name='investmentInfo',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='Main.investmentinfo'),
        ),
        migrations.AlterField(
            model_name='savings',
            name='investmentInfo',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='Main.investmentinfo'),
        ),
    ]