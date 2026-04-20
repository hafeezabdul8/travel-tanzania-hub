# football/populate_all_data.py
import os
import sys
import django
from datetime import date, time, datetime, timedelta
from decimal import Decimal

sys.path.append('/home/feezman/afcon_project')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'afcon.settings')
django.setup()

from football.models import (
    Team, Player, Stadium, Match, Goal, GroupStanding, 
    MatchNews, NewsComment, Ticket, UserPrediction, MatchAlert
)
from django.contrib.auth.models import User
from hotels.models import Hotel

def clear_existing_data():
    """Clear all existing football data"""
    print("\n🗑️ Clearing existing data...")
    NewsComment.objects.all().delete()
    MatchAlert.objects.all().delete()
    UserPrediction.objects.all().delete()
    Ticket.objects.all().delete()
    Goal.objects.all().delete()
    MatchNews.objects.all().delete()
    GroupStanding.objects.all().delete()
    Match.objects.all().delete()
    Player.objects.all().delete()
    Team.objects.all().delete()
    Stadium.objects.all().delete()
    print("✅ Existing data cleared")

def create_stadiums():
    """Create stadiums with image URLs"""
    print("\n🏟️ Creating Stadiums...")
    
    stadiums_data = [
        {
            'name': 'Benjamin Mkapa National Stadium',
            'city': 'Dar es Salaam',
            'capacity': 60000,
            'address': 'Taifa Road, Dar es Salaam, Tanzania',
            'latitude': -6.8500,
            'longitude': 39.2933,
            'description': 'The main stadium for AFCON 2027, hosting the opening match and final. Features modern facilities and excellent views.',
            'has_floodlights': True,
            'pitch_type': 'natural',
            'main_image_url': 'https://images.unsplash.com/photo-1595435934247-5d33b7f92c70?w=800',
            'aerial_image_url': 'https://images.unsplash.com/photo-1577223625816-7546f13df25d?w=800',
            'night_image_url': 'https://images.unsplash.com/photo-1522778119026-d647f0596c20?w=800',
            'pitch_image_url': 'https://images.unsplash.com/photo-1459865264687-287dbf7878f4?w=800',
            'stands_image_url': 'https://images.unsplash.com/photo-1522778119026-d647f0596c20?w=800',
            'facilities': ['Floodlights', 'VIP Lounges', 'Press Box', 'Medical Center', 'Parking for 2000 cars', 'WiFi', 'Food Courts'],
            'transport_info': 'Located in Kivukoni area. Accessible by taxi and public buses. Special AFCON shuttle buses available.'
        },
        {
            'name': 'Arusha Stadium',
            'city': 'Arusha',
            'capacity': 30000,
            'address': 'Sokoine Road, Arusha, Tanzania',
            'latitude': -3.3667,
            'longitude': 36.6833,
            'description': 'Modern stadium in the safari capital, hosting group stage matches. Beautiful views of Mount Meru.',
            'has_floodlights': True,
            'pitch_type': 'natural',
            'main_image_url': 'https://images.unsplash.com/photo-1516026672322-bc52d61a55d5?w=800',
            'aerial_image_url': 'https://images.unsplash.com/photo-1508098682722-e99c43a406b2?w=800',
            'night_image_url': 'https://images.unsplash.com/photo-1508098682722-e99c43a406b2?w=800',
            'pitch_image_url': 'https://images.unsplash.com/photo-1459865264687-287dbf7878f4?w=800',
            'facilities': ['Floodlights', 'VIP Area', 'Press Box', 'Medical Room', 'Parking for 800 cars', 'WiFi'],
            'transport_info': 'Located in city center. Walking distance from many hotels.'
        },
        {
            'name': 'Amaan Stadium',
            'city': 'Zanzibar',
            'capacity': 25000,
            'address': 'Zanzibar City, Zanzibar, Tanzania',
            'latitude': -6.1659,
            'longitude': 39.2026,
            'description': 'Coastal stadium with beautiful ocean views, hosting group stage matches.',
            'has_floodlights': True,
            'pitch_type': 'natural',
            'main_image_url': 'https://images.unsplash.com/photo-1563492065599-3520f775eeed?w=800',
            'aerial_image_url': 'https://images.unsplash.com/photo-1571896349842-33c89424de2d?w=800',
            'night_image_url': 'https://images.unsplash.com/photo-1571896349842-33c89424de2d?w=800',
            'pitch_image_url': 'https://images.unsplash.com/photo-1459865264687-287dbf7878f4?w=800',
            'facilities': ['Floodlights', 'VIP Seating', 'Press Area', 'First Aid Station', 'Parking for 500 cars'],
            'transport_info': 'Located in Zanzibar City. Ferry terminal 15 minutes away.'
        },
    ]
    
    stadiums = {}
    for data in stadiums_data:
        stadium, created = Stadium.objects.get_or_create(
            name=data['name'],
            defaults={
                'city': data['city'],
                'capacity': data['capacity'],
                'address': data['address'],
                'latitude': data['latitude'],
                'longitude': data['longitude'],
                'description': data['description'],
                'has_floodlights': data['has_floodlights'],
                'pitch_type': data['pitch_type'],
                'main_image_url': data.get('main_image_url'),
                'aerial_image_url': data.get('aerial_image_url'),
                'night_image_url': data.get('night_image_url'),
                'pitch_image_url': data.get('pitch_image_url'),
                'stands_image_url': data.get('stands_image_url'),
                'facilities': data['facilities'],
                'transport_info': data['transport_info'],
            }
        )
        stadiums[data['name']] = stadium
        print(f"   ✅ Created: {stadium.name}")
    
    return stadiums

