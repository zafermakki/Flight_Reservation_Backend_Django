from django.db import models
from flights.models import Flight


class Booking(models.Model):
    CLASS_CHOICES = [
        ('economy', 'Economy'),
        ('business', 'Business'),
        ('first_class', 'First Class'),
    ]
    GENDER_CHOICES = [
        ('male', 'Male'),
        ('female', 'Female'),
    ]
    flight = models.ForeignKey(Flight, on_delete=models.CASCADE, related_name="bookings",null=True, blank=True)
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES, default='male')
    date_of_birth = models.DateField(null=True, blank=True)
    nationality = models.CharField(max_length=50,null=True, blank=True)
    
    email = models.EmailField(editable=True)
    phone_number = models.CharField(max_length=20,null=True, blank=True)
    
    seats_booked = models.PositiveIntegerField()
    travel_class = models.CharField(max_length=20, choices=CLASS_CHOICES)
    booking_date = models.DateTimeField(auto_now_add=True)
    

    def __str__(self):
        return f"{self.flight} ({self.travel_class})"


