import math

from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator
from hotels.models import Hotel
from tourism.models import TourPackage, TouristAttraction

class Partner(models.Model):
    """Partner/Supplier registration model"""
    
    BUSINESS_TYPES = [
        ('hotel', 'Hotel Owner/Manager'),
        ('tour_operator', 'Tour Operator'),
        ('attraction', 'Tourist Attraction'),
        ('transport', 'Transport Service'),
        ('restaurant', 'Restaurant/Food Service'),
    ]
    
    STATUS_CHOICES = [
        ('pending', 'Pending Approval'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
        ('suspended', 'Suspended'),
    ]
    
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='partner_profile')
    business_name = models.CharField(max_length=200)
    business_type = models.CharField(max_length=50, choices=BUSINESS_TYPES)
    registration_number = models.CharField(max_length=100, blank=True)
    tax_id = models.CharField(max_length=100, blank=True, verbose_name="Tax ID/VAT Number")
    
    # Contact Information
    contact_person = models.CharField(max_length=100)
    phone = models.CharField(max_length=20)
    alternate_phone = models.CharField(max_length=20, blank=True)
    email = models.EmailField()
    website = models.URLField(blank=True)
    
    # Address
    address = models.TextField()
    city = models.CharField(max_length=100, choices=[
        ('DAR', 'Dar es Salaam'),
        ('ARU', 'Arusha'),
        ('ZAN', 'Zanzibar'),
        ('other', 'Other'),
    ])
    
    # Business Details
    description = models.TextField(blank=True)
    year_established = models.PositiveIntegerField(
        validators=[MinValueValidator(1900), MaxValueValidator(2027)],
        null=True, blank=True
    )
    employee_count = models.PositiveIntegerField(default=1)
    
    # Platform Settings
    commission_rate = models.DecimalField(
        max_digits=5, 
        decimal_places=2, 
        default=15.00,
        help_text="Platform commission percentage"
    )
    payment_method = models.CharField(max_length=50, choices=[
        ('bank_transfer', 'Bank Transfer'),
        ('mobile_money', 'Mobile Money'),
        ('paypal', 'PayPal'),
        ('other', 'Other'),
    ], default='bank_transfer')
    
    # Bank/Mobile Money Details
    bank_name = models.CharField(max_length=100, blank=True)
    bank_account = models.CharField(max_length=100, blank=True)
    bank_branch = models.CharField(max_length=100, blank=True)
    mobile_money_provider = models.CharField(max_length=50, blank=True, choices=[
        ('mpesa', 'M-Pesa'),
        ('tigopesa', 'Tigo Pesa'),
        ('airtelmoney', 'Airtel Money'),
        ('halopesa', 'Halo Pesa'),
        ('other', 'Other'),
    ])
    mobile_money_number = models.CharField(max_length=20, blank=True)
    
    # Status & Metadata
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    is_verified = models.BooleanField(default=False)
    verification_date = models.DateField(null=True, blank=True)
    agreement_signed = models.BooleanField(default=False)
    agreement_date = models.DateField(null=True, blank=True)
    
    # Platform Stats
    total_earnings = models.DecimalField(max_digits=12, decimal_places=2, default=0.00)
    pending_payout = models.DecimalField(max_digits=12, decimal_places=2, default=0.00)
    total_paid = models.DecimalField(max_digits=12, decimal_places=2, default=0.00)
    
    # Timestamps
    registration_date = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    latitude = models.DecimalField(
        max_digits=10, 
        decimal_places=7, 
        null=True, 
        blank=True,
        help_text="Latitude coordinate (e.g., -6.7924 for Dar es Salaam)"
    )
    longitude = models.DecimalField(
        max_digits=10, 
        decimal_places=7, 
        null=True, 
        blank=True,
        help_text="Longitude coordinate (e.g., 39.2083 for Dar es Salaam)"
    )
    
    # Google Maps Place ID (optional, for better accuracy)
    google_place_id = models.CharField(max_length=200, blank=True, null=True)
    
    # Distance settings
    delivery_radius_km = models.IntegerField(default=5, help_text="Maximum delivery radius in kilometers")
    is_delivery_available = models.BooleanField(default=False)
    
    def get_coordinates(self):
        """Get coordinates as tuple"""
        if self.latitude and self.longitude:
            return (float(self.latitude), float(self.longitude))
        return None
    
    def calculate_distance_to(self, lat, lng):
        """Calculate distance to another location in kilometers using Haversine formula"""
        if not self.latitude or not self.longitude:
            return None
        
        R = 6371  # Earth's radius in kilometers
        
        lat1 = math.radians(float(self.latitude))
        lon1 = math.radians(float(self.longitude))
        lat2 = math.radians(float(lat))
        lon2 = math.radians(float(lng))
        
        dlon = lon2 - lon1
        dlat = lat2 - lat1
        
        a = math.sin(dlat/2)**2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon/2)**2
        c = 2 * math.asin(math.sqrt(a))
        
        return round(R * c, 2)
    
    def get_distance_from_hotel(self, hotel):
        """Get distance from a specific hotel"""
        if hotel.latitude and hotel.longitude and self.latitude and self.longitude:
            return self.calculate_distance_to(hotel.latitude, hotel.longitude)
        return None
    
    def get_distance_from_stadium(self, stadium):
        """Get distance from a specific stadium"""
        if stadium.latitude and stadium.longitude and self.latitude and self.longitude:
            return self.calculate_distance_to(stadium.latitude, stadium.longitude)
        return None
    
    def get_google_maps_url(self):
        """Get Google Maps URL for directions"""
        if self.latitude and self.longitude:
            return f"https://www.google.com/maps/search/?api=1&query={self.latitude},{self.longitude}"
        elif self.address:
            return f"https://www.google.com/maps/search/?api=1&query={self.address.replace(' ', '+')}"
        return "#"
    
    def get_directions_from_location(self, from_lat, from_lng):
        """Get Google Maps directions URL from a location"""
        if self.latitude and self.longitude:
            return f"https://www.google.com/maps/dir/?api=1&origin={from_lat},{from_lng}&destination={self.latitude},{self.longitude}"
        return "#"
    
    class Meta:
        ordering = ['-registration_date']
        verbose_name = "Business Partner"
        verbose_name_plural = "Business Partners"
    
    def __str__(self):
        return f"{self.business_name} ({self.get_business_type_display()})"
    
    def get_approved_listings_count(self):
        """Count approved listings for this partner"""
        count = 0
        if self.business_type == 'hotel':
            count = Hotel.objects.filter(partner=self.user).count()
        elif self.business_type == 'tour_operator':
            count = TourPackage.objects.filter(partner=self.user).count()
        elif self.business_type == 'attraction':
            count = TouristAttraction.objects.filter(partner=self.user).count()
        return count
    
    def get_active_bookings_count(self):
        """Count active bookings for this partner"""
        from hotels.models import Booking
        from tourism.models import TourBooking
        
        count = 0
        if self.business_type == 'hotel':
            count = Booking.objects.filter(
                hotel__partner=self.user,
                status='confirmed'
            ).count()
        elif self.business_type in ['tour_operator', 'attraction']:
            count = TourBooking.objects.filter(
                tour_package__partner=self.user,
                status='confirmed'
            ).count()
        return count

