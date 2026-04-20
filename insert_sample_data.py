# football/insert_sample_data.py
import os
import django
from datetime import date, time, datetime, timedelta

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'afcon.settings')
django.setup()

from football.models import (
    Team, Player, Stadium, Match, Goal, GroupStanding, 
    MatchNews, UserPrediction, MatchAlert
)
from django.contrib.auth.models import User

print("=" * 50)
print("Inserting Sample Data for AFCON 2027")
print("=" * 50)

# ============ 1. CREATE STADIUMS ============
print("\n📋 Creating Stadiums...")

stadiums_data = [
    {
        'name': 'Benjamin Mkapa National Stadium',
        'city': 'Dar es Salaam',
        'capacity': 60000,
        'address': 'Taifa Road, Dar es Salaam',
        'description': 'The main stadium for AFCON 2027, hosting the opening match and final.',
        'has_floodlights': True,
        'pitch_type': 'natural',
        'main_image_url': 'https://images.unsplash.com/photo-1595435934247-5d33b7f92c70?w=800',
        'gallery_images': [
            'https://images.unsplash.com/photo-1595435934247-5d33b7f92c70?w=800',
            'https://images.unsplash.com/photo-1577223625816-7546f13df25d?w=800',
        ],
        'transport_info': 'Located in Kivukoni area. Accessible by taxi and public buses. Special AFCON shuttle buses available.'
    },
    {
        'name': 'Arusha Stadium',
        'city': 'Arusha',
        'capacity': 30000,
        'address': 'Sokoine Road, Arusha',
        'description': 'Modern stadium in the safari capital, hosting group stage matches.',
        'has_floodlights': True,
        'pitch_type': 'natural',
        'main_image_url': 'https://images.unsplash.com/photo-1516026672322-bc52d61a55d5?w=800',
        'transport_info': 'Located in city center. Walking distance from many hotels.'
    },
    {
        'name': 'Amaan Stadium',
        'city': 'Zanzibar',
        'capacity': 25000,
        'address': 'Zanzibar City, Zanzibar',
        'description': 'Coastal stadium with beautiful ocean views.',
        'has_floodlights': True,
        'pitch_type': 'natural',
        'main_image_url': 'https://images.unsplash.com/photo-1563492065599-3520f775eeed?w=800',
        'transport_info': 'Located in Zanzibar City. Ferry terminal 15 minutes away.'
    },
]

stadiums = {}
for stadium_data in stadiums_data:
    stadium, created = Stadium.objects.get_or_create(
        name=stadium_data['name'],
        defaults=stadium_data
    )
    stadiums[stadium.name] = stadium
    print(f"   {'✅ Created' if created else '⚠️ Already exists'}: {stadium.name}")

# ============ 2. CREATE TEAMS ============
print("\n📋 Creating Teams...")

