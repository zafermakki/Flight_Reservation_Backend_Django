# Generated by Django 4.2.17 on 2025-01-10 19:14

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ("flights", "0003_flightname"),
    ]

    operations = [
        migrations.AlterField(
            model_name="flightname",
            name="flight",
            field=models.OneToOneField(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="flight_names",
                to="flights.flight",
            ),
        ),
    ]
