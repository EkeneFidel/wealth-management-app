# Generated by Django 3.1.5 on 2021-02-12 08:57

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Main', '0027_auto_20210212_0956'),
    ]

    operations = [
        migrations.AlterField(
            model_name='savings',
            name='investmentInfo',
            field=models.ForeignKey(default=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL), null=True, on_delete=django.db.models.deletion.CASCADE, to='Main.investmentinfo'),
        ),
    ]