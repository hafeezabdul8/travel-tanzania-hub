from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import HotelViewSet, user_bookings, booking_detail, login_api, register_api, user_profile

router = DefaultRouter()
router.register(r'hotels', HotelViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('bookings/', user_bookings, name='api_bookings'),
    path('bookings/<int:pk>/', booking_detail, name='api_booking_detail'),
    path('auth/login/', login_api, name='api_login'),
    path('auth/register/', register_api, name='api_register'),
    path('auth/profile/', user_profile, name='api_profile'),
]