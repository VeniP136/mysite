# Generated by Django 4.0.1 on 2022-02-09 07:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('MarketBot', '0006_orders_crm'),
    ]

    operations = [
        migrations.AddField(
            model_name='orders',
            name='youMoneyId',
            field=models.CharField(default=1, max_length=80),
            preserve_default=False,
        ),
    ]
