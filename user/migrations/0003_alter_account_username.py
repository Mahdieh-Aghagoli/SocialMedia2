# Generated by Django 3.2.4 on 2021-06-05 11:29

import common.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0002_alter_account_username'),
    ]

    operations = [
        migrations.AlterField(
            model_name='account',
            name='username',
            field=models.CharField(max_length=30, unique=True, validators=[common.validators.username_validator], verbose_name='Username'),
        ),
    ]
