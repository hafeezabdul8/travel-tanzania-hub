from django.db import models
from django.urls import reverse

class City(models.Model):
    CITY_CHOICES = [
        ('DAR', 'Dar es Salaam'),
        ('ARU', 'Arusha'),
        ('ZAN', 'Zanzibar'),
    ]
    
    name = models.CharField(max_length=100)
    code = models.CharField(max_length=3, choices=CITY_CHOICES, unique=True)
    slug = models.SlugField(unique=True)
    
    # Basic Information
    tagline = models.CharField(max_length=200, help_text="Short catchy phrase about the city")
    description = models.TextField(help_text="Detailed description of the city")
    history = models.TextField(blank=True, help_text="Brief history of the city")
    culture = models.TextField(blank=True, help_text="Cultural information")
    
    # Images
    hero_image = models.URLField(help_text="Main hero image URL")
    gallery_images = models.JSONField(default=list, help_text="List of gallery image URLs")
    
    # Statistics
    population = models.CharField(max_length=50, blank=True)
    area = models.CharField(max_length=50, blank=True)
    language = models.CharField(max_length=100, default="Swahili, English")
    currency = models.CharField(max_length=50, default="Tanzanian Shilling (TZS)")
    timezone = models.CharField(max_length=50, default="EAT (UTC+3)")
    
    # AFCON Information
    stadium_name = models.CharField(max_length=200)
    stadium_capacity = models.IntegerField()
    stadium_image = models.URLField(blank=True)
    matches_count = models.IntegerField(default=0, help_text="Number of AFCON matches hosted")
    
    # Weather Information
    best_time_to_visit = models.CharField(max_length=200, help_text="Best months to visit")
    average_temperature = models.CharField(max_length=100, help_text="Average temperature during AFCON")
    weather_info = models.TextField(blank=True)
    
    # Transportation
    how_to_get_there = models.TextField(help_text="How to reach the city")
    getting_around = models.TextField(help_text="Local transportation options")
    airport_info = models.TextField(blank=True)
    
    # Quick Facts
    famous_for = models.TextField(help_text="What the city is famous for")
    local_cuisine = models.TextField(help_text="Famous local dishes")
    popular_activities = models.JSONField(default=list, help_text="List of popular activities")
    
    # Map
    latitude = models.DecimalField(max_digits=10, decimal_places=7, null=True, blank=True)
    longitude = models.DecimalField(max_digits=10, decimal_places=7, null=True, blank=True)
    map_embed_url = models.URLField(blank=True, help_text="Google Maps embed URL")
    
    # SEO
    meta_title = models.CharField(max_length=200, blank=True)
    meta_description = models.TextField(blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['name']
        verbose_name_plural = "Cities"
    
    def __str__(self):
        return self.name
    
    def get_absolute_url(self):
        return reverse('city:city_detail', args=[self.slug])