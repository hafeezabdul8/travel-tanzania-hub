from rest_framework import serializers
from .models import Hotel, RoomType, Booking
from django.contrib.auth.models import User

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name']

class HotelSerializer(serializers.ModelSerializer):
    city_display = serializers.CharField(source='get_city_display', read_only=True)
    
    class Meta:
        model = Hotel
        fields = '__all__'

class HotelListSerializer(serializers.ModelSerializer):
    city_display = serializers.CharField(source='get_city_display', read_only=True)
    
    class Meta:
        model = Hotel
        fields = ['id', 'name', 'city', 'city_display', 'price_per_night', 
                  'stars', 'image_url', 'available_rooms']

class RoomTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = RoomType
        fields = '__all__'

class BookingSerializer(serializers.ModelSerializer):
    hotel_name = serializers.CharField(source='hotel.name', read_only=True)
    hotel_image = serializers.CharField(source='hotel.get_main_image', read_only=True)
    
    class Meta:
        model = Booking
        fields = '__all__'
        read_only_fields = ['user', 'created_at']