teams_data = [
    # Group A
    {'name': 'Tanzania', 'short_name': 'TAN', 'country_code': 'tz', 'group': 'A', 'fifa_ranking': 120, 'coach': 'Adel Amrouche', 'flag_url': 'https://flagcdn.com/w320/tz.png'},
    {'name': 'Nigeria', 'short_name': 'NGA', 'country_code': 'ng', 'group': 'A', 'fifa_ranking': 42, 'coach': 'Jose Peseiro', 'flag_url': 'https://flagcdn.com/w320/ng.png'},
    {'name': 'Egypt', 'short_name': 'EGY', 'country_code': 'eg', 'group': 'A', 'fifa_ranking': 35, 'coach': 'Rui Vitoria', 'flag_url': 'https://flagcdn.com/w320/eg.png'},
    {'name': 'Morocco', 'short_name': 'MAR', 'country_code': 'ma', 'group': 'A', 'fifa_ranking': 13, 'coach': 'Walid Regragui', 'flag_url': 'https://flagcdn.com/w320/ma.png'},
    # Group B
    {'name': 'Senegal', 'short_name': 'SEN', 'country_code': 'sn', 'group': 'B', 'fifa_ranking': 20, 'coach': 'Aliou Cissé', 'flag_url': 'https://flagcdn.com/w320/sn.png'},
    {'name': 'Cameroon', 'short_name': 'CMR', 'country_code': 'cm', 'group': 'B', 'fifa_ranking': 45, 'coach': 'Rigobert Song', 'flag_url': 'https://flagcdn.com/w320/cm.png'},
    {'name': 'Ghana', 'short_name': 'GHA', 'country_code': 'gh', 'group': 'B', 'fifa_ranking': 60, 'coach': 'Chris Hughton', 'flag_url': 'https://flagcdn.com/w320/gh.png'},
    {'name': 'Ivory Coast', 'short_name': 'CIV', 'country_code': 'ci', 'group': 'B', 'fifa_ranking': 55, 'coach': 'Jean-Louis Gasset', 'flag_url': 'https://flagcdn.com/w320/ci.png'},
    # Group C
    {'name': 'Algeria', 'short_name': 'ALG', 'country_code': 'dz', 'group': 'C', 'fifa_ranking': 40, 'coach': 'Djamel Belmadi', 'flag_url': 'https://flagcdn.com/w320/dz.png'},
    {'name': 'Tunisia', 'short_name': 'TUN', 'country_code': 'tn', 'group': 'C', 'fifa_ranking': 32, 'coach': 'Jalel Kadri', 'flag_url': 'https://flagcdn.com/w320/tn.png'},
    {'name': 'South Africa', 'short_name': 'RSA', 'country_code': 'za', 'group': 'C', 'fifa_ranking': 66, 'coach': 'Hugo Broos', 'flag_url': 'https://flagcdn.com/w320/za.png'},
    {'name': 'Mali', 'short_name': 'MLI', 'country_code': 'ml', 'group': 'C', 'fifa_ranking': 50, 'coach': 'Eric Chelle', 'flag_url': 'https://flagcdn.com/w320/ml.png'},
]

teams = {}
for team_data in teams_data:
    team, created = Team.objects.get_or_create(
        name=team_data['name'],
        defaults=team_data
    )
    teams[team.short_name] = team
    print(f"   {'✅ Created' if created else '⚠️ Already exists'}: {team.name} (Group {team.group})")

# ============ 3. CREATE PLAYERS ============
print("\n📋 Creating Players...")

# Tanzania players
tanzania_players = [
    {'name': 'Aishi Manula', 'jersey_number': 1, 'position': 'GK', 'date_of_birth': date(1995, 9, 13), 'club': 'Simba SC', 'photo_url': 'https://via.placeholder.com/300x300/1e40af/white?text=GK'},
    {'name': 'Kelvin John', 'jersey_number': 10, 'position': 'FW', 'date_of_birth': date(2003, 1, 26), 'club': 'Young Africans', 'photo_url': 'https://via.placeholder.com/300x300/9d174d/white?text=FW'},
    {'name': 'Simon Msuva', 'jersey_number': 11, 'position': 'FW', 'date_of_birth': date(1993, 10, 2), 'club': 'Al-Hilal', 'photo_url': 'https://via.placeholder.com/300x300/9d174d/white?text=FW'},
    {'name': 'Himid Mao', 'jersey_number': 8, 'position': 'MF', 'date_of_birth': date(1992, 11, 15), 'club': 'Young Africans', 'photo_url': 'https://via.placeholder.com/300x300/854d0e/white?text=MF'},
    {'name': 'Mudathir Yahya', 'jersey_number': 7, 'position': 'MF', 'date_of_birth': date(1996, 5, 6), 'club': 'Young Africans', 'photo_url': 'https://via.placeholder.com/300x300/854d0e/white?text=MF'},
    {'name': 'Novatus Miroshi', 'jersey_number': 2, 'position': 'DF', 'date_of_birth': date(2002, 9, 2), 'club': 'Lech Poznan', 'photo_url': 'https://via.placeholder.com/300x300/166534/white?text=DF'},
]

for player_data in tanzania_players:
    player, created = Player.objects.get_or_create(
        team=teams['TAN'],
        jersey_number=player_data['jersey_number'],
        defaults=player_data
    )
    print(f"   {'✅ Created' if created else '⚠️ Already exists'}: {player.name} (TAN #{player.jersey_number})")

