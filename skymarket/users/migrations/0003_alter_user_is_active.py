# Generated by Django 4.1.6 on 2023-02-09 17:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_alter_user_first_name_alter_user_last_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='is_active',
            field=models.BooleanField(help_text='Укажите, активен ли аккаунт', verbose_name='Активен'),
        ),
    ]
