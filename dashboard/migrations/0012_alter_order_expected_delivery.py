# Generated by Django 3.2.5 on 2021-08-10 20:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0011_customer_is_money_manager'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='expected_delivery',
            field=models.TimeField(blank=True, null=True),
        ),
    ]