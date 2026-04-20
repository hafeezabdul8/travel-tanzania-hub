# hotels/add_sample_hotels.py
import os
import sys
import django

# Add the project root to Python path
sys.path.append('/home/feezman/afcon_project')

# Set the Django settings module
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'afcon.settings')

# Initialize Django
django.setup()

from decimal import Decimal
from django.utils import timezone
from hotels.models import Hotel, RoomType
from django.contrib.auth.models import User

def add_hotels():
    """Add sample hotels with images for AFCON 2027"""
    
    print("=" * 60)
    print("Adding Sample Hotels for AFCON 2027")
    print("=" * 60)
    
    # Get or create a default admin user as partner
    admin_user, created = User.objects.get_or_create(
        username='admin',
        defaults={'email': 'admin@example.com', 'is_staff': True}
    )
    if created:
        admin_user.set_password('admin123')
        admin_user.save()
        print("✅ Created admin user for partner reference")
    else:
        print(f"✅ Using existing admin user: {admin_user.username}")
    
    # ============ DAR ES SALAAM HOTELS ============
    dar_hotels = [
        {
            'name': 'Serena Hotel Dar es Salaam',
            'city': 'DAR',
            'address': 'Ohio Street, Dar es Salaam',
            'description': 'Luxury 5-star hotel with stunning ocean views, infinity pool, and world-class dining. Located just 3km from National Stadium.',
            'price_per_night': 250,
            'available_rooms': 120,
            'stars': 5,
            'wifi': True,
            'pool': True,
            'restaurant': True,
            'parking': True,
            'afcon_special': True,
            'image_url': 'https://images.unsplash.com/photo-1566073771259-6a8506099945?w=800',
        },
        {
            'name': 'Hyatt Regency Dar es Salaam',
            'city': 'DAR',
            'address': 'Kivukoni Street, Dar es Salaam',
            'description': 'Modern luxury hotel with panoramic Indian Ocean views, rooftop pool, and multiple restaurants.',
            'price_per_night': 220,
            'available_rooms': 150,
            'stars': 5,
            'wifi': True,
            'pool': True,
            'restaurant': True,
            'parking': True,
            'afcon_special': True,
            'image_url': 'https://images.unsplash.com/photo-1582719508461-905c673771fd?w=800',
        },
        {
            'name': 'Holiday Inn Dar es Salaam',
            'city': 'DAR',
            'address': 'Azikiwe Street, Dar es Salaam',
            'description': 'Comfortable mid-range hotel with excellent amenities, close to shopping centers.',
            'price_per_night': 120,
            'available_rooms': 80,
            'stars': 4,
            'wifi': True,
            'pool': True,
            'restaurant': True,
            'parking': True,
            'afcon_special': False,
            'image_url': 'https://images.unsplash.com/photo-1551882547-ff40c63fe5fa?w=800',
        },
        {
            'name': 'Peacock Hotel',
            'city': 'DAR',
            'address': 'Bibi Titi Mohammed Road, Dar es Salaam',
            'description': 'Affordable comfort with great service, rooftop pool, and just 1.5km from National Stadium.',
            'price_per_night': 80,
            'available_rooms': 60,
            'stars': 3,
            'wifi': True,
            'pool': True,
            'restaurant': True,
            'parking': True,
            'afcon_special': True,
            'image_url': 'https://images.unsplash.com/photo-1564501049412-61c2a3083791?w=800',
        },
        {
            'name': 'Johari Rotana',
            'city': 'DAR',
            'address': 'Peninsula Road, Dar es Salaam',
            'description': 'Sophisticated 5-star hotel with exceptional service, spa, and fine dining.',
            'price_per_night': 280,
            'available_rooms': 100,
            'stars': 5,
            'wifi': True,
            'pool': True,
            'restaurant': True,
            'parking': True,
            'afcon_special': True,
            'image_url': 'https://images.unsplash.com/photo-1584132967334-10e028bd69f7?w=800',
        },
    ]
    
    # ============ ARUSHA HOTELS ============
    arusha_hotels = [
        {
            'name': 'Arusha Serena Hotel',
            'city': 'ARU',
            'address': 'Serengeti Road, Arusha',
            'description': 'Luxury safari lodge style hotel with stunning views of Mount Meru.',
            'price_per_night': 180,
            'available_rooms': 75,
            'stars': 5,
            'wifi': True,
            'pool': True,
            'restaurant': True,
            'parking': True,
            'afcon_special': True,
            'image_url': 'https://images.unsplash.com/photo-1566073771259-6a8506099945?w=800',
        },
        {
            'name': 'Mount Meru Hotel',
            'city': 'ARU',
            'address': 'P.O. Box 790, Arusha',
            'description': 'Premier hotel with spectacular views of Mount Meru, large pool, and conference facilities.',
            'price_per_night': 150,
            'available_rooms': 120,
            'stars': 4,
            'wifi': True,
            'pool': True,
            'restaurant': True,
            'parking': True,
            'afcon_special': False,
            'image_url': 'https://images.unsplash.com/photo-1582719508461-905c673771fd?w=800',
        },
        {
            'name': 'Kibo Palace Hotel',
            'city': 'ARU',
            'address': 'Old Moshi Road, Arusha',
            'description': 'Modern boutique hotel with rooftop restaurant and excellent service.',
            'price_per_night': 100,
            'available_rooms': 50,
            'stars': 4,
            'wifi': True,
            'pool': True,
            'restaurant': True,
            'parking': True,
            'afcon_special': True,
            'image_url': 'https://images.unsplash.com/photo-1551882547-ff40c63fe5fa?w=800',
        },
        {
            'name': 'Arusha Hotel',
            'city': 'ARU',
            'address': 'P.O. Box 88, Arusha',
            'description': 'Historic hotel (est. 1894) with colonial charm, recently renovated.',
            'price_per_night': 70,
            'available_rooms': 80,
            'stars': 3,
            'wifi': True,
            'pool': False,
            'restaurant': True,
            'parking': True,
            'afcon_special': False,
            'image_url': 'https://images.unsplash.com/photo-1564501049412-61c2a3083791?w=800',
        },
        {
            'name': 'The African Tulip',
            'city': 'ARU',
            'address': 'Serengeti Road, Arusha',
            'description': 'Boutique hotel with beautiful gardens, swimming pool, and excellent restaurant.',
            'price_per_night': 160,
            'available_rooms': 45,
            'stars': 4,
            'wifi': True,
            'pool': True,
            'restaurant': True,
            'parking': True,
            'afcon_special': True,
            'image_url': 'https://images.unsplash.com/photo-1584132967334-10e028bd69f7?w=800',
        },
    ]
    
    # ============ ZANZIBAR HOTELS ============
    zanzibar_hotels = [
        {
            'name': 'Zanzibar Serena Hotel',
            'city': 'ZAN',
            'address': 'Stone Town, Zanzibar',
            'description': 'Luxury hotel in historic Stone Town, blending Swahili architecture with modern amenities.',
            'price_per_night': 300,
            'available_rooms': 60,
            'stars': 5,
            'wifi': True,
            'pool': True,
            'restaurant': True,
            'parking': True,
            'afcon_special': True,
            'image_url': 'https://images.unsplash.com/photo-1566073771259-6a8506099945?w=800',
        },
        {
            'name': 'The Residence Zanzibar',
            'city': 'ZAN',
            'address': 'Kiwengwa Beach, Zanzibar',
            'description': 'Ultra-luxury beach resort with private villas, spa, and exceptional dining.',
            'price_per_night': 350,
            'available_rooms': 90,
            'stars': 5,
            'wifi': True,
            'pool': True,
            'restaurant': True,
            'parking': True,
            'afcon_special': True,
            'image_url': 'https://images.unsplash.com/photo-1582719508461-905c673771fd?w=800',
        },
        {
            'name': 'TUI Blue Bahari Zanzibar',
            'city': 'ZAN',
            'address': 'Kiwengwa Beach, Zanzibar',
            'description': 'All-inclusive beach resort with excellent facilities, perfect for football fans.',
            'price_per_night': 180,
            'available_rooms': 150,
            'stars': 4,
            'wifi': True,
            'pool': True,
            'restaurant': True,
            'parking': True,
            'afcon_special': False,
            'image_url': 'https://images.unsplash.com/photo-1551882547-ff40c63fe5fa?w=800',
        },
        {
            'name': 'Gold Zanzibar Beach House',
            'city': 'ZAN',
            'address': 'Kendwa Beach, Zanzibar',
            'description': 'Beachfront boutique hotel with stunning sunset views.',
            'price_per_night': 120,
            'available_rooms': 35,
            'stars': 4,
            'wifi': True,
            'pool': True,
            'restaurant': True,
            'parking': True,
            'afcon_special': True,
            'image_url': 'https://images.unsplash.com/photo-1564501049412-61c2a3083791?w=800',
        },
        {
            'name': 'Park Hyatt Zanzibar',
            'city': 'ZAN',
            'address': 'Stone Town, Zanzibar',
            'description': 'Luxury beachfront hotel in Stone Town, combining history with modern luxury.',
            'price_per_night': 320,
            'available_rooms': 55,
            'stars': 5,
            'wifi': True,
            'pool': True,
            'restaurant': True,
            'parking': True,
            'afcon_special': True,
            'image_url': 'https://images.unsplash.com/photo-1584132967334-10e028bd69f7?w=800',
        },
    ]
    
    # Combine all hotels
    all_hotels = dar_hotels + arusha_hotels + zanzibar_hotels
    
    hotels_created = 0
    hotels_existing = 0
    
    print("\n📋 Adding hotels...\n")
    
    for hotel_data in all_hotels:
        hotel, created = Hotel.objects.get_or_create(
            name=hotel_data['name'],
            defaults={
                'city': hotel_data['city'],
                'address': hotel_data['address'],
                'description': hotel_data['description'],
                'price_per_night': Decimal(str(hotel_data['price_per_night'])),
                'available_rooms': hotel_data['available_rooms'],
                'stars': hotel_data['stars'],
                'wifi': hotel_data['wifi'],
                'pool': hotel_data['pool'],
                'restaurant': hotel_data['restaurant'],
                'parking': hotel_data['parking'],
                'afcon_special': hotel_data.get('afcon_special', False),
                'image_url': hotel_data['image_url'],
                'is_approved': True,
                'partner': admin_user,
                'created_at': timezone.now(),
            }
        )
        
        if created:
            hotels_created += 1
            print(f"✅ Created: {hotel.name} - {hotel.get_city_display()} - ${hotel.price_per_night}/night")
            
            # Create room types for each hotel - FIXED: Use Decimal multiplication
            price = hotel.price_per_night
            room_types = [
                {'name': 'Standard Room', 'price': price * Decimal('0.8')},
                {'name': 'Deluxe Room', 'price': price},
                {'name': 'Executive Suite', 'price': price * Decimal('1.5')},
            ]
            
            for rt in room_types:
                room_type, rt_created = RoomType.objects.get_or_create(
                    hotel=hotel,
                    name=rt['name'],
                    defaults={'price_per_night': rt['price']}
                )
                if rt_created:
                    print(f"   └─ Added room type: {rt['name']} (${rt['price']:.0f}/night)")
        else:
            hotels_existing += 1
            print(f"⚠️ Already exists: {hotel.name}")
    
    # Print summary
    print("\n" + "=" * 60)
    print("HOTEL ADDITION SUMMARY")
    print("=" * 60)
    print(f"✅ New hotels created: {hotels_created}")
    print(f"⚠️ Existing hotels skipped: {hotels_existing}")
    print(f"🏨 Total hotels in database: {Hotel.objects.count()}")
    print(f"   - Dar es Salaam: {Hotel.objects.filter(city='DAR').count()}")
    print(f"   - Arusha: {Hotel.objects.filter(city='ARU').count()}")
    print(f"   - Zanzibar: {Hotel.objects.filter(city='ZAN').count()}")
    print(f"🏷️  Total room types: {RoomType.objects.count()}")
    print("=" * 60)
    print("\n🎉 All hotels added successfully!")
    print("\n📸 Images are from Unsplash and will display on the hotel listing page.")

if __name__ == "__main__":
    add_hotels()