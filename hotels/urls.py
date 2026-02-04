from django.urls import path
from . import views

urlpatterns = [
    path('', views.hotel_list, name='hotel_list'),
    path('<int:hotel_id>/', views.hotel_detail, name='hotel_detail'),
    path('<int:hotel_id>/book/', views.book_hotel, name='book_hotel'),
    path('booking/<int:booking_id>/', views.booking_confirmation, name='booking_confirmation'),
    path('my-bookings/', views.my_bookings, name='my_bookings'),
]