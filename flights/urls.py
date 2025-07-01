from django.urls import path
from . import views

urlpatterns = [
    path('search/', views.SearchFlightsView.as_view(), name='search_flights'),
    path('flights/<int:id>/', views.FlightDetailView.as_view(), name='flight-detail'),
]