# Nigeria players
nigeria_players = [
    {'name': 'Victor Osimhen', 'jersey_number': 9, 'position': 'FW', 'date_of_birth': date(1998, 12, 29), 'club': 'Napoli', 'photo_url': 'https://via.placeholder.com/300x300/9d174d/white?text=FW'},
    {'name': 'Ahmed Musa', 'jersey_number': 7, 'position': 'FW', 'date_of_birth': date(1992, 10, 14), 'club': 'Sivasspor', 'photo_url': 'https://via.placeholder.com/300x300/9d174d/white?text=FW'},
    {'name': 'Wilfred Ndidi', 'jersey_number': 4, 'position': 'MF', 'date_of_birth': date(1996, 12, 16), 'club': 'Leicester City', 'photo_url': 'https://via.placeholder.com/300x300/854d0e/white?text=MF'},
]

for player_data in nigeria_players:
    player, created = Player.objects.get_or_create(
        team=teams['NGA'],
        jersey_number=player_data['jersey_number'],
        defaults=player_data
    )
    print(f"   {'✅ Created' if created else '⚠️ Already exists'}: {player.name} (NGA #{player.jersey_number})")

# Egypt players
egypt_players = [
    {'name': 'Mohamed Salah', 'jersey_number': 10, 'position': 'FW', 'date_of_birth': date(1992, 6, 15), 'club': 'Liverpool', 'photo_url': 'https://via.placeholder.com/300x300/9d174d/white?text=FW'},
    {'name': 'Mohamed Elneny', 'jersey_number': 8, 'position': 'MF', 'date_of_birth': date(1992, 7, 11), 'club': 'Arsenal', 'photo_url': 'https://via.placeholder.com/300x300/854d0e/white?text=MF'},
]

for player_data in egypt_players:
    player, created = Player.objects.get_or_create(
        team=teams['EGY'],
        jersey_number=player_data['jersey_number'],
        defaults=player_data
    )
    print(f"   {'✅ Created' if created else '⚠️ Already exists'}: {player.name} (EGY #{player.jersey_number})")

# ============ 4. CREATE MATCHES ============
print("\n📋 Creating Matches...")

# Match dates (January 2027)
match_dates = [
    date(2027, 1, 10),  # Opening match
    date(2027, 1, 14),
    date(2027, 1, 18),
    date(2027, 1, 22),
    date(2027, 1, 26),
    date(2027, 1, 30),
]

matches_data = [
    # Opening match
    {
        'match_number': 1,
        'match_type': 'group',
        'home_team': teams['TAN'],
        'away_team': teams['NGA'],
        'stadium': stadiums['Benjamin Mkapa National Stadium'],
        'date': match_dates[0],
        'time': time(19, 0),
        'status': 'scheduled',
        'tv_channels': ['Azam TV', 'SuperSport', 'BBC Sport'],
    },
    {
        'match_number': 2,
        'match_type': 'group',
        'home_team': teams['EGY'],
        'away_team': teams['MAR'],
        'stadium': stadiums['Benjamin Mkapa National Stadium'],
        'date': match_dates[0],
        'time': time(16, 0),
        'status': 'scheduled',
        'tv_channels': ['Azam TV', 'SuperSport'],
    },
    {
        'match_number': 3,
        'match_type': 'group',
        'home_team': teams['SEN'],
        'away_team': teams['CMR'],
        'stadium': stadiums['Arusha Stadium'],
        'date': match_dates[1],
        'time': time(19, 0),
        'status': 'scheduled',
        'tv_channels': ['Azam TV', 'SuperSport'],
    },
    {
        'match_number': 4,
        'match_type': 'group',
        'home_team': teams['GHA'],
        'away_team': teams['CIV'],
        'stadium': stadiums['Amaan Stadium'],
        'date': match_dates[1],
        'time': time(19, 0),
        'status': 'scheduled',
        'tv_channels': ['Azam TV', 'SuperSport'],
    },
]