def create_teams(stadiums):
    """Create teams with image URLs"""
    print("\n⚽ Creating Teams...")
    
    teams_data = [
        # Group A
        {'name': 'Tanzania', 'short_name': 'TAN', 'country_code': 'tz', 'group': 'A', 'fifa_ranking': 120, 'coach': 'Adel Amrouche', 
         'flag_url': 'https://flagcdn.com/w320/tz.png', 'logo_url': 'https://flagcdn.com/w320/tz.png',
         'team_photo_url': 'https://images.unsplash.com/photo-1522778119026-d647f0596c20?w=800',
         'coach_photo_url': 'https://randomuser.me/api/portraits/men/32.jpg',
         'achievements': 'AFCON 1980 Champions', 'stadium': stadiums['Benjamin Mkapa National Stadium']},
        
        {'name': 'Nigeria', 'short_name': 'NGA', 'country_code': 'ng', 'group': 'A', 'fifa_ranking': 42, 'coach': 'Jose Peseiro',
         'flag_url': 'https://flagcdn.com/w320/ng.png', 'logo_url': 'https://flagcdn.com/w320/ng.png',
         'team_photo_url': 'https://images.unsplash.com/photo-1522778119026-d647f0596c20?w=800',
         'achievements': '3x AFCON Champions (1980, 1994, 2013)'},
        
        {'name': 'Egypt', 'short_name': 'EGY', 'country_code': 'eg', 'group': 'A', 'fifa_ranking': 35, 'coach': 'Rui Vitoria',
         'flag_url': 'https://flagcdn.com/w320/eg.png', 'logo_url': 'https://flagcdn.com/w320/eg.png',
         'team_photo_url': 'https://images.unsplash.com/photo-1522778119026-d647f0596c20?w=800',
         'achievements': '7x AFCON Champions (Most titles)'},
        
        {'name': 'Morocco', 'short_name': 'MAR', 'country_code': 'ma', 'group': 'A', 'fifa_ranking': 13, 'coach': 'Walid Regragui',
         'flag_url': 'https://flagcdn.com/w320/ma.png', 'logo_url': 'https://flagcdn.com/w320/ma.png',
         'team_photo_url': 'https://images.unsplash.com/photo-1522778119026-d647f0596c20?w=800',
         'achievements': 'AFCON 1976 Champions'},
        
        # Group B
        {'name': 'Senegal', 'short_name': 'SEN', 'country_code': 'sn', 'group': 'B', 'fifa_ranking': 20, 'coach': 'Aliou Cissé',
         'flag_url': 'https://flagcdn.com/w320/sn.png', 'logo_url': 'https://flagcdn.com/w320/sn.png',
         'achievements': 'AFCON 2021 Champions'},
        
        {'name': 'Cameroon', 'short_name': 'CMR', 'country_code': 'cm', 'group': 'B', 'fifa_ranking': 45, 'coach': 'Rigobert Song',
         'flag_url': 'https://flagcdn.com/w320/cm.png', 'logo_url': 'https://flagcdn.com/w320/cm.png',
         'achievements': '5x AFCON Champions'},
        
        {'name': 'Ghana', 'short_name': 'GHA', 'country_code': 'gh', 'group': 'B', 'fifa_ranking': 60, 'coach': 'Chris Hughton',
         'flag_url': 'https://flagcdn.com/w320/gh.png', 'logo_url': 'https://flagcdn.com/w320/gh.png',
         'achievements': '4x AFCON Champions'},
        
        {'name': 'Ivory Coast', 'short_name': 'CIV', 'country_code': 'ci', 'group': 'B', 'fifa_ranking': 55, 'coach': 'Jean-Louis Gasset',
         'flag_url': 'https://flagcdn.com/w320/ci.png', 'logo_url': 'https://flagcdn.com/w320/ci.png',
         'achievements': '2x AFCON Champions (1992, 2015)'},
        
        # Group C
        {'name': 'Algeria', 'short_name': 'ALG', 'country_code': 'dz', 'group': 'C', 'fifa_ranking': 40, 'coach': 'Djamel Belmadi',
         'flag_url': 'https://flagcdn.com/w320/dz.png', 'logo_url': 'https://flagcdn.com/w320/dz.png',
         'achievements': 'AFCON 2019 Champions'},
        
        {'name': 'Tunisia', 'short_name': 'TUN', 'country_code': 'tn', 'group': 'C', 'fifa_ranking': 32, 'coach': 'Jalel Kadri',
         'flag_url': 'https://flagcdn.com/w320/tn.png', 'logo_url': 'https://flagcdn.com/w320/tn.png',
         'achievements': 'AFCON 2004 Champions'},
        
        {'name': 'South Africa', 'short_name': 'RSA', 'country_code': 'za', 'group': 'C', 'fifa_ranking': 66, 'coach': 'Hugo Broos',
         'flag_url': 'https://flagcdn.com/w320/za.png', 'logo_url': 'https://flagcdn.com/w320/za.png',
         'achievements': 'AFCON 1996 Champions'},
        
        {'name': 'Mali', 'short_name': 'MLI', 'country_code': 'ml', 'group': 'C', 'fifa_ranking': 50, 'coach': 'Eric Chelle',
         'flag_url': 'https://flagcdn.com/w320/ml.png', 'logo_url': 'https://flagcdn.com/w320/ml.png',
         'achievements': 'Best: Runners-up 1972'},
        
        # Group D
        {'name': 'DR Congo', 'short_name': 'COD', 'country_code': 'cd', 'group': 'D', 'fifa_ranking': 68, 'coach': 'Sébastien Desabre',
         'flag_url': 'https://flagcdn.com/w320/cd.png', 'logo_url': 'https://flagcdn.com/w320/cd.png',
         'achievements': '2x AFCON Champions (1968, 1974)'},
        
        {'name': 'Burkina Faso', 'short_name': 'BFA', 'country_code': 'bf', 'group': 'D', 'fifa_ranking': 58, 'coach': 'Hubert Velud',
         'flag_url': 'https://flagcdn.com/w320/bf.png', 'logo_url': 'https://flagcdn.com/w320/bf.png',
         'achievements': 'Best: Runners-up 2013'},
        
        {'name': 'Guinea', 'short_name': 'GUI', 'country_code': 'gn', 'group': 'D', 'fifa_ranking': 80, 'coach': 'Kaba Diawara',
         'flag_url': 'https://flagcdn.com/w320/gn.png', 'logo_url': 'https://flagcdn.com/w320/gn.png',
         'achievements': 'Best: Runners-up 1976'},
        
        {'name': 'Equatorial Guinea', 'short_name': 'EQG', 'country_code': 'gq', 'group': 'D', 'fifa_ranking': 95, 'coach': 'Juan Micha',
         'flag_url': 'https://flagcdn.com/w320/gq.png', 'logo_url': 'https://flagcdn.com/w320/gq.png',
         'achievements': 'Best: 4th place 2015'},
        
        # Group E
        {'name': 'Zambia', 'short_name': 'ZAM', 'country_code': 'zm', 'group': 'E', 'fifa_ranking': 88, 'coach': 'Avram Grant',
         'flag_url': 'https://flagcdn.com/w320/zm.png', 'logo_url': 'https://flagcdn.com/w320/zm.png',
         'achievements': 'AFCON 2012 Champions'},
        
        {'name': 'Angola', 'short_name': 'ANG', 'country_code': 'ao', 'group': 'E', 'fifa_ranking': 85, 'coach': 'Pedro Gonçalves',
         'flag_url': 'https://flagcdn.com/w320/ao.png', 'logo_url': 'https://flagcdn.com/w320/ao.png',
         'achievements': 'Best: Quarterfinals 2008, 2010'},
        
        {'name': 'Mauritania', 'short_name': 'MTN', 'country_code': 'mr', 'group': 'E', 'fifa_ranking': 105, 'coach': 'Amir Abdou',
         'flag_url': 'https://flagcdn.com/w320/mr.png', 'logo_url': 'https://flagcdn.com/w320/mr.png',
         'achievements': 'Best: Round of 16 2019'},
        
        {'name': 'Sudan', 'short_name': 'SUD', 'country_code': 'sd', 'group': 'E', 'fifa_ranking': 128, 'coach': 'Burhan Tia',
         'flag_url': 'https://flagcdn.com/w320/sd.png', 'logo_url': 'https://flagcdn.com/w320/sd.png',
         'achievements': 'AFCON 1970 Champions'},
        
        # Group F
        {'name': 'Cape Verde', 'short_name': 'CPV', 'country_code': 'cv', 'group': 'F', 'fifa_ranking': 72, 'coach': 'Bubista',
         'flag_url': 'https://flagcdn.com/w320/cv.png', 'logo_url': 'https://flagcdn.com/w320/cv.png',
         'achievements': 'Best: Quarterfinals 2013, 2021'},
        
        {'name': 'Zimbabwe', 'short_name': 'ZIM', 'country_code': 'zw', 'group': 'F', 'fifa_ranking': 125, 'coach': 'Baltemar Brito',
         'flag_url': 'https://flagcdn.com/w320/zw.png', 'logo_url': 'https://flagcdn.com/w320/zw.png',
         'achievements': 'Best: Group stage 2004, 2006, 2017, 2019'},
        
        {'name': 'Benin', 'short_name': 'BEN', 'country_code': 'bj', 'group': 'F', 'fifa_ranking': 98, 'coach': 'Gernot Rohr',
         'flag_url': 'https://flagcdn.com/w320/bj.png', 'logo_url': 'https://flagcdn.com/w320/bj.png',
         'achievements': 'Best: Quarterfinals 2019'},
        
        {'name': 'Mozambique', 'short_name': 'MOZ', 'country_code': 'mz', 'group': 'F', 'fifa_ranking': 115, 'coach': 'Chiquinho Conde',
         'flag_url': 'https://flagcdn.com/w320/mz.png', 'logo_url': 'https://flagcdn.com/w320/mz.png',
         'achievements': 'Best: Group stage 1998, 2010'},
    ]
    
    teams = {}
    for data in teams_data:
        team, created = Team.objects.get_or_create(
            name=data['name'],
            defaults={
                'short_name': data['short_name'],
                'country_code': data['country_code'],
                'group': data['group'],
                'fifa_ranking': data['fifa_ranking'],
                'coach': data['coach'],
                'stadium': data.get('stadium'),
                'flag_url': data.get('flag_url'),
                'logo_url': data.get('logo_url'),
                'team_photo_url': data.get('team_photo_url'),
                'coach_photo_url': data.get('coach_photo_url'),
                'achievements': data.get('achievements', ''),
            }
        )
        teams[data['short_name']] = team
        print(f"   ✅ Created: {team.name} (Group {team.group})")
    
    return teams

