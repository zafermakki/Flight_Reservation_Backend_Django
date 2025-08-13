from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status
from django.db.models import Q
from rest_framework.views import APIView
from .models import Flight
from .serializers import FlightSerializer, LocationSerializer

@api_view(['GET'])
def SearchFlightsView(request):
    flight_number = request.query_params.get('flight_number')
    from_location = request.query_params.get('from_location')
    to_location = request.query_params.get('to_location')
    start_date = request.query_params.get('start_date')
    end_date = request.query_params.get('end_date')

    # بحث برقم الرحلة إذا تم إدخاله
    if flight_number:
        flights = Flight.objects.filter(flight_number__iexact=flight_number)
        if not flights.exists():
            return Response({"message": "there is no trip with this number"}, status=status.HTTP_404_NOT_FOUND)
        return Response(FlightSerializer(flights, many=True).data)

    # البحث بالطريقة القديمة
    if not (from_location and to_location and start_date and end_date):
        return Response({"error": "please enter all fields or put the number of the trip"}, status=status.HTTP_400_BAD_REQUEST)

    flights = Flight.objects.filter(
        from_location__iexact=from_location,
        to_location__iexact=to_location,
        departure_date__range=[start_date, end_date]
    )
    if not flights.exists():
        return Response({"message": "there is no trips with this details"}, status=status.HTTP_404_NOT_FOUND)

    return Response(FlightSerializer(flights, many=True).data)

    
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

