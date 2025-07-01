from django.db import models
from flights.models import Flight


class Booking(models.Model):
    CLASS_CHOICES = [
        ('economy', 'Economy'),
        ('business', 'Business'),
        ('first_class', 'First Class'),
    ]

    flight = models.ForeignKey(Flight, on_delete=models.CASCADE, related_name="bookings")
    passport_name = models.CharField(max_length=100)
    email = models.EmailField(editable=False)
    seats_booked = models.PositiveIntegerField()
    travel_class = models.CharField(max_length=20, choices=CLASS_CHOICES)
    credit_card_name = models.CharField(max_length=100)
    credit_card_number = models.CharField(max_length=19)
    booking_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.passport_name} on flight {self.flight} ({self.travel_class})"