def create_players(teams):
    """Create players with image URLs"""
    print("\n👤 Creating Players...")
    
    players_data = [
        # Tanzania Players
        {'team': 'TAN', 'name': 'Aishi Manula', 'jersey': 1, 'position': 'GK', 'dob': date(1995, 9, 13), 'club': 'Simba SC', 
         'photo_url': 'https://randomuser.me/api/portraits/men/1.jpg', 'action_photo_url': 'https://randomuser.me/api/portraits/men/1.jpg'},
        {'team': 'TAN', 'name': 'Mudathir Yahya', 'jersey': 2, 'position': 'MF', 'dob': date(1996, 5, 6), 'club': 'Young Africans',
         'photo_url': 'https://randomuser.me/api/portraits/men/2.jpg'},
        {'team': 'TAN', 'name': 'Himid Mao', 'jersey': 8, 'position': 'MF', 'dob': date(1992, 11, 15), 'club': 'Young Africans',
         'photo_url': 'https://randomuser.me/api/portraits/men/3.jpg'},
        {'team': 'TAN', 'name': 'Simon Msuva', 'jersey': 11, 'position': 'FW', 'dob': date(1993, 10, 2), 'club': 'Al-Hilal',
         'photo_url': 'https://randomuser.me/api/portraits/men/4.jpg'},
        {'team': 'TAN', 'name': 'Kelvin John', 'jersey': 10, 'position': 'FW', 'dob': date(2003, 1, 26), 'club': 'Young Africans',
         'photo_url': 'https://randomuser.me/api/portraits/men/5.jpg'},
        
        # Nigeria Players
        {'team': 'NGA', 'name': 'Victor Osimhen', 'jersey': 9, 'position': 'FW', 'dob': date(1998, 12, 29), 'club': 'Napoli',
         'photo_url': 'https://randomuser.me/api/portraits/men/10.jpg', 'action_photo_url': 'https://randomuser.me/api/portraits/men/10.jpg'},
        {'team': 'NGA', 'name': 'Ahmed Musa', 'jersey': 7, 'position': 'FW', 'dob': date(1992, 10, 14), 'club': 'Sivasspor',
         'photo_url': 'https://randomuser.me/api/portraits/men/11.jpg'},
        {'team': 'NGA', 'name': 'Wilfred Ndidi', 'jersey': 4, 'position': 'MF', 'dob': date(1996, 12, 16), 'club': 'Leicester City',
         'photo_url': 'https://randomuser.me/api/portraits/men/12.jpg'},
        {'team': 'NGA', 'name': 'Alex Iwobi', 'jersey': 18, 'position': 'MF', 'dob': date(1996, 5, 3), 'club': 'Fulham',
         'photo_url': 'https://randomuser.me/api/portraits/men/13.jpg'},
        
        # Egypt Players
        {'team': 'EGY', 'name': 'Mohamed Salah', 'jersey': 10, 'position': 'FW', 'dob': date(1992, 6, 15), 'club': 'Liverpool',
         'photo_url': 'https://randomuser.me/api/portraits/men/20.jpg', 'action_photo_url': 'https://randomuser.me/api/portraits/men/20.jpg'},
        {'team': 'EGY', 'name': 'Mohamed Elneny', 'jersey': 8, 'position': 'MF', 'dob': date(1992, 7, 11), 'club': 'Arsenal',
         'photo_url': 'https://randomuser.me/api/portraits/men/21.jpg'},
        
        # Senegal Players
        {'team': 'SEN', 'name': 'Sadio Mané', 'jersey': 10, 'position': 'FW', 'dob': date(1992, 4, 10), 'club': 'Al-Nassr',
         'photo_url': 'https://randomuser.me/api/portraits/men/30.jpg', 'action_photo_url': 'https://randomuser.me/api/portraits/men/30.jpg'},
        {'team': 'SEN', 'name': 'Kalidou Koulibaly', 'jersey': 3, 'position': 'DF', 'dob': date(1991, 6, 20), 'club': 'Al-Hilal',
         'photo_url': 'https://randomuser.me/api/portraits/men/31.jpg'},
        {'team': 'SEN', 'name': 'Edouard Mendy', 'jersey': 1, 'position': 'GK', 'dob': date(1992, 3, 1), 'club': 'Al-Ahli',
         'photo_url': 'https://randomuser.me/api/portraits/men/32.jpg'},
        
        # Morocco Players
        {'team': 'MAR', 'name': 'Hakim Ziyech', 'jersey': 7, 'position': 'MF', 'dob': date(1993, 3, 19), 'club': 'Galatasaray',
         'photo_url': 'https://randomuser.me/api/portraits/men/40.jpg'},
        {'team': 'MAR', 'name': 'Yassine Bounou', 'jersey': 1, 'position': 'GK', 'dob': date(1991, 4, 5), 'club': 'Al-Hilal',
         'photo_url': 'https://randomuser.me/api/portraits/men/41.jpg'},
        {'team': 'MAR', 'name': 'Achraf Hakimi', 'jersey': 2, 'position': 'DF', 'dob': date(1998, 11, 4), 'club': 'PSG',
         'photo_url': 'https://randomuser.me/api/portraits/men/42.jpg'},
    ]
    
    players_created = 0
    for data in players_data:
        team = teams.get(data['team'])
        if team:
            player, created = Player.objects.get_or_create(
                team=team,
                jersey_number=data['jersey'],
                defaults={
                    'name': data['name'],
                    'position': data['position'],
                    'date_of_birth': data['dob'],
                    'club': data['club'],
                    'photo_url': data.get('photo_url'),
                    'action_photo_url': data.get('action_photo_url'),
                }
            )
            if created:
                players_created += 1
                print(f"   ✅ Created: {player.name} ({team.short_name} #{player.jersey_number})")
    
    print(f"   📊 Total players created: {players_created}")

