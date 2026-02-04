from django.contrib import admin
from .models import TouristAttraction, AttractionImage, TourPackage, UserReview

class AttractionImageInline(admin.TabularInline):
    model = AttractionImage
    extra = 1

class TourPackageInline(admin.TabularInline):
    model = TourPackage
    extra = 1

@admin.register(TouristAttraction)
class TouristAttractionAdmin(admin.ModelAdmin):
    list_display = ['name', 'city', 'category', 'entry_fee', 'best_time_to_visit']
    list_filter = ['city', 'category']
    search_fields = ['name', 'description', 'location']
    inlines = [AttractionImageInline, TourPackageInline]

@admin.register(UserReview)
class UserReviewAdmin(admin.ModelAdmin):
    list_display = ['user', 'attraction', 'rating', 'created_at']
    list_filter = ['rating', 'created_at']
    search_fields = ['user__username', 'attraction__name', 'comment']
    readonly_fields = ['created_at']

@admin.register(TourPackage)
class TourPackageAdmin(admin.ModelAdmin):
    list_display = ['name', 'attraction', 'duration', 'price', 'is_featured']
    list_filter = ['is_featured', 'attraction__city']
    search_fields = ['name', 'description']
    
from .models import TourBooking

@admin.register(TourBooking)
class TourBookingAdmin(admin.ModelAdmin):
    list_display = ['user', 'tour_package', 'booking_date', 'number_of_people', 'total_price', 'status', 'created_at']
    list_filter = ['status', 'booking_date', 'tour_package__attraction__city']
    search_fields = ['user__username', 'tour_package__name', 'special_requests']
    readonly_fields = ['created_at', 'updated_at']
    
    def get_queryset(self, request):
        return super().get_queryset(request).select_related('user', 'tour_package')