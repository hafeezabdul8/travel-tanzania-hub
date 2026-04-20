import os
import sys
import django
from decimal import Decimal
from datetime import datetime  # Import datetime to parse strings

sys.path.append('/home/feezman/afcon_project')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'afcon.settings')
django.setup()

from football.models import Team, Player

def populate_database():
    # --- TEAM DATA ---
    teams_to_create = [
        {"name": "South Africa", "short_name": "RSA", "country_code": "ZA", "group": "A", "coach": "Hugo Broos", "rank": 59},
        {"name": "Cameroon", "short_name": "CMR", "country_code": "CM", "group": "C", "coach": "Marc Brys", "rank": 49},
        {"name": "Mali", "short_name": "MLI", "country_code": "ML", "group": "E", "coach": "Tom Saintfiet", "rank": 54},
        {"name": "Ivory Coast", "short_name": "CIV", "country_code": "CI", "group": "A", "coach": "Emerse Faé", "rank": 38},
        {"name": "Kenya", "short_name": "KEN", "country_code": "KE", "group": "F", "coach": "Engin Fırat", "rank": 102},
    ]

    team_objs = {}
    for t_data in teams_to_create:
        team, _ = Team.objects.get_or_create(
            name=t_data["name"],
            defaults={
                "short_name": t_data["short_name"],
                "country_code": t_data["country_code"],
                "group": t_data["group"],
                "coach": t_data["coach"],
                "fifa_ranking": t_data["rank"]
            }
        )
        team_objs[t_data["name"]] = team

    # --- PLAYER DATA (4 per team) ---
    players_data = {
        "South Africa": [
            ("Ronwen Williams", 1, "GK", "Mamelodi Sundowns", "1992-01-21", 1200000, 1.84, 79),
            ("Lyle Foster", 9, "FW", "Burnley", "2000-09-03", 14000000, 1.85, 77),
            ("Teboho Mokoena", 4, "MF", "Mamelodi Sundowns", "1997-01-24", 3000000, 1.76, 70),
            ("Percy Tau", 10, "FW", "Al Ahly", "1994-05-13", 1600000, 1.75, 72),
        ],
        "Cameroon": [
            ("André Onana", 24, "GK", "Manchester United", "1996-04-02", 43000000, 1.90, 93),
            ("Bryan Mbeumo", 10, "FW", "Brentford", "1999-08-07", 45000000, 1.71, 70),
            ("Zambo Anguissa", 8, "MF", "Napoli", "1995-11-16", 38000000, 1.84, 78),
            ("Christopher Wooh", 4, "DF", "Rennes", "2001-09-18", 10000000, 1.91, 85),
        ],
        "Mali": [
            ("Yves Bissouma", 10, "MF", "Tottenham", "1996-08-30", 35000000, 1.82, 80),
            ("Amadou Haidara", 4, "MF", "RB Leipzig", "1998-01-31", 20000000, 1.75, 72),
            ("El Bilal Touré", 9, "FW", "Stuttgart", "2001-10-03", 20000000, 1.85, 77),
            ("Hamari Traoré", 2, "DF", "Real Sociedad", "1992-01-27", 3500000, 1.75, 71),
        ],
        "Ivory Coast": [
            ("Sébastien Haller", 22, "FW", "Leganes", "1994-06-22", 12000000, 1.90, 82),
            ("Franck Kessié", 8, "MF", "Al Ahli", "1996-12-19", 18000000, 1.83, 82),
            ("Ousmane Diomande", 2, "DF", "Sporting CP", "2003-12-04", 45000000, 1.90, 86),
            ("Simon Adingra", 24, "FW", "Brighton", "2002-01-01", 30000000, 1.75, 69),
        ],
        "Kenya": [
            ("Michael Olunga", 14, "FW", "Al-Duhail", "1994-03-26", 8000000, 1.93, 85),
            ("Joseph Okumu", 2, "DF", "Reims", "1997-05-26", 9000000, 1.93, 82),
            ("Richard Odada", 6, "MF", "Dundee Utd", "2000-11-25", 600000, 1.90, 78),
            ("Patrick Matasi", 18, "GK", "Kenya Police", "1987-12-11", 100000, 1.88, 80),
        ]
    }

    # Populate Players
    for team_name, players in players_data.items():
        team_obj = team_objs[team_name]
        for p in players:
            # Convert date string to date object so model.save() can read .year
            dob_obj = datetime.strptime(p[4], "%Y-%m-%d").date()
            
            Player.objects.update_or_create(
                team=team_obj,
                jersey_number=p[1],
                defaults={
                    "name": p[0],
                    "position": p[2],
                    "club": p[3],
                    "date_of_birth": dob_obj,
                    "market_value": Decimal(p[5]),
                    "height": Decimal(p[6]),
                    "weight": Decimal(p[7]),
                }
            )
            print(f"Created/Updated: {p[0]}")

    print("\n✅ Successfully added 20 star players!")

if __name__ == "__main__":
    populate_database()
