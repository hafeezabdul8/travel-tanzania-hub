from django.shortcuts import render, get_object_or_404
from django.db.models import Q
from .models import City
from hotels.models import Hotel
from tourism.models import TouristAttraction
from football.models import Stadium, Match

def city_detail(request, slug):
    """Detailed city guide page"""
    city = get_object_or_404(City, slug=slug)
    
    # Get hotels in this city
    hotels = Hotel.objects.filter(city=city.code, is_approved=True)[:6]
    
    # Get tourist attractions in this city
    attractions = TouristAttraction.objects.filter(city=city.code)[:6]
    
    # Get stadiums in this city
    stadiums = Stadium.objects.filter(city=city.name)[:3]
    
    # Get upcoming matches in this city
    matches = Match.objects.filter(stadium__city=city.name, status='scheduled')[:5]
    
    # Get all hotels count
    hotels_count = Hotel.objects.filter(city=city.code, is_approved=True).count()
    
    # Get all attractions count
    attractions_count = TouristAttraction.objects.filter(city=city.code).count()
    
    # Get top rated hotels (by stars)
    top_hotels = Hotel.objects.filter(city=city.code, is_approved=True).order_by('-stars')[:3]
    
    # Get featured attractions
    featured_attractions = attractions[:3]
    
    context = {
        'city': city,
        'hotels': hotels,
        'attractions': attractions,
        'stadiums': stadiums,
        'matches': matches,
        'hotels_count': hotels_count,
        'attractions_count': attractions_count,
        'top_hotels': top_hotels,
        'featured_attractions': featured_attractions,
    }
    return render(request, 'city/city_detail.html', context)