class PartnerDocument(models.Model):
    """Documents uploaded by partners for verification"""
    
    DOCUMENT_TYPES = [
        ('business_registration', 'Business Registration Certificate'),
        ('tax_certificate', 'Tax Clearance Certificate'),
        ('license', 'Business License'),
        ('id_card', 'National ID/Passport'),
        ('bank_statement', 'Bank Statement'),
        ('other', 'Other'),
    ]
    
    partner = models.ForeignKey(Partner, on_delete=models.CASCADE, related_name='documents')
    document_type = models.CharField(max_length=50, choices=DOCUMENT_TYPES)
    document_file = models.FileField(upload_to='partner_documents/%Y/%m/')
    description = models.CharField(max_length=200, blank=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)
    verified = models.BooleanField(default=False)
    
    def __str__(self):
        return f"{self.get_document_type_display()} - {self.partner.business_name}"

class PartnerPayout(models.Model):
    """Payout records to partners"""
    
    PAYOUT_METHODS = [
        ('bank_transfer', 'Bank Transfer'),
        ('mobile_money', 'Mobile Money'),
        ('cash', 'Cash'),
        ('other', 'Other'),
    ]
    
    PAYOUT_STATUS = [
        ('pending', 'Pending Processing'),
        ('processing', 'Processing'),
        ('completed', 'Completed'),
        ('failed', 'Failed'),
        ('cancelled', 'Cancelled'),
    ]
    
    partner = models.ForeignKey(Partner, on_delete=models.CASCADE, related_name='payouts')
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    commission_deducted = models.DecimalField(max_digits=12, decimal_places=2, default=0.00)
    net_amount = models.DecimalField(max_digits=12, decimal_places=2)
    payout_method = models.CharField(max_length=50, choices=PAYOUT_METHODS)
    
    # Transaction Details
    transaction_id = models.CharField(max_length=100, blank=True)
    reference_number = models.CharField(max_length=100, blank=True)
    bank_reference = models.CharField(max_length=100, blank=True)
    
    # Period Covered
    period_start = models.DateField()
    period_end = models.DateField()
    
    # Status
    status = models.CharField(max_length=20, choices=PAYOUT_STATUS, default='pending')
    notes = models.TextField(blank=True)
    
    # Metadata
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='created_payouts')
    processed_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='processed_payouts')
    processed_date = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"Payout: {self.partner.business_name} - ${self.amount}"

