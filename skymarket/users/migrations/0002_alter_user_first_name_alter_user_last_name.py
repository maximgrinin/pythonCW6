# Generated by Django 4.1.6 on 2023-02-08 20:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='first_name',
            field=models.CharField(help_text='Введите имя', max_length=100, verbose_name='Имя'),
        ),
        migrations.AlterField(
            model_name='user',
            name='last_name',
            field=models.CharField(help_text='Введите фамилию', max_length=100, verbose_name='Фамилия'),
        ),
    ]
