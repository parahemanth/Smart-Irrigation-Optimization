# Generated by Django 4.2.7 on 2023-11-09 11:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('wether', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='data',
            name='location',
        ),
        migrations.AddField(
            model_name='data',
            name='locations',
            field=models.CharField(default=None, max_length=50),
            preserve_default=False,
        ),
    ]
