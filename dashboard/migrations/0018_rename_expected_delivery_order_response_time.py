# Generated by Django 3.2.5 on 2021-08-17 19:42

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0017_order_expected_delivery_time'),
    ]

    operations = [
        migrations.RenameField(
            model_name='order',
            old_name='expected_delivery',
            new_name='response_time',
        ),
    ]
