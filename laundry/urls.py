from django.urls import path

from .views import (
    LaundryBookingCreateView,
    MyLaundryBookingsView
)


urlpatterns = [

    path(
        'book/',
        LaundryBookingCreateView.as_view(),
        name='laundry-book'
    ),

    path(
        'my-bookings/',
        MyLaundryBookingsView.as_view(),
        name='my-bookings'
    ),

]