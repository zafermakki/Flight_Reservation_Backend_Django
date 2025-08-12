from rest_framework import serializers
from .models import Flight

class FlightSerializer(serializers.ModelSerializer):
    class Meta:
        model = Flight
        fields = "__all__"

class LocationSerializer(serializers.Serializer):
    location = serializers.CharField()