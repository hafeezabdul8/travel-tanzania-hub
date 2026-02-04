import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'afcon.settings')
django.setup()

from hotels.models import Hotel

# Simple hotels with only the fields your model has
SIMPLE_HOTELS = [
    # DAR ES SALAAM
    {
        'name': 'Serena Hotel Dar es Salaam',
        'city': 'DAR',
        'address': 'Ohio Street, Dar es Salaam',
        'description': '5-star luxury hotel with sea views. Official AFCON partner.',
        'price_per_night': 450,
        'available_rooms': 40,
        'image_url': 'https://images.unsplash.com/photo-1566073771259-6a8506099945?ixlib=rb-4.0.3&auto=format&fit=crop&w=1200&q=80',
        'stars': 5,
    },
    {
        'name': 'Hyatt Regency Dar es Salaam',
        'city': 'DAR',
        'address': 'Kivukoni Front, Dar es Salaam',
        'description': 'Modern luxury hotel with harbor views.',
        'price_per_night': 420,
        'available_rooms': 35,
        'image_url': 'https://images.unsplash.com/photo-1584132967334-10e028bd69f7?ixlib=rb-4.0.3&auto=format&fit=crop&w=1200&q=80',
        'stars': 5,
    },
    {
        'name': 'Holiday Inn Dar es Salaam',
        'city': 'DAR',
        'address': 'City Center, Dar es Salaam',
        'description': 'Perfect for football teams and delegations.',
        'price_per_night': 220,
        'available_rooms': 60,
        'image_url': 'https://images.unsplash.com/photo-1568084680786-a84f91d1153c?ixlib=rb-4.0.3&auto=format&fit=crop&w=1200&q=80',
        'stars': 4,
    },
    {
        'name': 'Southern Sun Dar es Salaam',
        'city': 'DAR',
        'address': 'Garden Avenue, Dar es Salaam',
        'description': 'City center hotel with rooftop pool.',
        'price_per_night': 280,
        'available_rooms': 45,
        'image_url': 'https://images.unsplash.com/photo-1542314831-068cd1dbfeeb?ixlib=rb-4.0.3&auto=format&fit=crop&w=1200&q=80',
        'stars': 4,
    },
    
    # ARUSHA
    {
        'name': 'Arusha Serena Hotel',
        'city': 'ARU',
        'address': 'Dodoma Road, Arusha',
        'description': 'Luxury resort with Mount Meru views.',
        'price_per_night': 350,
        'available_rooms': 28,
        'image_url': 'https://images.unsplash.com/photo-1516026672322-bc52d61a55d5?ixlib=rb-4.0.3&auto=format&fit=crop&w=1200&q=80',
        'stars': 5,
    },
    {
        'name': 'Mount Meru Hotel',
        'city': 'ARU',
        'address': 'Old Moshi Road, Arusha',
        'description': 'Historic hotel popular with safari groups.',
        'price_per_night': 180,
        'available_rooms': 65,
        'image_url': 'https://images.unsplash.com/photo-1542314831-068cd1dbfeeb?ixlib=rb-4.0.3&auto=format&fit=crop&w=1200&q=80',
        'stars': 4,
    },
    {
        'name': 'Kibo Palace Hotel',
        'city': 'ARU',
        'address': 'Old Moshi Road, Arusha',
        'description': 'Modern luxury hotel with Kilimanjaro views.',
        'price_per_night': 320,
        'available_rooms': 40,
        'image_url': 'https://images.unsplash.com/photo-1584132967334-10e028bd69f7?ixlib=rb-4.0.3&auto=format&fit=crop&w=1200&q=80',
        'stars': 5,
    },
    
    # ZANZIBAR
    {
        'name': 'Zanzibar Serena Hotel',
        'city': 'ZAN',
        'address': 'Stone Town, Zanzibar',
        'description': 'Beachfront hotel in historic Stone Town.',
        'price_per_night': 480,
        'available_rooms': 35,
        'image_url': 'https://images.unsplash.com/photo-1563492065599-3520f775eeed?ixlib=rb-4.0.3&auto=format&fit=crop&w=1200&q=80',
        'stars': 5,
    },
    {
        'name': 'The Residence Zanzibar',
        'city': 'ZAN',
        'address': 'Kiwengwa, Zanzibar',
        'description': 'Luxury villa resort with private pools.',
        'price_per_night': 650,
        'available_rooms': 20,
        'image_url': 'https://images.unsplash.com/photo-1561501878-aabd62634533?ixlib=rb-4.0.3&auto=format&fit=crop&w=1200&q=80',
        'stars': 5,
    },
    {
        'name': 'Tembo Hotel Zanzibar',
        'city': 'ZAN',
        'address': 'Shangani, Stone Town',
        'description': 'Historic hotel with ocean views.',
        'price_per_night': 190,
        'available_rooms': 45,
        'image_url': 'https://images.unsplash.com/photo-1571896349842-33c89424de2d?ixlib=rb-4.0.3&auto=format&fit=crop&w=1200&q=80',
        'stars': 4,
    },
]

print("Creating 10 key hotels...")
for hotel_data in SIMPLE_HOTELS:
    hotel, created = Hotel.objects.get_or_create(
        name=hotel_data['name'],
        defaults=hotel_data
    )
    print(f"{'✅ Created' if created else '📝 Exists'}: {hotel.name}")

print(f"\n🎉 Total hotels: {Hotel.objects.count()}")
print(f"🏙️  Dar es Salaam: {Hotel.objects.filter(city='DAR').count()}")
print(f"🏔️  Arusha: {Hotel.objects.filter(city='ARU').count()}")
print(f"🏖️  Zanzibar: {Hotel.objects.filter(city='ZAN').count()}")
