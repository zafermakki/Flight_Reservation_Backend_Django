from django.core.mail import send_mail
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Flight
from .serializers import BookingSerializer


class BookingView(APIView):
    def post(self, request, *args, **kwargs):
        serializer = BookingSerializer(data=request.data)
        if serializer.is_valid():
            flight_id = request.data.get('flight')
            seats_booked = int(request.data.get('seats_booked'))
            travel_class = request.data.get('travel_class')

            try:
                # Retrieve the flight from the database
                flight = Flight.objects.get(id=flight_id)

                # Check seat availability based on travel class
                if travel_class == 'economy':
                    if flight.available_economy_seats >= seats_booked:
                        flight.available_economy_seats -= seats_booked
                    else:
                        return Response(
                            {"error": f"The available economy seats are {flight.available_economy_seats}. Please select fewer seats."},
                            status=status.HTTP_400_BAD_REQUEST
                        )
                elif travel_class == 'business':
                    if flight.available_business_seats >= seats_booked:
                        flight.available_business_seats -= seats_booked
                    else:
                        return Response(
                            {"error": f"The available business seats are {flight.available_business_seats}. Please select fewer seats."},
                            status=status.HTTP_400_BAD_REQUEST
                        )
                elif travel_class == 'first_class':
                    if flight.available_first_class_seats >= seats_booked:
                        flight.available_first_class_seats -= seats_booked
                    else:
                        return Response(
                            {"error": f"The available first-class seats are {flight.available_first_class_seats}. Please select fewer seats."},
                            status=status.HTTP_400_BAD_REQUEST
                        )
                else:
                    return Response(
                        {"error": "Invalid travel class. Please choose a valid option (economy, business, first_class)."},
                        status=status.HTTP_400_BAD_REQUEST
                    )

                # Save flight updates
                flight.save()

                # Save booking
                booking = serializer.save(email=request.user.email)

                # Send confirmation email
                send_mail(
                    subject='Your Booking Confirmation',
                    message=(
                        f"Dear {request.user.first_name},\n\n"
                        f"Your booking for flight {flight.id} has been successfully completed. "
                        f"We wish you a pleasant journey!\n\n"
                        "Thank you for choosing our service."
                    ),
                    from_email='your-email@gmail.com',
                    recipient_list=[request.user.email],
                    fail_silently=False,
                )

                return Response(serializer.data, status=status.HTTP_201_CREATED)
            except Flight.DoesNotExist:
                return Response(
                    {"error": "The specified flight does not exist."},
                    status=status.HTTP_404_NOT_FOUND
                )

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
