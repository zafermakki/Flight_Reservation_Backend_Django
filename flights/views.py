from rest_framework.response import Response
from rest_framework import status
from django.db.models import Q
from rest_framework.views import APIView
from .models import Flight
from .serializers import FlightSerializer, LocationSerializer

class SearchFlightsView(APIView):
    def get(self, request):
        from_location = request.GET.get('from_location')
        to_location = request.GET.get('to_location')
        start_date = request.GET.get('start_date')
        end_date = request.GET.get('end_date')
        
        if not from_location or not to_location:
            return Response(
                {'error': 'Please provide both from_location and to_location'},
                status=status.HTTP_400_BAD_REQUEST
            )

        flights = Flight.objects.filter(
            from_location__icontains=from_location,
            to_location__icontains=to_location
        )

        if start_date and end_date:
            flights = flights.filter(
                departure_date__range=[start_date, end_date]
            )

        if not flights.exists():
            return Response(
                {'message': 'No flights found for the specified criteria'},
                status=status.HTTP_404_NOT_FOUND
            )

        serializer = FlightSerializer(flights, many=True)
        return Response(serializer.data)
    
class FlightDetailView(APIView):
    def get(self, request, id):
        try:
            flight = Flight.objects.get(id=id)
            serializer = FlightSerializer(flight)
            return Response(serializer.data, status=200)
        except Flight.DoesNotExist:
            return Response({"error": "Flight not found"}, status=404)

class FromLocationView(APIView):
    def get(self, request):
        locations = Flight.objects.values_list('from_location', flat=True).distinct()
        serializer = LocationSerializer([{'location': loc} for loc in locations], many=True)
        return Response(serializer.data)

class ToLocationView(APIView):
    def get(self, request):
        locations = Flight.objects.values_list('to_location', flat=True).distinct()
        serializer = LocationSerializer([{'location': loc} for loc in locations], many=True)
        return Response(serializer.data)