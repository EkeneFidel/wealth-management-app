# Generated by Django 3.1.5 on 2021-02-12 09:12

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Main', '0028_auto_20210212_0957'),
    ]

    operations = [
        migrations.AlterField(
            model_name='savings',
            name='investmentInfo',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='Main.investmentinfo'),
        ),
    ]
