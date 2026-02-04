from django.db import models
from django.contrib.auth.models import User
from hotels.models import Hotel, Booking
from tourism.models import TourPackage

class PlatformEarning(models.Model):
    date = models.DateField()
    total_bookings = models.IntegerField(default=0)
    hotel_commission = models.DecimalField(max_digits=12, decimal_places=2, default=0.00)
    tour_commission = models.DecimalField(max_digits=12, decimal_places=2, default=0.00)
    total_commission = models.DecimalField(max_digits=12, decimal_places=2, default=0.00)
    created_at = models.DateTimeField(auto_now_add=True)

class PartnerPayout(models.Model):
    partner = models.ForeignKey(User, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    payment_date = models.DateField()
    status = models.CharField(max_length=20, choices=[
        ('pending', 'Pending'),
        ('paid', 'Paid'),
        ('failed', 'Failed')
    ], default='pending')
    reference_number = models.CharField(max_length=100, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)