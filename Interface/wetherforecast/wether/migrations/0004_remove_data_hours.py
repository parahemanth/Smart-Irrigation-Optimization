# Generated by Django 3.2.20 on 2023-11-10 13:20

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('wether', '0003_data_hours'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='data',
            name='hours',
        ),
    ]