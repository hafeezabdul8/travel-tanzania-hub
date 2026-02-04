import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'afcon.settings')
django.setup()

from tourism.models import TouristAttraction, TourPackage

# Sample attractions data
attractions = [
    {
        'name': 'Serengeti National Park',
        'city': 'ARU',
        'category': 'nature',
        'description': 'World-famous national park known for its annual migration of over 1.5 million wildebeest and 250,000 zebras.',
        'location': 'Northern Tanzania',
        'entry_fee': 70,
        'best_time_to_visit': 'June to October',
        'estimated_visit_time': '2-3 days',
    },
    {
        'name': 'Stone Town',
        'city': 'ZAN',
        'category': 'culture',
        'description': 'Historic center of Zanzibar City, a UNESCO World Heritage Site with Arabic architecture.',
        'location': 'Zanzibar City',
        'entry_fee': 10,
        'best_time_to_visit': 'All year',
        'estimated_visit_time': '4-6 hours',
    },
    {
        'name': 'Mount Kilimanjaro',
        'city': 'ARU',
        'category': 'adventure',
        'description': 'Africa\'s highest mountain at 5,895 meters. Popular for hiking and climbing.',
        'location': 'Kilimanjaro Region',
        'entry_fee': 100,
        'best_time_to_visit': 'June to October, December to March',
        'estimated_visit_time': '5-9 days',
    },
    {
        'name': 'Ngorongoro Crater',
        'city': 'ARU',
        'category': 'nature',
        'description': 'World\'s largest inactive volcanic caldera with diverse wildlife including the Big Five.',
        'location': 'Ngorongoro Conservation Area',
        'entry_fee': 80,
        'best_time_to_visit': 'June to September',
        'estimated_visit_time': '1 day',
    },
    {
        'name': 'Bongoyo Island',
        'city': 'DAR',
        'category': 'beach',
        'description': 'Beautiful island perfect for snorkeling, swimming, and beach relaxation.',
        'location': 'Dar es Salaam Marine Reserve',
        'entry_fee': 5,
        'best_time_to_visit': 'Morning',
        'estimated_visit_time': '4-5 hours',
    },
    {
        'name': 'Spice Tours',
        'city': 'ZAN',
        'category': 'food',
        'description': 'Experience Zanzibar\'s spice farms and learn about clove, cinnamon, and nutmeg cultivation.',
        'location': 'Various locations in Zanzibar',
        'entry_fee': 25,
        'best_time_to_visit': 'Morning',
        'estimated_visit_time': '3-4 hours',
    },
]

for data in attractions:
    attraction, created = TouristAttraction.objects.get_or_create(
        name=data['name'],
        defaults=data
    )
    print(f"{'Created' if created else 'Exists'}: {attraction.name}")

print("Tourism data created!")