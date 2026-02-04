from django.db import models
from django.contrib.auth.models import User
from django.conf import settings 
from django.utils import timezone

class Hotel(models.Model):
    CITY_CHOICES = [
        ('DAR', 'Dar es Salaam'),
        ('ARU', 'Arusha'),
        ('ZAN', 'Zanzibar'),
    ]
    
    name = models.CharField(max_length=200)
    city = models.CharField(max_length=3, choices=CITY_CHOICES)
    address = models.TextField()
    description = models.TextField(blank=True)
    price_per_night = models.DecimalField(max_digits=10, decimal_places=2)
    available_rooms = models.IntegerField(default=10)
    stars = models.IntegerField(default=3)
    image_url = models.URLField(max_length=500, blank=True)
    
    # Add the missing fields as optional
    wifi = models.BooleanField(default=True)
    pool = models.BooleanField(default=False)
    restaurant = models.BooleanField(default=True)
    parking = models.BooleanField(default=True)
    afcon_special = models.BooleanField(default=False)
    
    
    partner = models.ForeignKey(
        User,  # FIX: Use User directly since you imported it
        on_delete=models.CASCADE,
        related_name='hotels',
        null=True,
        blank=True,
        help_text="Partner who owns/manages this hotel"
    )
    
    # Commission fields
    commission_percentage = models.DecimalField(
        max_digits=5, 
        decimal_places=2, 
        default=15.00,
        help_text="Platform commission percentage"
    )
    partner_contact = models.CharField(max_length=100, blank=True)
    partner_email = models.EmailField(blank=True)
    partner_phone = models.CharField(max_length=20, blank=True)
    
    # Approval fields
    is_approved = models.BooleanField(default=False)
    approval_date = models.DateField(null=True, blank=True)
    approved_by = models.ForeignKey(
        User,  # FIX: Use User directly
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='approved_hotels'
    )
    
    created_at = models.DateTimeField(default=timezone.now)  # Add this
    updated_at = models.DateTimeField(auto_now=True)      # Add this
    
    def get_image_url(self):
        return self.image_url or "https://images.unsplash.com/photo-1566073771259-6a8506099945?auto=format&fit=crop&w=800&q=80"
    
    def __str__(self):
        return f"{self.name} - {self.get_city_display()}"


class RoomType(models.Model):
    hotel = models.ForeignKey(Hotel, on_delete=models.CASCADE, related_name='room_types')
    name = models.CharField(max_length=100, default='Standard Room')
    price_per_night = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    
    def __str__(self):
        return f"{self.hotel.name} - {self.name}"


class Booking(models.Model):
    STATUS_CHOICES = [  # Add status choices
        ('pending', 'Pending'),
        ('confirmed', 'Confirmed'),
        ('cancelled', 'Cancelled'),
        ('completed', 'Completed'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    hotel = models.ForeignKey(Hotel, on_delete=models.CASCADE)
    check_in = models.DateField()
    check_out = models.DateField()
    guests = models.IntegerField(default=1)  # Add this field
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    
    platform_commission = models.DecimalField(
        max_digits=10, 
        decimal_places=2, 
        default=0.00
    )
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    hotel_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')  # Add status
    special_requests = models.TextField(blank=True)  # Add special requests
    
    created_at = models.DateTimeField(default=timezone.now)  # Add timestamps
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.user.username} - {self.hotel.name}"
    
    def calculate_commission(self):
        """Calculate commission automatically"""
        if self.hotel.commission_percentage:
            self.platform_commission = (self.total_price * self.hotel.commission_percentage) / 100
            self.hotel_amount = self.total_price - self.platform_commission
            self.total_amount = self.total_price
    
    def save(self, *args, **kwargs):
        if not self.platform_commission:
            self.calculate_commission()
        super().save(*args, **kwargs)
