# Generated by Django 4.0.1 on 2022-02-04 10:47

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('MarketBot', '0002_orders'),
    ]

    operations = [
        migrations.RenameField(
            model_name='orders',
            old_name='Date',
            new_name='date',
        ),
    ]