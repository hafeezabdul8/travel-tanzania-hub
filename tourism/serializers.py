from rest_framework import serializers
from .models import TouristAttraction, TourPackage, UserReview

class TouristAttractionSerializer(serializers.ModelSerializer):
    city_display = serializers.CharField(source='get_city_display', read_only=True)
    category_display = serializers.CharField(source='get_category_display', read_only=True)
    icon = serializers.CharField(source='get_icon', read_only=True)
    
    class Meta:
        model = TouristAttraction
        fields = '__all__'

class TourPackageSerializer(serializers.ModelSerializer):
    attraction_name = serializers.CharField(source='attraction.name', read_only=True)
    
    class Meta:
        model = TourPackage
        fields = '__all__'