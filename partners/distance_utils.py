import math
from decimal import Decimal
from hotels.models import Hotel
from football.models import Stadium

def calculate_distance(lat1, lng1, lat2, lng2):
    """Calculate distance between two points in kilometers"""
    if not all([lat1, lng1, lat2, lng2]):
        return None
    
    R = 6371  # Earth's radius in kilometers
    
    lat1_rad = math.radians(float(lat1))
    lon1_rad = math.radians(float(lng1))
    lat2_rad = math.radians(float(lat2))
    lon2_rad = math.radians(float(lng2))
    
    dlon = lon2_rad - lon1_rad
    dlat = lat2_rad - lat1_rad
    
    a = math.sin(dlat/2)**2 + math.cos(lat1_rad) * math.cos(lat2_rad) * math.sin(dlon/2)**2
    c = 2 * math.asin(math.sqrt(a))
    
    return round(R * c, 2)

def find_nearby_partners(partner, radius_km=5):
    """Find partners within a radius"""
    from .models import Partner
    
    if not partner.latitude or not partner.longitude:
        return []
    
    all_partners = Partner.objects.filter(
        status='approved',
        latitude__isnull=False,
        longitude__isnull=False
    ).exclude(id=partner.id)
    
    nearby = []
    for p in all_partners:
        distance = calculate_distance(
            partner.latitude, partner.longitude,
            p.latitude, p.longitude
        )
        if distance and distance <= radius_km:
            nearby.append({'partner': p, 'distance': distance})
    
    return sorted(nearby, key=lambda x: x['distance'])

def get_partners_near_hotel(hotel, radius_km=3):
    """Get partners near a specific hotel"""
    from .models import Partner
    
    if not hotel.latitude or not hotel.longitude:
        return []
    
    partners = Partner.objects.filter(
        status='approved',
        latitude__isnull=False,
        longitude__isnull=False
    )
    
    results = []
    for partner in partners:
        distance = calculate_distance(
            hotel.latitude, hotel.longitude,
            partner.latitude, partner.longitude
        )
        if distance and distance <= radius_km:
            results.append({'partner': partner, 'distance': distance})
    
    return sorted(results, key=lambda x: x['distance'])

def get_partners_near_stadium(stadium, radius_km=3):
    """Get partners near a specific stadium"""
    from .models import Partner
    
    if not stadium.latitude or not stadium.longitude:
        return []
    
    partners = Partner.objects.filter(
        status='approved',
        latitude__isnull=False,
        longitude__isnull=False
    )
    
    results = []
    for partner in partners:
        distance = calculate_distance(
            stadium.latitude, stadium.longitude,
            partner.latitude, partner.longitude
        )
        if distance and distance <= radius_km:
            results.append({'partner': partner, 'distance': distance})
    
    return sorted(results, key=lambda x: x['distance'])