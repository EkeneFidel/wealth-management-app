# Generated by Django 3.1.6 on 2021-02-17 21:46

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Main', '0038_auto_20210217_2245'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='savings',
            name='sub_category',
        ),
    ]
