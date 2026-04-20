# tourism/add_sample_attractions.py
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
from tourism.models import TouristAttraction, AttractionImage, TourPackage
from django.contrib.auth.models import User

def add_attractions():
    """Add sample tourist attractions with images for AFCON 2027"""
    
    print("=" * 60)
    print("Adding Sample Tourist Attractions for AFCON 2027")
    print("=" * 60)
    
    # Get or create admin user
    admin_user, created = User.objects.get_or_create(
        username='admin',
        defaults={'email': 'admin@example.com', 'is_staff': True}
    )
    if created:
        admin_user.set_password('admin123')
        admin_user.save()
        print("✅ Created admin user")
    
    # ============ DAR ES SALAAM ATTRACTIONS ============
    dar_attractions = [
        {
            'name': 'National Museum of Tanzania',
            'city': 'DAR',
            'category': 'culture',
            'description': 'The National Museum houses exhibits on Tanzanian history, culture, and the famous fossils of early humans discovered in Olduvai Gorge.',
            'location': 'Shaaban Robert Street, Dar es Salaam',
            'entry_fee': 10,
            'opening_hours': '9:30 AM - 6:00 PM',
            'best_time_to_visit': 'Morning',
            'estimated_visit_time': '2-3 hours',
            'website': 'https://www.museum.or.tz',
            'contact_phone': '+255 22 211 7508',
            'image_url': 'https://images.unsplash.com/photo-1582555172866-f73bb12c2b2e?w=800',
            'primary_image': True,
        },
        {
            'name': 'Bongoyo Island',
            'city': 'DAR',
            'category': 'beach',
            'description': 'Beautiful uninhabited island with pristine beaches, excellent snorkeling, and relaxing picnic spots. Accessible by boat from Slipway.',
            'location': 'Off the coast of Dar es Salaam',
            'entry_fee': 15,
            'opening_hours': '8:00 AM - 5:00 PM',
            'best_time_to_visit': 'Morning (low tide)',
            'estimated_visit_time': '4-5 hours',
            'website': '',
            'contact_phone': '+255 22 260 0380',
            'image_url': 'https://images.unsplash.com/photo-1507525428034-b723cf961d3e?w=800',
            'primary_image': True,
        },
        {
            'name': 'Kivukoni Fish Market',
            'city': 'DAR',
            'category': 'food',
            'description': 'Vibrant fish market where you can see the daily catch being auctioned and enjoy fresh seafood prepared on the spot.',
            'location': 'Kivukoni Front, Dar es Salaam',
            'entry_fee': None,
            'opening_hours': '5:00 AM - 6:00 PM',
            'best_time_to_visit': 'Early morning (6-8 AM)',
            'estimated_visit_time': '1-2 hours',
            'website': '',
            'contact_phone': '',
            'image_url': 'https://images.unsplash.com/photo-1534088568595-a066f410bcda?w=800',
            'primary_image': True,
        },
        {
            'name': 'Mbudya Island',
            'city': 'DAR',
            'category': 'beach',
            'description': 'Popular island getaway with white sandy beaches, crystal clear waters, and local seafood restaurants.',
            'location': 'Off Kunduchi Beach, Dar es Salaam',
            'entry_fee': 10,
            'opening_hours': '8:00 AM - 5:00 PM',
            'best_time_to_visit': 'Morning',
            'estimated_visit_time': '4-6 hours',
            'website': '',
            'contact_phone': '',
            'image_url': 'https://images.unsplash.com/photo-1507525428034-b723cf961d3e?w=800',
            'primary_image': False,
        },
        {
            'name': 'Village Museum',
            'city': 'DAR',
            'category': 'culture',
            'description': 'Open-air museum showcasing traditional Tanzanian village life with authentic huts, crafts, and cultural performances.',
            'location': 'Kigamboni, Dar es Salaam',
            'entry_fee': 5,
            'opening_hours': '9:00 AM - 5:00 PM',
            'best_time_to_visit': 'Morning',
            'estimated_visit_time': '2 hours',
            'website': '',
            'contact_phone': '+255 22 270 0430',
            'image_url': 'https://images.unsplash.com/photo-1523800503107-5bc3ba2a6f81?w=800',
            'primary_image': False,
        },
        {
            'name': 'Slipway Shopping Center',
            'city': 'DAR',
            'category': 'shopping',
            'description': 'Waterfront shopping and entertainment complex with shops, restaurants, art galleries, and a marina.',
            'location': 'Msasani Peninsula, Dar es Salaam',
            'entry_fee': None,
            'opening_hours': '9:00 AM - 10:00 PM',
            'best_time_to_visit': 'Afternoon/Evening',
            'estimated_visit_time': '2-3 hours',
            'website': 'https://www.slipwaytz.com',
            'contact_phone': '+255 22 260 0893',
            'image_url': 'https://images.unsplash.com/photo-1555529669-e69e7aa0ba9a?w=800',
            'primary_image': False,
        },
    ]
    
    # ============ ARUSHA ATTRACTIONS ============
    arusha_attractions = [
        {
            'name': 'Serengeti National Park',
            'city': 'ARU',
            'category': 'nature',
            'description': 'World-famous wildlife reserve known for the Great Migration of wildebeest and zebra, plus the Big Five.',
            'location': 'Northern Tanzania, near Arusha',
            'entry_fee': 70,
            'opening_hours': '6:00 AM - 6:00 PM',
            'best_time_to_visit': 'June-October (dry season)',
            'estimated_visit_time': '2-5 days',
            'website': 'https://www.tanzaniaparks.go.tz',
            'contact_phone': '+255 27 297 0404',
            'image_url': 'https://images.unsplash.com/photo-1516426122078-c23e76319801?w=800',
            'primary_image': True,
        },
        {
            'name': 'Mount Kilimanjaro',
            'city': 'ARU',
            'category': 'adventure',
            'description': 'Africa\'s highest mountain (5,895m) offering challenging climbs with breathtaking views. Multiple routes available.',
            'location': 'Kilimanjaro Region, near Arusha',
            'entry_fee': 100,
            'opening_hours': '24/7 (climbing permits required)',
            'best_time_to_visit': 'January-March, June-October',
            'estimated_visit_time': '5-9 days',
            'website': 'https://www.kilimanjaro.com',
            'contact_phone': '',
            'image_url': 'https://images.unsplash.com/photo-1492106087820-71f1a00d2b11?w=800',
            'primary_image': True,
        },
        {
            'name': 'Ngorongoro Crater',
            'city': 'ARU',
            'category': 'nature',
            'description': 'UNESCO World Heritage site, the world\'s largest inactive volcanic caldera with incredible wildlife density.',
            'location': 'Ngorongoro Conservation Area, near Arusha',
            'entry_fee': 70,
            'opening_hours': '6:00 AM - 6:00 PM',
            'best_time_to_visit': 'June-October',
            'estimated_visit_time': '1-2 days',
            'website': 'https://www.ngorongorocrater.com',
            'contact_phone': '+255 27 253 6037',
            'image_url': 'https://images.unsplash.com/photo-1547471080-7cc2caa01b98?w=800',
            'primary_image': True,
        },
        {
            'name': 'Arusha National Park',
            'city': 'ARU',
            'category': 'nature',
            'description': 'Small but diverse park featuring Mount Meru, Ngurdoto Crater, and Momella Lakes with flamingos.',
            'location': '25km from Arusha city center',
            'entry_fee': 45,
            'opening_hours': '7:00 AM - 6:00 PM',
            'best_time_to_visit': 'Morning',
            'estimated_visit_time': '4-6 hours',
            'website': '',
            'contact_phone': '+255 27 297 0404',
            'image_url': 'https://images.unsplash.com/photo-1547471080-7cc2caa01b98?w=800',
            'primary_image': False,
        },
        {
            'name': 'Lake Manyara National Park',
            'city': 'ARU',
            'category': 'nature',
            'description': 'Famous for tree-climbing lions, flamingos, and diverse birdlife along the Rift Valley escarpment.',
            'location': '126km from Arusha',
            'entry_fee': 50,
            'opening_hours': '6:30 AM - 6:30 PM',
            'best_time_to_visit': 'Afternoon (bird watching)',
            'estimated_visit_time': '1 day',
            'website': '',
            'contact_phone': '',
            'image_url': 'https://images.unsplash.com/photo-1547471080-7cc2caa01b98?w=800',
            'primary_image': False,
        },
        {
            'name': 'Tarangire National Park',
            'city': 'ARU',
            'category': 'nature',
            'description': 'Known for massive elephant herds, baobab trees, and diverse wildlife including lions and leopards.',
            'location': '120km from Arusha',
            'entry_fee': 50,
            'opening_hours': '6:00 AM - 6:00 PM',
            'best_time_to_visit': 'June-October',
            'estimated_visit_time': '1 day',
            'website': '',
            'contact_phone': '',
            'image_url': 'https://images.unsplash.com/photo-1547471080-7cc2caa01b98?w=800',
            'primary_image': False,
        },
        {
            'name': 'Cultural Heritage Centre',
            'city': 'ARU',
            'category': 'shopping',
            'description': 'Large complex with art galleries, gemstone shops, souvenirs, and Tanzanite jewelry.',
            'location': 'Njiro Road, Arusha',
            'entry_fee': None,
            'opening_hours': '8:30 AM - 6:30 PM',
            'best_time_to_visit': 'Afternoon',
            'estimated_visit_time': '2-3 hours',
            'website': 'https://www.culturalheritage.co.tz',
            'contact_phone': '+255 27 254 8270',
            'image_url': 'https://images.unsplash.com/photo-1555529669-e69e7aa0ba9a?w=800',
            'primary_image': False,
        },
        {
            'name': 'Maasai Market',
            'city': 'ARU',
            'category': 'shopping',
            'description': 'Vibrant market selling traditional Maasai crafts, beadwork, fabrics, and local artwork.',
            'location': 'Clock Tower Area, Arusha',
            'entry_fee': None,
            'opening_hours': '9:00 AM - 6:00 PM',
            'best_time_to_visit': 'Morning',
            'estimated_visit_time': '1-2 hours',
            'website': '',
            'contact_phone': '',
            'image_url': 'https://images.unsplash.com/photo-1555529669-e69e7aa0ba9a?w=800',
            'primary_image': False,
        },
    ]
    
    # ============ ZANZIBAR ATTRACTIONS ============
    zanzibar_attractions = [
        {
            'name': 'Stone Town',
            'city': 'ZAN',
            'category': 'culture',
            'description': 'UNESCO World Heritage site with winding alleys, historic buildings, bazaars, and the former slave market.',
            'location': 'Zanzibar City, Zanzibar',
            'entry_fee': None,
            'opening_hours': '24/7',
            'best_time_to_visit': 'Morning or Late Afternoon',
            'estimated_visit_time': '3-4 hours',
            'website': '',
            'contact_phone': '',
            'image_url': 'https://images.unsplash.com/photo-1510150825674-dcd6b71a8c8b?w=800',
            'primary_image': True,
        },
        {
            'name': 'Nungwi Beach',
            'city': 'ZAN',
            'category': 'beach',
            'description': 'One of Zanzibar\'s most famous beaches with white sand, clear turquoise water, and vibrant nightlife.',
            'location': 'Northern tip of Zanzibar',
            'entry_fee': None,
            'opening_hours': '24/7',
            'best_time_to_visit': 'Morning (low tide)',
            'estimated_visit_time': 'Full day',
            'website': '',
            'contact_phone': '',
            'image_url': 'https://images.unsplash.com/photo-1507525428034-b723cf961d3e?w=800',
            'primary_image': True,
        },
        {
            'name': 'Kendwa Beach',
            'city': 'ZAN',
            'category': 'beach',
            'description': 'Beautiful beach with all-year swimming (no tides), perfect for sunset viewing and water sports.',
            'location': 'Northwest coast of Zanzibar',
            'entry_fee': None,
            'opening_hours': '24/7',
            'best_time_to_visit': 'Afternoon',
            'estimated_visit_time': 'Full day',
            'website': '',
            'contact_phone': '',
            'image_url': 'https://images.unsplash.com/photo-1507525428034-b723cf961d3e?w=800',
            'primary_image': False,
        },
        {
            'name': 'Prison Island (Changuu)',
            'city': 'ZAN',
            'category': 'culture',
            'description': 'Historic island with giant tortoises, former prison ruins, and beautiful snorkeling spots.',
            'location': '5km from Stone Town',
            'entry_fee': 10,
            'opening_hours': '8:00 AM - 5:00 PM',
            'best_time_to_visit': 'Morning',
            'estimated_visit_time': '2-3 hours',
            'website': '',
            'contact_phone': '',
            'image_url': 'https://images.unsplash.com/photo-1507525428034-b723cf961d3e?w=800',
            'primary_image': False,
        },
        {
            'name': 'Spice Farms (Spice Tour)',
            'city': 'ZAN',
            'category': 'food',
            'description': 'Guided tours through spice plantations learning about cloves, nutmeg, cinnamon, vanilla, and tasting tropical fruits.',
            'location': 'Various locations across Zanzibar',
            'entry_fee': 20,
            'opening_hours': '9:00 AM - 4:00 PM',
            'best_time_to_visit': 'Morning',
            'estimated_visit_time': '3-4 hours',
            'website': '',
            'contact_phone': '',
            'image_url': 'https://images.unsplash.com/photo-1595225476474-8756391a2c2a?w=800',
            'primary_image': True,
        },
        {
            'name': 'Jozani Chwaka Bay National Park',
            'city': 'ZAN',
            'category': 'nature',
            'description': 'Home to the rare red colobus monkeys, mangrove forests, and diverse bird species.',
            'location': 'Southern Zanzibar',
            'entry_fee': 12,
            'opening_hours': '7:30 AM - 5:00 PM',
            'best_time_to_visit': 'Morning',
            'estimated_visit_time': '2-3 hours',
            'website': '',
            'contact_phone': '+255 24 223 3030',
            'image_url': 'https://images.unsplash.com/photo-1547471080-7cc2caa01b98?w=800',
            'primary_image': False,
        },
        {
            'name': 'Forodhani Gardens Night Market',
            'city': 'ZAN',
            'category': 'food',
            'description': 'Evening food market offering fresh seafood, Zanzibar pizza, sugarcane juice, and local delicacies.',
            'location': 'Stone Town waterfront',
            'entry_fee': None,
            'opening_hours': '5:00 PM - 10:00 PM',
            'best_time_to_visit': 'Evening',
            'estimated_visit_time': '2 hours',
            'website': '',
            'contact_phone': '',
            'image_url': 'https://images.unsplash.com/photo-1534088568595-a066f410bcda?w=800',
            'primary_image': False,
        },
        {
            'name': 'Mnemba Island',
            'city': 'ZAN',
            'category': 'beach',
            'description': 'Exclusive private island resort with world-class snorkeling, diving, and pristine beaches.',
            'location': 'Northeast coast of Zanzibar',
            'entry_fee': 50,
            'opening_hours': '8:00 AM - 5:00 PM',
            'best_time_to_visit': 'Morning',
            'estimated_visit_time': 'Full day',
            'website': '',
            'contact_phone': '',
            'image_url': 'https://images.unsplash.com/photo-1507525428034-b723cf961d3e?w=800',
            'primary_image': False,
        },
        {
            'name': 'Darajani Market',
            'city': 'ZAN',
            'category': 'shopping',
            'description': 'Busy local market selling spices, fruits, vegetables, meat, fish, and local crafts.',
            'location': 'Stone Town, Zanzibar',
            'entry_fee': None,
            'opening_hours': '6:00 AM - 7:00 PM',
            'best_time_to_visit': 'Morning',
            'estimated_visit_time': '1-2 hours',
            'website': '',
            'contact_phone': '',
            'image_url': 'https://images.unsplash.com/photo-1555529669-e69e7aa0ba9a?w=800',
            'primary_image': False,
        },
    ]
    
    # ============ ALL TANZANIA ATTRACTIONS ============
    all_tanzania_attractions = [
        {
            'name': 'Selous Game Reserve',
            'city': 'ALL',
            'category': 'nature',
            'description': 'UNESCO World Heritage site, one of Africa\'s largest wildlife reserves with boat safaris on Rufiji River.',
            'location': 'Southern Tanzania',
            'entry_fee': 50,
            'opening_hours': '6:00 AM - 6:00 PM',
            'best_time_to_visit': 'June-October',
            'estimated_visit_time': '2-3 days',
            'website': '',
            'contact_phone': '',
            'image_url': 'https://images.unsplash.com/photo-1516426122078-c23e76319801?w=800',
            'primary_image': True,
        },
        {
            'name': 'Mahale Mountains National Park',
            'city': 'ALL',
            'category': 'nature',
            'description': 'Home to wild chimpanzees, with pristine beaches on Lake Tanganyika and excellent hiking.',
            'location': 'Western Tanzania',
            'entry_fee': 80,
            'opening_hours': '6:00 AM - 6:00 PM',
            'best_time_to_visit': 'May-October',
            'estimated_visit_time': '3-4 days',
            'website': '',
            'contact_phone': '',
            'image_url': 'https://images.unsplash.com/photo-1547471080-7cc2caa01b98?w=800',
            'primary_image': False,
        },
    ]
    
    # Combine all attractions
    all_attractions = dar_attractions + arusha_attractions + zanzibar_attractions + all_tanzania_attractions
    
    attractions_created = 0
    attractions_existing = 0
    
    print("\n📋 Adding attractions...\n")
    
    for att_data in all_attractions:
        attraction, created = TouristAttraction.objects.get_or_create(
            name=att_data['name'],
            defaults={
                'city': att_data['city'],
                'category': att_data['category'],
                'description': att_data['description'],
                'location': att_data['location'],
                'entry_fee': Decimal(str(att_data['entry_fee'])) if att_data['entry_fee'] else None,
                'opening_hours': att_data['opening_hours'],
                'best_time_to_visit': att_data['best_time_to_visit'],
                'estimated_visit_time': att_data['estimated_visit_time'],
                'website': att_data['website'],
                'contact_phone': att_data['contact_phone'],
                'partner': admin_user,
            }
        )
        
        if created:
            attractions_created += 1
            print(f"✅ Created: {attraction.name} - {attraction.get_city_display()} - {attraction.get_category_display()}")
            
            # Add image for this attraction
            image_url = att_data['image_url']
            is_primary = att_data.get('primary_image', True)
            
            AttractionImage.objects.get_or_create(
                attraction=attraction,
                image_url=image_url,
                defaults={
                    'caption': f"Main image of {attraction.name}",
                    'is_primary': is_primary
                }
            )
            print(f"   └─ Added image: {image_url[:50]}...")
        else:
            attractions_existing += 1
            print(f"⚠️ Already exists: {attraction.name}")
    
    # ============ CREATE TOUR PACKAGES ============
    print("\n📋 Creating tour packages...\n")
    
    tour_packages = [
        # Serengeti packages
        {
            'attraction_name': 'Serengeti National Park',
            'name': 'Serengeti Classic Safari',
            'description': '3-day classic safari experience with game drives in Serengeti and Ngorongoro Crater.',
            'duration': '3 days',
            'price': 450,
            'includes': 'Park fees, Accommodation, Meals, Professional guide, 4x4 vehicle',
            'excludes': 'International flights, Visa, Tips, Travel insurance',
            'is_featured': True,
            'supplier_name': 'Serengeti Adventures',
            'supplier_contact': '+255 27 254 8900',
        },
        {
            'attraction_name': 'Serengeti National Park',
            'name': 'Serengeti Luxury Safari',
            'description': '5-day luxury safari with hot air balloon ride and luxury lodge accommodation.',
            'duration': '5 days',
            'price': 1200,
            'includes': 'Park fees, Luxury lodges, All meals, Balloon safari, Airport transfers',
            'excludes': 'International flights, Visa, Tips',
            'is_featured': True,
            'supplier_name': 'Luxury Safari Tanzania',
            'supplier_contact': '+255 27 254 8911',
        },
        # Kilimanjaro packages
        {
            'attraction_name': 'Mount Kilimanjaro',
            'name': 'Kilimanjaro Machame Route',
            'description': '6-day Machame Route (Whiskey Route) - most scenic route with great acclimatization.',
            'duration': '6 days',
            'price': 1500,
            'includes': 'Park fees, Guide and porters, Camping equipment, Meals, Rescue fees',
            'excludes': 'Gear rental, Tips, Flights',
            'is_featured': True,
            'supplier_name': 'Kilimanjaro Experts',
            'supplier_contact': '+255 27 254 8922',
        },
        {
            'attraction_name': 'Mount Kilimanjaro',
            'name': 'Kilimanjaro Marangu Route',
            'description': '5-day Marangu Route (Coca-Cola Route) - easier with hut accommodation.',
            'duration': '5 days',
            'price': 1200,
            'includes': 'Park fees, Guide and porters, Hut accommodation, Meals',
            'excludes': 'Gear rental, Tips, Flights',
            'is_featured': False,
            'supplier_name': 'Kilimanjaro Experts',
            'supplier_contact': '+255 27 254 8922',
        },
        # Zanzibar packages
        {
            'attraction_name': 'Stone Town',
            'name': 'Stone Town Walking Tour',
            'description': 'Guided walking tour through historic Stone Town, visiting key landmarks and markets.',
            'duration': '3 hours',
            'price': 25,
            'includes': 'Professional guide, Entrance fees, Bottled water',
            'excludes': 'Lunch, Souvenirs',
            'is_featured': True,
            'supplier_name': 'Zanzibar Tours',
            'supplier_contact': '+255 24 223 8933',
        },
        {
            'attraction_name': 'Spice Farms (Spice Tour)',
            'name': 'Zanzibar Spice Tour',
            'description': 'Experience Zanzibar\'s spice heritage with local guide, tasting fresh fruits and spices.',
            'duration': '4 hours',
            'price': 35,
            'includes': 'Spice farm entry, Guide, Fruit tasting, Spice purchase opportunity',
            'excludes': 'Transport to farm, Tips',
            'is_featured': True,
            'supplier_name': 'Zanzibar Spice Tours',
            'supplier_contact': '+255 24 223 8944',
        },
        # Ngorongoro packages
        {
            'attraction_name': 'Ngorongoro Crater',
            'name': 'Ngorongoro Crater Day Trip',
            'description': 'Full day game drive in the world-famous Ngorongoro Crater with picnic lunch.',
            'duration': '1 day',
            'price': 250,
            'includes': 'Park fees, Vehicle, Guide, Picnic lunch',
            'excludes': 'Accommodation, Tips',
            'is_featured': False,
            'supplier_name': 'Ngorongoro Safaris',
            'supplier_contact': '+255 27 254 8955',
        },
    ]
    
    packages_created = 0
    packages_existing = 0
    
    for package_data in tour_packages:
        try:
            attraction = TouristAttraction.objects.get(name=package_data['attraction_name'])
            package, created = TourPackage.objects.get_or_create(
                name=package_data['name'],
                attraction=attraction,
                defaults={
                    'description': package_data['description'],
                    'duration': package_data['duration'],
                    'price': Decimal(str(package_data['price'])),
                    'includes': package_data['includes'],
                    'excludes': package_data['excludes'],
                    'is_featured': package_data['is_featured'],
                    'supplier_name': package_data['supplier_name'],
                    'supplier_contact': package_data['supplier_contact'],
                    'partner': admin_user,
                }
            )
            if created:
                packages_created += 1
                print(f"✅ Created tour package: {package.name} - ${package.price}")
            else:
                packages_existing += 1
                print(f"⚠️ Already exists: {package.name}")
        except TouristAttraction.DoesNotExist:
            print(f"⚠️ Attraction not found for package: {package_data['attraction_name']}")
    
    # Print summary
    print("\n" + "=" * 60)
    print("TOURIST ATTRACTIONS SUMMARY")
    print("=" * 60)
    print(f"✅ New attractions created: {attractions_created}")
    print(f"⚠️ Existing attractions skipped: {attractions_existing}")
    print(f"🏛️ Total attractions: {TouristAttraction.objects.count()}")
    print(f"   - Dar es Salaam: {TouristAttraction.objects.filter(city='DAR').count()}")
    print(f"   - Arusha: {TouristAttraction.objects.filter(city='ARU').count()}")
    print(f"   - Zanzibar: {TouristAttraction.objects.filter(city='ZAN').count()}")
    print(f"   - All Tanzania: {TouristAttraction.objects.filter(city='ALL').count()}")
    print(f"📸 Total images: {AttractionImage.objects.count()}")
    print(f"🎒 Tour packages created: {packages_created}")
    print(f"🎒 Total tour packages: {TourPackage.objects.count()}")
    print("=" * 60)
    print("\n🎉 All attractions added successfully!")
    print("\n📸 Images are from Unsplash and will display on the tourism page.")

if __name__ == "__main__":
    add_attractions()