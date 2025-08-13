# serializers.py

from rest_framework import serializers
from django.db import transaction
from .models import Booking
from flights.models import Flight

from django.core.mail import send_mail

from django.db import transaction

class BookingCreateSerializer(serializers.ModelSerializer):
    flight_id = serializers.PrimaryKeyRelatedField(
        queryset=Flight.objects.all(),
        write_only=True,
        source='flight'  # هذا يربط flight_id مع حقل flight في الـ model
    )

    class Meta:
        model = Booking
        fields = [
            'flight_id',
            'gender',
            'date_of_birth',
            'nationality',
            'email',
            'phone_number',
            'seats_booked',
            'travel_class',
        ]

    def create(self, validated_data):
        print("Flight ID coming from request:", validated_data['flight'].id)
        seats_requested = validated_data['seats_booked']
        travel_class = validated_data['travel_class']
        flight = validated_data.pop('flight')  # هذا الآن كائن Flight مباشرة

        with transaction.atomic():
            flight = Flight.objects.select_for_update().get(pk=flight.pk)
            print("Flight from request:", flight.id)

            # التحقق من المقاعد
            if travel_class == 'economy':
                if flight.available_economy_seats < seats_requested:
                    raise serializers.ValidationError("Not enough economy seats available.")
                flight.available_economy_seats -= seats_requested
            elif travel_class == 'business':
                if flight.available_business_seats < seats_requested:
                    raise serializers.ValidationError("Not enough business seats available.")
                flight.available_business_seats -= seats_requested
            elif travel_class == 'first_class':
                if flight.available_first_class_seats < seats_requested:
                    raise serializers.ValidationError("Not enough first class seats available.")
                flight.available_first_class_seats -= seats_requested

            flight.save()

            booking = Booking.objects.create(flight=flight, **validated_data)

            email = validated_data.get('email')
            if email:
                send_mail(
                    subject="Booking Confirmation",
                    message="Your booking was successful! We wish you a pleasant trip.",
                    from_email=None,
                    recipient_list=[email],
                    fail_silently=True,
                )

            return booking



class BookingSerializer(serializers.ModelSerializer):
    flight = serializers.StringRelatedField()
    
    class Meta:
        model = Booking
        fields = '__all__'