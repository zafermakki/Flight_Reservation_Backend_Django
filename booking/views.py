from rest_framework import generics
from .models import Booking
from .serializers import BookingCreateSerializer

class BookingCreateView(generics.CreateAPIView):
    queryset = Booking.objects.all()
    serializer_class = BookingCreateSerializer