def create_matches(teams, stadiums):
    """Create matches with image URLs"""
    print("\n📅 Creating Matches...")
    
    match_dates = [
        date(2027, 1, 10), date(2027, 1, 11), date(2027, 1, 12), date(2027, 1, 13),
        date(2027, 1, 14), date(2027, 1, 15), date(2027, 1, 16), date(2027, 1, 17),
    ]
    
    matches_data = [
        {'num': 1, 'type': 'group', 'home': 'TAN', 'away': 'NGA', 'stadium': 'Benjamin Mkapa National Stadium', 'date': match_dates[0], 'time': time(19, 0)},
        {'num': 2, 'type': 'group', 'home': 'EGY', 'away': 'MAR', 'stadium': 'Benjamin Mkapa National Stadium', 'date': match_dates[0], 'time': time(16, 0)},
        {'num': 3, 'type': 'group', 'home': 'SEN', 'away': 'CMR', 'stadium': 'Arusha Stadium', 'date': match_dates[1], 'time': time(19, 0)},
        {'num': 4, 'type': 'group', 'home': 'GHA', 'away': 'CIV', 'stadium': 'Amaan Stadium', 'date': match_dates[1], 'time': time(19, 0)},
        {'num': 5, 'type': 'group', 'home': 'ALG', 'away': 'TUN', 'stadium': 'Benjamin Mkapa National Stadium', 'date': match_dates[2], 'time': time(16, 0)},
        {'num': 6, 'type': 'group', 'home': 'RSA', 'away': 'MLI', 'stadium': 'Arusha Stadium', 'date': match_dates[2], 'time': time(19, 0)},
        {'num': 7, 'type': 'group', 'home': 'COD', 'away': 'BFA', 'stadium': 'Amaan Stadium', 'date': match_dates[3], 'time': time(16, 0)},
        {'num': 8, 'type': 'group', 'home': 'GUI', 'away': 'EQG', 'stadium': 'Benjamin Mkapa National Stadium', 'date': match_dates[3], 'time': time(19, 0)},
    ]
    
    for data in matches_data:
        match, created = Match.objects.get_or_create(
            match_number=data['num'],
            defaults={
                'match_type': data['type'],
                'home_team': teams[data['home']],
                'away_team': teams[data['away']],
                'stadium': stadiums[data['stadium']],
                'date': data['date'],
                'time': data['time'],
                'status': 'scheduled',
                'poster_url': 'https://images.unsplash.com/photo-1522778119026-d647f0596c20?w=800',
                'tv_channels': ['Azam TV', 'SuperSport', 'BBC Sport'],
            }
        )
        if created:
            print(f"   ✅ Created: Match {match.match_number}: {match.home_team.short_name} vs {match.away_team.short_name}")