for match_data in matches_data:
    match, created = Match.objects.get_or_create(
        match_number=match_data['match_number'],
        defaults=match_data
    )
    print(f"   {'✅ Created' if created else '⚠️ Already exists'}: Match {match.match_number}: {match.home_team.short_name} vs {match.away_team.short_name}")

# ============ 5. CREATE GROUP STANDINGS ============
print("\n📋 Creating Group Standings...")

groups = ['A', 'B', 'C']
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
        print(f"   {'✅ Created' if created else '⚠️ Already exists'}: {team.name} - Group {group}")

# ============ 6. CREATE NEWS ============
print("\n📋 Creating News...")

news_data = [
    {
        'title': 'AFCON 2027 Opening Match: Tanzania vs Nigeria',
        'slug': 'afcon-2027-opening-match-tanzania-nigeria',
        'content': 'The Africa Cup of Nations 2027 will kick off with host nation Tanzania facing Nigeria at the Benjamin Mkapa National Stadium in Dar es Salaam. The match promises to be an exciting opener with both teams eager to start their campaign with a win.',
        'excerpt': 'Hosts Tanzania begin their AFCON 2027 journey against Nigeria in the opening match.',
        'category': 'match_preview',
        'author': 'AFCON Staff',
        'is_published': True,
    },
    {
        'title': 'Taifa Stars Squad Announced for AFCON 2027',
        'slug': 'taifa-stars-squad-announced-afcon-2027',
        'content': 'Tanzania national team coach has announced the final 27-man squad for AFCON 2027. The squad features a mix of experienced players and young talents ready to make their mark on the continental stage.',
        'excerpt': 'Captain Himid Mao leads a talented Tanzania squad for AFCON 2027.',
        'category': 'team_news',
        'author': 'AFCON Staff',
        'is_published': True,
    },
    {
        'title': 'Benjamin Mkapa Stadium Ready for AFCON 2027',
        'slug': 'benjamin-mkapa-stadium-ready-afcon-2027',
        'content': 'The newly renovated Benjamin Mkapa Stadium in Dar es Salaam is ready to host the Africa Cup of Nations. With a capacity of 60,000, it will be the main venue for the tournament including the opening match and final.',
        'excerpt': 'Dar es Salaam\'s main stadium completes renovation ahead of AFCON 2027.',
        'category': 'general',
        'author': 'AFCON Staff',
        'is_published': True,
    },
    {
        'title': 'Top Scorers to Watch at AFCON 2027',
        'slug': 'top-scorers-to-watch-afcon-2027',
        'content': 'With stars like Mohamed Salah, Victor Osimhen, and Sadio Mane expected to feature, AFCON 2027 promises to be a showcase of African attacking talent.',
        'excerpt': 'A look at the top goal-scoring threats at AFCON 2027.',
        'category': 'match_preview',
        'author': 'AFCON Staff',
        'is_published': True,
    },
    {
        'title': 'Travel Guide for AFCON 2027 Visitors',
        'slug': 'travel-guide-afcon-2027-visitors',
        'content': 'Everything you need to know about traveling to Tanzania for AFCON 2027. From accommodation to transportation and tourist attractions.',
        'excerpt': 'Complete travel guide for fans visiting Tanzania for AFCON 2027.',
        'category': 'general',
        'author': 'Travel Desk',
        'is_published': True,
    },
]

for news_item in news_data:
    news, created = MatchNews.objects.get_or_create(
        slug=news_item['slug'],
        defaults=news_item
    )
    print(f"   {'✅ Created' if created else '⚠️ Already exists'}: {news.title}")

# ============ SUMMARY ============
print("\n" + "=" * 50)
print("📊 DATA INSERTION SUMMARY")
print("=" * 50)
print(f"✅ Stadiums: {Stadium.objects.count()}")
print(f"✅ Teams: {Team.objects.count()}")
print(f"✅ Players: {Player.objects.count()}")
print(f"✅ Matches: {Match.objects.count()}")
print(f"✅ Group Standings: {GroupStanding.objects.count()}")
print(f"✅ News: {MatchNews.objects.count()}")
print("\n🎉 Sample data inserted successfully!")
print("=" * 50)