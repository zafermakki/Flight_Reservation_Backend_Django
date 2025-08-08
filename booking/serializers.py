# serializers.py

from rest_framework import serializers
from django.db import transaction
from .models import Booking
from flights.models import Flight

from django.core.mail import send_mail

class BookingCreateSerializer(serializers.ModelSerializer):
    flight_id = serializers.PrimaryKeyRelatedField(
        queryset=Flight.objects.all(), source='flight', write_only=True
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

    def validate(self, data):
        # المبدأ العام هنا هو التحقق لاحقًا داخل المعاملة
        return data

    def create(self, validated_data):
        seats_requested = validated_data['seats_booked']
        travel_class = validated_data['travel_class']
        flight_id = validated_data['flight'].id

        # استخدام المعاملة الذرية مع القفل
        with transaction.atomic():
            # نعيد تحميل الرحلة بقفل لمنع الحجز المتزامن من تعديلها
            flight = Flight.objects.select_for_update().get(id=flight_id)

            # التحقق من توفر الكراسي حسب الدرجة
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

            # إنشاء الحجز
            validated_data['flight'] = flight  # نعيد تعيينه بعد select_for_update
            booking = Booking.objects.create(**validated_data)

            # إرسال رسالة إلى البريد الإلكتروني المدخل
            email = validated_data.get('email')
            if email:
                send_mail(
                    subject="Booking Confirmation",
                    message="Your booking was successful! We wish you a pleasant trip.",
                    from_email=None,  # Use default from settings
                    recipient_list=[email],
                    fail_silently=True,
                )

            return booking

class BookingSerializer(serializers.ModelSerializer):
    flight = serializers.StringRelatedField()
    
    class Meta:
        model = Booking
        fields = '__all__'