from django.contrib import admin
from .models import Hotel, RoomType, Booking

@admin.register(Hotel)
class HotelAdmin(admin.ModelAdmin):
    list_display = ['name', 'city', 'stars', 'price_per_night', 'available_rooms']
    list_filter = ['city', 'stars']
    search_fields = ['name', 'city', 'address']

@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ['user', 'hotel', 'check_in', 'check_out', 'total_price']
    list_filter = ['check_in']
    search_fields = ['user__username', 'hotel__name']

@admin.register(RoomType)
class RoomTypeAdmin(admin.ModelAdmin):
    list_display = ['name', 'hotel', 'price_per_night']