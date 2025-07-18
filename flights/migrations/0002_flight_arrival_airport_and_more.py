# Generated by Django 4.2.17 on 2025-01-10 18:53

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("flights", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="flight",
            name="arrival_airport",
            field=models.CharField(default="Unknown Airport", max_length=100),
        ),
        migrations.AddField(
            model_name="flight",
            name="available_business_seats",
            field=models.PositiveIntegerField(blank=True, default=0, null=True),
        ),
        migrations.AddField(
            model_name="flight",
            name="available_economy_seats",
            field=models.PositiveIntegerField(blank=True, default=0, null=True),
        ),
        migrations.AddField(
            model_name="flight",
            name="available_first_class_seats",
            field=models.PositiveIntegerField(blank=True, default=0, null=True),
        ),
        migrations.AddField(
            model_name="flight",
            name="booking_type",
            field=models.CharField(
                choices=[
                    ("economy", "Economy"),
                    ("business", "Business"),
                    ("first_class", "First Class"),
                ],
                default="economy",
                max_length=50,
            ),
        ),
        migrations.AddField(
            model_name="flight",
            name="departure_airport",
            field=models.CharField(default="aleppo", max_length=100),
        ),
        migrations.AddField(
            model_name="flight",
            name="expected_time",
            field=models.DurationField(
                blank=True,
                help_text="Expected duration of the flight (hh:mm:ss)",
                null=True,
            ),
        ),
        migrations.AddField(
            model_name="flight",
            name="has_transit",
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name="flight",
            name="price_business",
            field=models.DecimalField(
                blank=True, decimal_places=2, max_digits=10, null=True
            ),
        ),
        migrations.AddField(
            model_name="flight",
            name="price_economy",
            field=models.DecimalField(
                blank=True, decimal_places=2, max_digits=10, null=True
            ),
        ),
        migrations.AddField(
            model_name="flight",
            name="price_first_class",
            field=models.DecimalField(
                blank=True, decimal_places=2, max_digits=10, null=True
            ),
        ),
        migrations.AddField(
            model_name="flight",
            name="transit_airport",
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AddField(
            model_name="flight",
            name="transit_country",
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.DeleteModel(
            name="Booking",
        ),
        migrations.DeleteModel(
            name="BookingType",
        ),
    ]
