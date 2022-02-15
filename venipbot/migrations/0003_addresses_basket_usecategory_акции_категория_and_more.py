# Generated by Django 4.0.1 on 2022-02-03 06:16

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('venipbot', '0002_alter_telegramchat_id_alter_telegramstate_id_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='addresses',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('chatid', models.CharField(max_length=40)),
                ('address', models.CharField(blank=True, default=None, max_length=400, null=True)),
                ('name', models.CharField(blank=True, default=None, max_length=40, null=True)),
                ('telephone', models.CharField(blank=True, default=None, max_length=40, null=True)),
            ],
            options={
                'verbose_name_plural': 'addresses',
            },
        ),
        migrations.CreateModel(
            name='basket',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('chatid', models.CharField(max_length=40)),
                ('productid', models.CharField(max_length=40)),
                ('quantity', models.CharField(max_length=40)),
                ('action', models.BooleanField()),
            ],
            options={
                'verbose_name_plural': 'basket',
            },
        ),
        migrations.CreateModel(
            name='UseCategory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('chatid', models.CharField(max_length=40)),
                ('category', models.CharField(max_length=40)),
                ('subcategory', models.CharField(max_length=40)),
                ('globall', models.CharField(max_length=40)),
                ('address', models.CharField(blank=True, default=None, max_length=400, null=True)),
                ('name', models.CharField(blank=True, default=None, max_length=40, null=True)),
                ('telephone', models.CharField(blank=True, default=None, max_length=40, null=True)),
                ('handler', models.CharField(blank=True, default=None, max_length=40, null=True)),
            ],
            options={
                'verbose_name_plural': 'UseCategory',
            },
        ),
        migrations.CreateModel(
            name='Акции',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Имя', models.CharField(max_length=40)),
                ('Описание', models.CharField(max_length=400)),
                ('Цена', models.CharField(max_length=40)),
                ('Фото', models.ImageField(upload_to='images/')),
                ('Дата_начала', models.DateTimeField(blank=True, default=None, null=True)),
                ('Дата_окончания', models.DateTimeField(blank=True, default=None, null=True)),
                ('Отключить_акцию', models.BooleanField()),
            ],
            options={
                'verbose_name_plural': 'Акции',
            },
        ),
        migrations.CreateModel(
            name='Категория',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Имя', models.CharField(max_length=40)),
            ],
            options={
                'verbose_name_plural': 'Категория',
            },
        ),
        migrations.CreateModel(
            name='Подкатегория',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Имя', models.CharField(max_length=40)),
                ('Категория', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='venipbot.категория')),
            ],
            options={
                'verbose_name_plural': 'Подкатегория',
            },
        ),
        migrations.CreateModel(
            name='Продукт',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Имя', models.CharField(max_length=40)),
                ('Описание', models.CharField(max_length=400)),
                ('Цена', models.CharField(max_length=40)),
                ('Фото', models.ImageField(upload_to='images/')),
                ('Категория', models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.CASCADE, to='venipbot.категория')),
                ('Подкатегория', models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.CASCADE, to='venipbot.подкатегория')),
            ],
            options={
                'verbose_name_plural': 'Продукт',
            },
        ),
    ]
