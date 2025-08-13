from django.urls import path
from . import views
from .views import FromLocationView, ToLocationView, SearchFlightsView

urlpatterns = [
    path('search/', SearchFlightsView, name='search_flights'),
    path('locations/from/', FromLocationView.as_view(), name='from-locations'),
    path('locations/to/', ToLocationView.as_view(), name='to-locations'),
    path('flights/<int:id>/', views.FlightDetailView.as_view(), name='flight-detail'),

]
