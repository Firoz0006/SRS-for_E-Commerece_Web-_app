# Generated by Django 4.1.6 on 2023-03-26 05:09

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='customer',
            old_name='loyalty',
            new_name='localty',
        ),
    ]
