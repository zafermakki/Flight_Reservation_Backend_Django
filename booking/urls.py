from django.urls import path
from .views import BookingCreateView,CustomerBookingsView,CancelBookingView

urlpatterns = [
    path('create/', BookingCreateView.as_view(), name='booking-create'),
    path('customer-bookings/<str:email>/', CustomerBookingsView.as_view(), name='customer-bookings'),
    path('cancel-booking/<int:booking_id>/', CancelBookingView.as_view(), name='cancel-booking'),
]
