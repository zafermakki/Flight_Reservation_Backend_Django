from django.urls import path
from . import views
from .views import FromLocationView, ToLocationView

urlpatterns = [
    path('search/', views.SearchFlightsView.as_view(), name='search_flights'),
    path('locations/from/', FromLocationView.as_view(), name='from-locations'),
    path('locations/to/', ToLocationView.as_view(), name='to-locations'),
    path('flights/<int:id>/', views.FlightDetailView.as_view(), name='flight-detail'),

]
