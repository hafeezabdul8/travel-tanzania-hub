# city/add_city_data.py
import os
import sys
import django

sys.path.append('/home/feezman/afcon_project')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'afcon.settings')
django.setup()

from city.models import City

def add_cities():
    print("=" * 60)
    print("Adding City Data")
    print("=" * 60)
    
    cities_data = [
        {
            'name': 'Dar es Salaam',
            'code': 'DAR',
            'slug': 'dar-es-salaam',
            'tagline': 'The Vibrant Commercial Capital',
            'description': 'Dar es Salaam, meaning "Haven of Peace" in Arabic, is Tanzania\'s largest city and economic hub. This bustling metropolis combines modern skyscrapers with historic architecture, beautiful beaches, and a lively waterfront. As the main host city for AFCON 2027, Dar es Salaam offers visitors a perfect blend of business and leisure.',
            'history': 'Dar es Salaam was founded in 1862 by Sultan Majid bin Said of Zanzibar. It served as the capital of German East Africa and later Tanganyika before the capital was moved to Dodoma in 1974. Today, it remains the country\'s most important commercial center.',
            'culture': 'The city is a melting pot of cultures including Swahili, Arab, Indian, and European influences. The National Museum, Village Museum, and various art galleries showcase Tanzania\'s rich heritage.',
            'hero_image': 'https://images.unsplash.com/photo-1593701461760-2f9d5e48f8f4?w=1200',
            'gallery_images': [
                'https://images.unsplash.com/photo-1593701461760-2f9d5e48f8f4?w=800',
                'https://images.unsplash.com/photo-1566073771259-6a8506099945?w=800',
                'https://images.unsplash.com/photo-1582719508461-905c673771fd?w=800',
            ],
            'population': '6.7 million',
            'area': '1,590 km²',
            'language': 'Swahili, English',
            'stadium_name': 'Benjamin Mkapa National Stadium',
            'stadium_capacity': 60000,
            'stadium_image': 'https://images.unsplash.com/photo-1595435934247-5d33b7f92c70?w=800',
            'matches_count': 20,
            'best_time_to_visit': 'June to October (dry season)',
            'average_temperature': '28°C (82°F) during AFCON in January',
            'weather_info': 'January is warm and humid with occasional short rains. Average high 32°C, low 24°C.',
            'how_to_get_there': 'Julius Nyerere International Airport (DAR) connects to major international cities. Domestic flights, buses, and trains available.',
            'getting_around': 'Dala-dala (minibuses), taxis, ride-hailing apps (Uber/Bolt), and bajaj (tuk-tuks).',
            'airport_info': 'Julius Nyerere International Airport - 12km from city center. Taxi fare $20-30.',
            'famous_for': 'Beaches, nightlife, fish market, Kariakoo Market, Tinga Tinga art',
            'local_cuisine': 'Zanzibar pizza, mishkaki (grilled meat), ugali, fresh seafood, pilau rice',
            'popular_activities': [
                'Visit National Museum',
                'Relax at Coco Beach',
                'Explore Kariakoo Market',
                'Boat trip to Bongoyo Island',
                'Enjoy sunset at The Waterfront',
                'Tinga Tinga art shopping'
            ],
            'latitude': -6.7924,
            'longitude': 39.2083,
        },
        {
            'name': 'Arusha',
            'code': 'ARU',
            'slug': 'arusha',
            'tagline': 'The Safari Capital of Tanzania',
            'description': 'Arusha is the gateway to Tanzania\'s northern safari circuit, including the world-famous Serengeti, Ngorongoro Crater, and Mount Kilimanjaro. This charming city offers a perfect blend of urban convenience and natural wonders, making it an ideal base for both AFCON matches and safari adventures.',
            'history': 'Arusha was established as a German military outpost in 1900. It gained prominence as a trading center and is now the headquarters of the East African Community.',
            'culture': 'The city is a cultural crossroads where Maasai traditions meet modern Tanzanian life. Visit the Cultural Heritage Centre and Maasai markets for authentic experiences.',
            'hero_image': 'https://images.unsplash.com/photo-1516026672322-bc52d61a55d5?w=1200',
            'gallery_images': [
                'https://images.unsplash.com/photo-1516026672322-bc52d61a55d5?w=800',
                'https://images.unsplash.com/photo-1547471080-7cc2caa01b98?w=800',
                'https://images.unsplash.com/photo-1508098682722-e99c43a406b2?w=800',
            ],
            'population': '1.5 million',
            'area': '1,280 km²',
            'language': 'Swahili, English, Maasai',
            'stadium_name': 'Arusha Stadium',
            'stadium_capacity': 30000,
            'stadium_image': 'https://images.unsplash.com/photo-1508098682722-e99c43a406b2?w=800',
            'matches_count': 12,
            'best_time_to_visit': 'June to October (dry season for safaris)',
            'average_temperature': '22°C (72°F) during AFCON in January',
            'weather_info': 'January is warm with afternoon showers possible. Average high 28°C, low 15°C.',
            'how_to_get_there': 'Kilimanjaro International Airport (JRO) or Arusha Airport (ARK). Daily flights from Dar es Salaam and Zanzibar.',
            'getting_around': 'Taxis, dala-dala, and tour operator vehicles for safaris.',
            'airport_info': 'Kilimanjaro International Airport - 50km from city center. Shuttle $30-50.',
            'famous_for': 'Serengeti safaris, Mount Kilimanjaro, Ngorongoro Crater, coffee plantations',
            'local_cuisine': 'Nyama choma (grilled meat), ugali, local stews, fresh coffee',
            'popular_activities': [
                'Serengeti Safari',
                'Ngorongoro Crater Tour',
                'Mount Kilimanjaro Trek',
                'Visit Maasai Village',
                'Coffee Plantation Tour',
                'Arusha National Park'
            ],
            'latitude': -3.3667,
            'longitude': 36.6833,
        },
        {
            'name': 'Zanzibar',
            'code': 'ZAN',
            'slug': 'zanzibar',
            'tagline': 'The Spice Island Paradise',
            'description': 'Zanzibar, also known as the Spice Island, is a semi-autonomous archipelago off the coast of Tanzania. Famous for its stunning beaches, historic Stone Town, and rich spice heritage, Zanzibar offers a unique blend of African, Arab, Indian, and European influences.',
            'history': 'Zanzibar was a major trading hub for spices and slaves, controlled by Omani Arabs for centuries. It became a British protectorate in 1890 and joined Tanganyika to form Tanzania in 1964.',
            'culture': 'Stone Town\'s winding alleys reveal a fascinating history of sultans, explorers, and traders. The culture is a unique fusion of Swahili, Arabic, Indian, and European elements.',
            'hero_image': 'https://images.unsplash.com/photo-1563492065599-3520f775eeed?w=1200',
            'gallery_images': [
                'https://images.unsplash.com/photo-1563492065599-3520f775eeed?w=800',
                'https://images.unsplash.com/photo-1507525428034-b723cf961d3e?w=800',
                'https://images.unsplash.com/photo-1510150825674-dcd6b71a8c8b?w=800',
            ],
            'population': '1.3 million',
            'area': '2,461 km²',
            'language': 'Swahili, English, Arabic',
            'stadium_name': 'Amaan Stadium',
            'stadium_capacity': 25000,
            'stadium_image': 'https://images.unsplash.com/photo-1563492065599-3520f775eeed?w=800',
            'matches_count': 10,
            'best_time_to_visit': 'June to October (dry season)',
            'average_temperature': '30°C (86°F) during AFCON in January',
            'weather_info': 'January is hot and humid with possible short rains. Average high 32°C, low 24°C.',
            'how_to_get_there': 'Abeid Amani Karume International Airport (ZNZ). Daily flights from Dar es Salaam (30 min) and international destinations.',
            'getting_around': 'Taxis, dala-dala, walking in Stone Town, boat tours',
            'airport_info': 'Abeid Amani Karume International Airport - 8km from Stone Town. Taxi $10-15.',
            'famous_for': 'Stone Town (UNESCO), spice tours, pristine beaches, coral reefs',
            'local_cuisine': 'Zanzibar pizza, biryani, fresh seafood, urojo soup, spice tea',
            'popular_activities': [
                'Stone Town Walking Tour',
                'Spice Farm Tour',
                'Beach Hopping (Nungwi, Kendwa)',
                'Prison Island Visit',
                'Snorkeling & Diving',
                'Sunset Dhow Cruise'
            ],
            'latitude': -6.1659,
            'longitude': 39.2026,
        },
    ]
    
    for data in cities_data:
        city, created = City.objects.get_or_create(
            code=data['code'],
            defaults=data
        )
        if created:
            print(f"✅ Created: {city.name}")
        else:
            print(f"⚠️ Already exists: {city.name}")
    
    print("\n🎉 All cities added successfully!")

if __name__ == "__main__":
    add_cities()