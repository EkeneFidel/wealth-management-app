# Generated by Django 3.1.6 on 2021-02-17 21:49

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Main', '0040_remove_savings_category'),
    ]

    operations = [
        migrations.AddField(
            model_name='savings',
            name='category',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='Main.category'),
        ),
        migrations.AddField(
            model_name='savings',
            name='sub_category',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='Main.subcategory'),
        ),
    ]
