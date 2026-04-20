# city/admin.py
from django.contrib import admin
from .models import City

@admin.register(City)
class CityAdmin(admin.ModelAdmin):
    list_display = ['name', 'code', 'stadium_name', 'stadium_capacity', 'matches_count', 'hotels_count', 'attractions_count', 'created_at']
    list_filter = ['code', 'created_at']
    search_fields = ['name', 'code', 'stadium_name', 'description']
    prepopulated_fields = {'slug': ('name',)}
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('name', 'code', 'slug', 'tagline', 'description')
        }),
        ('History & Culture', {
            'fields': ('history', 'culture'),
            'classes': ('collapse',)
        }),
        ('Images', {
            'fields': ('hero_image', 'gallery_images'),
            'description': 'Use Unsplash or other image URLs. For gallery, enter JSON array like ["url1", "url2"]'
        }),
        ('Statistics', {
            'fields': ('population', 'area', 'language', 'currency', 'timezone')
        }),
        ('AFCON Information', {
            'fields': ('stadium_name', 'stadium_capacity', 'stadium_image', 'matches_count')
        }),
        ('Weather & Travel', {
            'fields': ('best_time_to_visit', 'average_temperature', 'weather_info')
        }),
        ('Transportation', {
            'fields': ('how_to_get_there', 'getting_around', 'airport_info'),
            'classes': ('collapse',)
        }),
        ('Tourism Information', {
            'fields': ('famous_for', 'local_cuisine', 'popular_activities'),
            'description': 'Popular activities should be entered as JSON array like ["Activity 1", "Activity 2"]'
        }),
        ('Location & Maps', {
            'fields': ('latitude', 'longitude', 'map_embed_url'),
            'classes': ('collapse',)
        }),
        ('SEO', {
            'fields': ('meta_title', 'meta_description'),
            'classes': ('collapse',)
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    readonly_fields = ['created_at', 'updated_at']
    
    def hotels_count(self, obj):
        """Count hotels in this city"""
        from hotels.models import Hotel
        count = Hotel.objects.filter(city=obj.code, is_approved=True).count()
        return count
    hotels_count.short_description = '🏨 Hotels'
    
    def attractions_count(self, obj):
        """Count attractions in this city"""
        from tourism.models import TouristAttraction
        count = TouristAttraction.objects.filter(city=obj.code).count()
        return count
    attractions_count.short_description = '🏛️ Attractions'
    
    def stadiums_count(self, obj):
        """Count stadiums in this city"""
        from football.models import Stadium
        count = Stadium.objects.filter(city=obj.name).count()
        return count
    stadiums_count.short_description = '🏟️ Stadiums'
    
    def matches_count_display(self, obj):
        """Display matches count with icon"""
        return f"⚽ {obj.matches_count}"
    matches_count_display.short_description = 'AFCON Matches'
    
    def get_queryset(self, request):
        return super().get_queryset(request)
    
    def save_model(self, request, obj, form, change):
        """Auto-generate meta_title and meta_description if not provided"""
        if not obj.meta_title:
            obj.meta_title = f"{obj.name} - AFCON 2027 City Guide | Hotels, Attractions & Stadium"
        if not obj.meta_description:
            obj.meta_description = f"Complete guide to {obj.name} for AFCON 2027. Find hotels, tourist attractions, stadium information, local cuisine, and travel tips for {obj.name}."
        super().save_model(request, obj, form, change)