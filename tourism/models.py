from django.conf import settings
from django.db import models
from django.contrib.auth.models import User

from hotels.models import Booking

class TouristAttraction(models.Model):
    CITY_CHOICES = [
        ('DAR', 'Dar es Salaam'),
        ('ARU', 'Arusha'),
        ('ZAN', 'Zanzibar'),
        ('ALL', 'All Tanzania'),
    ]
    
    CATEGORY_CHOICES = [
        ('nature', '🌿 Nature & Wildlife'),
        ('beach', '🏖️ Beach & Coast'),
        ('culture', '🎭 Culture & History'),
        ('adventure', '🗻 Adventure & Sports'),
        ('food', '🍲 Food & Dining'),
        ('shopping', '🛍️ Shopping & Markets'),
    ]
    
    name = models.CharField(max_length=200)
    city = models.CharField(max_length=3, choices=CITY_CHOICES)
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES)
    description = models.TextField()
    location = models.CharField(max_length=200)
    entry_fee = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    opening_hours = models.CharField(max_length=100, default="9:00 AM - 5:00 PM")
    best_time_to_visit = models.CharField(max_length=100, default="Morning")
    estimated_visit_time = models.CharField(max_length=50, default="2-3 hours")
    website = models.URLField(blank=True)
    contact_phone = models.CharField(max_length=20, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    partner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='attractions',
        null=True,
        blank=True
    )
    
    class Meta:
        ordering = ['name']
    
    def __str__(self):
        return f"{self.name} - {self.get_city_display()}"
    
    def get_icon(self):
        icons = {
            'nature': 'fa-tree',
            'beach': 'fa-umbrella-beach',
            'culture': 'fa-landmark',
            'adventure': 'fa-mountain',
            'food': 'fa-utensils',
            'shopping': 'fa-shopping-bag',
        }
        return icons.get(self.category, 'fa-map-marker-alt')
    
     
    
    
    def get_image_url(self):
        """Get image URL for this attraction"""
        image = self.get_primary_image()
        if image:
            return image.image_url
        return None
    def get_primary_image(self):
        """Get primary image or first image for this attraction"""
        if hasattr(self, 'images'):
            primary = self.images.filter(is_primary=True).first()
            if primary:
                return primary
            return self.images.first()
        return None


class AttractionImage(models.Model):
    attraction = models.ForeignKey(TouristAttraction, on_delete=models.CASCADE, related_name='images')
    image_url = models.URLField(help_text="Use Unsplash or other image URLs")
    caption = models.CharField(max_length=200, blank=True)
    is_primary = models.BooleanField(default=False)
    
    def __str__(self):
        return f"Image for {self.attraction.name}"

class TourPackage(models.Model):
    attraction = models.ForeignKey(TouristAttraction, on_delete=models.CASCADE, related_name='tour_packages')
    name = models.CharField(max_length=200)
    description = models.TextField()
    duration = models.CharField(max_length=50, default="1 day")
    price = models.DecimalField(max_digits=10, decimal_places=2)
    includes = models.TextField(help_text="List what's included, separated by commas")
    excludes = models.TextField(help_text="List what's excluded, separated by commas", blank=True)
    is_featured = models.BooleanField(default=False)
    
    commission_percentage = models.DecimalField(
        max_digits=5, 
        decimal_places=2, 
        default=20.00
    )
    supplier_name = models.CharField(max_length=200)
    supplier_contact = models.CharField(max_length=100)
    
    partner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='tour_packages',
        null=True,
        blank=True
    )

    
    def __str__(self):
        return f"{self.name} - ${self.price}"
    
    def get_includes_list(self):
        return [item.strip() for item in self.includes.split(',')]
    
    def get_excludes_list(self):
        return [item.strip() for item in self.excludes.split(',')] if self.excludes else []

class UserReview(models.Model):
    RATING_CHOICES = [
        (1, '⭐'),
        (2, '⭐⭐'),
        (3, '⭐⭐⭐'),
        (4, '⭐⭐⭐⭐'),
        (5, '⭐⭐⭐⭐⭐'),
    ]
    
    attraction = models.ForeignKey(TouristAttraction, on_delete=models.CASCADE, related_name='reviews')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    rating = models.IntegerField(choices=RATING_CHOICES)
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.user.username} - {self.attraction.name} ({self.rating} stars)"
    
class BookingTransaction(models.Model):
    TRANSACTION_TYPES = [
        ('hotel', 'Hotel Booking'),
        ('tour', 'Tour Package'),
        ('attraction', 'Attraction Ticket'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    transaction_type = models.CharField(max_length=20, choices=TRANSACTION_TYPES)
    booking = models.ForeignKey(Booking, on_delete=models.SET_NULL, null=True, blank=True)
    tour_package = models.ForeignKey(TourPackage, on_delete=models.SET_NULL, null=True, blank=True)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    commission_amount = models.DecimalField(max_digits=10, decimal_places=2)
    net_amount = models.DecimalField(max_digits=10, decimal_places=2)
    transaction_date = models.DateTimeField(auto_now_add=True)
    payment_status = models.CharField(max_length=20, choices=[
        ('pending', 'Pending'),
        ('completed', 'Completed'),
        ('failed', 'Failed')
    ], default='pending')
    
    
from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator

class TourBooking(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('confirmed', 'Confirmed'),
        ('cancelled', 'Cancelled'),
        ('completed', 'Completed'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    tour_package = models.ForeignKey(TourPackage, on_delete=models.CASCADE, related_name='bookings')
    booking_date = models.DateField()
    number_of_people = models.IntegerField(default=1)  # ADD THIS
    special_requests = models.TextField(blank=True)
    total_price = models.DecimalField(max_digits=10, decimal_places=2)  # ADD THIS
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.user.username} - {self.tour_package.name}"
    
    def save(self, *args, **kwargs):
        # Auto-calculate total price before saving if not set
        if not self.total_price and self.tour_package:
            self.total_price = self.calculate_total_price()
        super().save(*args, **kwargs)
    
    def calculate_total_price(self):
        return self.number_of_people * self.tour_package.price
    """Tour package bookings"""
    
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('confirmed', 'Confirmed'),
        ('cancelled', 'Cancelled'),
        ('completed', 'Completed'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    tour_package = models.ForeignKey('TourPackage', on_delete=models.CASCADE)
    booking_date = models.DateField()
    number_of_people = models.IntegerField(default=1) 
    participants = models.IntegerField(default=1, validators=[MinValueValidator(1)])
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    platform_commission = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    special_requests = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.user.username} - {self.tour_package.name}"
