# Generated by Django 4.0.1 on 2022-02-08 10:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('MarketBot', '0005_orders_address_id'),
    ]

    operations = [
        migrations.AddField(
            model_name='orders',
            name='CRM',
            field=models.CharField(default=1, max_length=40),
            preserve_default=False,
        ),
    ]