class PartnerCommissionRate(models.Model):
    """Commission rates for different services"""
    
    SERVICE_TYPES = [
        ('hotel_booking', 'Hotel Booking'),
        ('tour_package', 'Tour Package'),
        ('attraction_ticket', 'Attraction Ticket'),
        ('transport', 'Transport Service'),
        ('restaurant', 'Restaurant Booking'),
    ]
    
    partner = models.ForeignKey(Partner, on_delete=models.CASCADE, related_name='commission_rates')
    service_type = models.CharField(max_length=50, choices=SERVICE_TYPES)
    commission_rate = models.DecimalField(max_digits=5, decimal_places=2)
    effective_date = models.DateField()
    is_active = models.BooleanField(default=True)
    
    class Meta:
        unique_together = ['partner', 'service_type']
        ordering = ['-effective_date']
    
    def __str__(self):
        return f"{self.partner}: {self.get_service_type_display()} - {self.commission_rate}%"

class PartnerNotification(models.Model):
    """Notifications sent to partners"""
    
    NOTIFICATION_TYPES = [
        ('booking', 'New Booking'),
        ('payout', 'Payout Processed'),
        ('verification', 'Verification Update'),
        ('system', 'System Announcement'),
        ('promotion', 'Promotion/Special Offer'),
    ]
    
    partner = models.ForeignKey(Partner, on_delete=models.CASCADE, related_name='notifications')
    notification_type = models.CharField(max_length=50, choices=NOTIFICATION_TYPES)
    title = models.CharField(max_length=200)
    message = models.TextField()
    is_read = models.BooleanField(default=False)
    related_booking = models.ForeignKey('hotels.Booking', on_delete=models.SET_NULL, null=True, blank=True)
    related_payout = models.ForeignKey(PartnerPayout, on_delete=models.SET_NULL, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.partner}: {self.title}"
    
class PartnerImage(models.Model):
    """Images uploaded by partners for their business"""
    
    IMAGE_TYPES = [
        ('logo', 'Business Logo'),
        ('cover', 'Cover Photo'),
        ('interior', 'Interior / Facility'),
        ('product', 'Product / Service'),
        ('team', 'Team Photo'),
        ('event', 'Event / Activity'),
        ('other', 'Other'),
    ]
    
    partner = models.ForeignKey(Partner, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='partner_images/%Y/%m/', blank=True, null=True)
    image_url = models.URLField(blank=True, null=True, help_text="Or provide external image URL")
    image_type = models.CharField(max_length=20, choices=IMAGE_TYPES, default='other')
    title = models.CharField(max_length=200, blank=True)
    description = models.TextField(blank=True)
    is_primary = models.BooleanField(default=False)
    display_order = models.IntegerField(default=0)
    is_approved = models.BooleanField(default=False)  # Admin approval needed
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['display_order', '-created_at']
    
    def __str__(self):
        return f"{self.partner.business_name} - {self.get_image_type_display()}"
    
    def get_image_display_url(self):
        """Get the image URL from either uploaded file or external URL"""
        if self.image and hasattr(self.image, 'url'):
            return self.image.url
        return self.image_url