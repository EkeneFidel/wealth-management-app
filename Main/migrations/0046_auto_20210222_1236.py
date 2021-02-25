# Generated by Django 3.1.6 on 2021-02-22 11:36

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Main', '0045_auto_20210222_1236'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='savings',
            name='category',
        ),
        migrations.AddField(
            model_name='insurances',
            name='sub_category',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='Main.subcategory'),
        ),
        migrations.AddField(
            model_name='investments',
            name='sub_category',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='Main.subcategory'),
        ),
    ]