def create_group_standings(teams):
    """Create group standings"""
    print("\n📊 Creating Group Standings...")
    
    groups = ['A', 'B', 'C', 'D', 'E', 'F']
    for group in groups:
        group_teams = Team.objects.filter(group=group)
        for team in group_teams:
            standing, created = GroupStanding.objects.get_or_create(
                team=team,
                group=group,
                defaults={
                    'played': 0,
                    'won': 0,
                    'drawn': 0,
                    'lost': 0,
                    'goals_for': 0,
                    'goals_against': 0,
                    'points': 0,
                }
            )
        print(f"   ✅ Created standings for Group {group}")

def create_news():
    """Create news articles with image URLs"""
    print("\n📰 Creating News...")
    
    news_data = [
        {
            'title': 'AFCON 2027 Draw: Tanzania placed in Group A with Nigeria, Egypt, Morocco',
            'slug': 'afcon-2027-draw-tanzania-group-a',
            'content': 'The official draw for AFCON 2027 has placed hosts Tanzania in Group A alongside African giants Nigeria, Egypt, and Morocco.',
            'excerpt': 'Hosts Tanzania face a tough group with Nigeria, Egypt, and Morocco.',
            'category': 'team_news',
            'author': 'AFCON Media',
            'featured_image_url': 'https://images.unsplash.com/photo-1522778119026-d647f0596c20?w=800',
            'thumbnail_url': 'https://images.unsplash.com/photo-1522778119026-d647f0596c20?w=400',
            'is_published': True,
        },
        {
            'title': 'Benjamin Mkapa Stadium Ready for AFCON 2027 Opening Match',
            'slug': 'benjamin-mkapa-stadium-ready-afcon-2027',
            'content': 'The newly renovated Benjamin Mkapa Stadium in Dar es Salaam is ready to host the Africa Cup of Nations.',
            'excerpt': 'Dar es Salaam\'s main stadium completes renovation.',
            'category': 'general',
            'author': 'AFCON Media',
            'featured_image_url': 'https://images.unsplash.com/photo-1595435934247-5d33b7f92c70?w=800',
            'thumbnail_url': 'https://images.unsplash.com/photo-1595435934247-5d33b7f92c70?w=400',
            'is_published': True,
        },
        {
            'title': 'Taifa Stars Squad Announced for AFCON 2027',
            'slug': 'taifa-stars-squad-announced-afcon-2027',
            'content': 'Tanzania national team coach has announced the final 27-man squad for AFCON 2027.',
            'excerpt': 'Captain Himid Mao leads a talented Tanzania squad.',
            'category': 'team_news',
            'author': 'Tanzania Football Federation',
            'featured_image_url': 'https://images.unsplash.com/photo-1577223625816-7546f13df25d?w=800',
            'thumbnail_url': 'https://images.unsplash.com/photo-1577223625816-7546f13df25d?w=400',
            'is_published': True,
        },
        {
            'title': 'Top Scorers to Watch at AFCON 2027',
            'slug': 'top-scorers-to-watch-afcon-2027',
            'content': 'Mohamed Salah, Victor Osimhen, and Sadio Mané headline the golden boot contenders.',
            'excerpt': 'Star strikers ready to shine at AFCON 2027.',
            'category': 'match_preview',
            'author': 'AFCON Media',
            'featured_image_url': 'https://images.unsplash.com/photo-1516026672322-bc52d61a55d5?w=800',
            'thumbnail_url': 'https://images.unsplash.com/photo-1516026672322-bc52d61a55d5?w=400',
            'is_published': True,
        },
    ]
    
    for data in news_data:
        news, created = MatchNews.objects.get_or_create(
            slug=data['slug'],
            defaults={
                'title': data['title'],
                'content': data['content'],
                'excerpt': data['excerpt'],
                'category': data['category'],
                'author': data['author'],
                'featured_image_url': data['featured_image_url'],
                'thumbnail_url': data.get('thumbnail_url'),
                'is_published': data['is_published'],
            }
        )
        if created:
            print(f"   ✅ Created: {news.title}")

def main():
    print("=" * 60)
    print("POPULATING FOOTBALL DATA WITH IMAGES")
    print("=" * 60)
    
    # Clear existing data
    clear_existing_data()
    
    # Create all data
    stadiums = create_stadiums()
    teams = create_teams(stadiums)
    create_players(teams)
    create_matches(teams, stadiums)
    create_group_standings(teams)
    create_news()
    
    # Final summary
    print("\n" + "=" * 60)
    print("FINAL SUMMARY")
    print("=" * 60)
    print(f"🏟️ Stadiums: {Stadium.objects.count()}")
    print(f"⚽ Teams: {Team.objects.count()}")
    print(f"👤 Players: {Player.objects.count()}")
    print(f"📅 Matches: {Match.objects.count()}")
    print(f"📊 Group Standings: {GroupStanding.objects.count()}")
    print(f"📰 News: {MatchNews.objects.count()}")
    print("=" * 60)
    print("\n🎉 All football data populated successfully!")
    print("\n📸 All images are from Unsplash and flagcdn.com")

if __name__ == "__main__":
    main()