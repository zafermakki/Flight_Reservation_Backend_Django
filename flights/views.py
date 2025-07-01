from rest_framework.response import Response
from rest_framework import status
from django.db.models import Q
from rest_framework.decorators import APIView
from .models import Flight
from .serializers import FlightSerializer

class SearchFlightsView(APIView):
    def get(self, request):
        country = request.GET.get('country')
        start_date = request.GET.get('start_date')
        end_date = request.GET.get('end_date')
        if not country:
            return Response({'error':'please provide a country name'}, status=status.HTTP_400_BAD_REQUEST)
        
        flights = Flight.objects.filter(
            Q(from_location__icontains=country) | Q(to_location__icontains=country)
        )
        
        if start_date and end_date:
            flights = flights.filter(
                departure_date__range=[start_date, end_date]
            )
        
        if not flights.exists():
            return Response({'message': ' No flights available for the specified country'}, status=status.HTTP_404_NOT_FOUND)
        
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
