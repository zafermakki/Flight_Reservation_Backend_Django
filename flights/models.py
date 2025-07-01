from django.db import models

    
class Flight(models.Model):
    
    airline = models.CharField(max_length=100)
    
    from_location = models.CharField(max_length=100)
    to_location = models.CharField(max_length=100)
    
    departure_airport = models.CharField(max_length=100,default="aleppo")
    arrival_airport = models.CharField(max_length=100,default="Unknown Airport")
    
    departure_date = models.DateField()
    departure_time = models.TimeField()
    expected_time = models.DurationField(blank=True,null=True,help_text="Expected duration of the flight (hh:mm:ss)")

    price_economy = models.DecimalField(max_digits=10, decimal_places=2,blank=True,null=True)    
    price_business = models.DecimalField(max_digits=10, decimal_places=2,blank=True,null=True)    
    price_first_class = models.DecimalField(max_digits=10, decimal_places=2,blank=True,null=True)    
    
    available_economy_seats = models.PositiveIntegerField(default=0,blank=True,null=True)
    available_business_seats = models.PositiveIntegerField(default=0,blank=True,null=True)
    available_first_class_seats = models.PositiveIntegerField(default=0,blank=True,null=True)
    
    has_transit = models.BooleanField(default=False)
    transit_airport = models.CharField(max_length=100, blank=True, null=True)
    transit_country = models.CharField(max_length=100, blank=True, null=True)
    
    
    def __str__(self) -> str:
        return f"{self.airline} from {self.from_location} to {self.to_location} on {self.departure_date} at {self.departure_time}"
    
class FlightName(models.Model):
    name = models.CharField(max_length=200)
    flight = models.OneToOneField(Flight, on_delete=models.CASCADE, related_name="flight_names")
    
    def __str__(self) -> str:
        return f"{self.name} for flight: {self.flight}"