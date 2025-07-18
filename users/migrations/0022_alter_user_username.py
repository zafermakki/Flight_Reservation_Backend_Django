# Generated by Django 4.2.17 on 2025-01-25 19:04

import django.contrib.auth.validators
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("users", "0021_user_temp_password"),
    ]

    operations = [
        migrations.AlterField(
            model_name="user",
            name="username",
            field=models.CharField(
                blank=True,
                max_length=250,
                null=True,
                validators=[django.contrib.auth.validators.UnicodeUsernameValidator],
            ),
        ),
    ]
