# Generated by Django 4.1.6 on 2023-03-27 18:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0003_rename_localty_customer_locality'),
    ]

    operations = [
        migrations.AlterField(
            model_name='orderplaced',
            name='status',
            field=models.CharField(choices=[('accepted', 'Accepted'), ('packed', 'Packed'), ('on the way', 'On The Way'), ('delivered', 'Delivered'), ('cancel', 'Cancelled')], default='Pending', max_length=50),
        ),
    ]
