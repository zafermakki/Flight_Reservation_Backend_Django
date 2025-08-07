from rest_framework import generics
from .models import Booking
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import BookingCreateSerializer,BookingSerializer

class BookingCreateView(generics.CreateAPIView):
    queryset = Booking.objects.all()
    serializer_class = BookingCreateSerializer

class CustomerBookingsView(generics.ListAPIView):
    serializer_class = BookingSerializer

    def get_queryset(self):
        email = self.kwargs.get('email')
        return Booking.objects.filter(email=email)

class CancelBookingView(APIView):
    def delete(self, request, booking_id):
        try:
            booking = Booking.objects.get(id=booking_id)
            flight = booking.flight
            seats_to_return = booking.seats_booked
            travel_class = booking.travel_class

            # تحديث عدد المقاعد المتوفرة حسب نوع الحجز
            if travel_class == 'economy':
                flight.available_economy_seats += seats_to_return
            elif travel_class == 'business':
                flight.available_business_seats += seats_to_return
            elif travel_class == 'first_class':
                flight.available_first_class_seats += seats_to_return
            else:
                return Response({'error': 'Invalid travel class'}, status=status.HTTP_400_BAD_REQUEST)

            flight.save()  # حفظ التعديلات
            booking.delete()  # حذف الحجز

            return Response({'message': 'Booking cancelled and seats restored successfully'}, status=status.HTTP_200_OK)

        except Booking.DoesNotExist:
            return Response({'error': 'Booking not found'}, status=status.HTTP_404_NOT_FOUND)