from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator
from hotels.models import Hotel  # To link hotels near stadiums

class Team(models.Model):
    """National Team Model"""
    GROUP_CHOICES = [
        ('A', 'Group A'),
        ('B', 'Group B'),
        ('C', 'Group C'),
        ('D', 'Group D'),
        ('E', 'Group E'),
        ('F', 'Group F'),
    ]
    
    name = models.CharField(max_length=100)
    short_name = models.CharField(max_length=10, help_text="e.g., TAN, NGR, EGY")
    country_code = models.CharField(max_length=3, help_text="ISO country code")
    
    # Image URLs - Team related images
    flag_url = models.URLField(blank=True, null=True, 
                               help_text="URL for team flag (e.g., from flagcdn.com)")
    logo_url = models.URLField(blank=True, null=True,
                               help_text="URL for team logo")
    jersey_url = models.URLField(blank=True, null=True,
                                 help_text="URL for team jersey image")
    team_photo_url = models.URLField(blank=True, null=True,
                                     help_text="URL for team group photo")
    stadium_photo_url = models.URLField(blank=True, null=True,
                                        help_text="URL for team's home stadium photo")
    
    group = models.CharField(max_length=1, choices=GROUP_CHOICES)
    fifa_ranking = models.IntegerField(default=100, help_text="Current FIFA World Ranking")
    coach = models.CharField(max_length=100)
    coach_photo_url = models.URLField(blank=True, null=True,
                                      help_text="URL for coach photo")
    stadium = models.ForeignKey('Stadium', on_delete=models.SET_NULL, null=True, blank=True, related_name='home_teams')
    founded = models.IntegerField(null=True, blank=True)
    association = models.CharField(max_length=200, help_text="Football association name", blank=True)
    website = models.URLField(blank=True)
    social_media = models.JSONField(default=dict, help_text="Social media links")
    achievements = models.TextField(blank=True, help_text="Previous AFCON achievements")
    squad_value = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True, help_text="Estimated squad value in USD")
    
    # Statistics for current tournament
    played = models.IntegerField(default=0)
    won = models.IntegerField(default=0)
    drawn = models.IntegerField(default=0)
    lost = models.IntegerField(default=0)
    goals_for = models.IntegerField(default=0)
    goals_against = models.IntegerField(default=0)
    points = models.IntegerField(default=0)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['group', '-points', 'name']
    
    def __str__(self):
        return f"{self.name} ({self.group})"
    
    def goal_difference(self):
        return self.goals_for - self.goals_against
    
    def get_flag_url(self):
        """Get flag URL - priority: flag_url > default"""
        if self.flag_url:
            return self.flag_url
        return f"https://flagcdn.com/w320/{self.country_code.lower()}.png"
    
    def get_logo_url(self):
        """Get logo URL"""
        return self.logo_url
    
    def get_jersey_url(self):
        """Get jersey URL"""
        return self.jersey_url
    
    def get_team_photo_url(self):
        """Get team photo URL"""
        return self.team_photo_url
    
    def get_coach_photo_url(self):
        """Get coach photo URL"""
        return self.coach_photo_url
    
    def get_group_display(self):
        return f"Group {self.group}"


class Player(models.Model):
    """Player Model"""
    POSITION_CHOICES = [
        ('GK', 'Goalkeeper'),
        ('DF', 'Defender'),
        ('MF', 'Midfielder'),
        ('FW', 'Forward'),
    ]
    
    team = models.ForeignKey(Team, on_delete=models.CASCADE, related_name='players')
    name = models.CharField(max_length=100)
    jersey_number = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(99)])
    position = models.CharField(max_length=2, choices=POSITION_CHOICES)
    position_detail = models.CharField(max_length=50, blank=True, help_text="e.g., Center Back, Striker")
    date_of_birth = models.DateField()
    age = models.IntegerField(editable=False, default=0)
    height = models.DecimalField(max_digits=5, decimal_places=2, help_text="Height in meters", null=True, blank=True)
    weight = models.DecimalField(max_digits=5, decimal_places=2, help_text="Weight in kg", null=True, blank=True)
    preferred_foot = models.CharField(max_length=10, choices=[('left', 'Left'), ('right', 'Right'), ('both', 'Both')], default='right')
    
    # Player Image URLs - Multiple photo options
    photo_url = models.URLField(blank=True, null=True,
                                help_text="URL for player portrait photo")
    action_photo_url = models.URLField(blank=True, null=True,
                                       help_text="URL for action photo during match")
    celebration_photo_url = models.URLField(blank=True, null=True,
                                            help_text="URL for goal celebration photo")
    training_photo_url = models.URLField(blank=True, null=True,
                                         help_text="URL for training session photo")
    jersey_photo_url = models.URLField(blank=True, null=True,
                                       help_text="URL for player jersey photo")
    
    club = models.CharField(max_length=100, blank=True, help_text="Current club team")
    club_country = models.CharField(max_length=50, blank=True)
    club_logo_url = models.URLField(blank=True, null=True,
                                    help_text="URL for club logo")
    market_value = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True, help_text="Market value in USD")
    
    # Tournament statistics
    appearances = models.IntegerField(default=0)
    goals = models.IntegerField(default=0)
    assists = models.IntegerField(default=0)
    yellow_cards = models.IntegerField(default=0)
    red_cards = models.IntegerField(default=0)
    man_of_match = models.IntegerField(default=0)
    minutes_played = models.IntegerField(default=0)
    
    bio = models.TextField(blank=True)
    social_media = models.JSONField(default=dict, blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['team', 'jersey_number']
        unique_together = ['team', 'jersey_number']
    
    def __str__(self):
        return f"{self.name} ({self.team.short_name}) - #{self.jersey_number}"
    
    def save(self, *args, **kwargs):
        from datetime import date
        if self.date_of_birth:
            today = date.today()
            self.age = today.year - self.date_of_birth.year - ((today.month, today.day) < (self.date_of_birth.month, self.date_of_birth.day))
        super().save(*args, **kwargs)
    
    def get_position_icon(self):
        icons = {
            'GK': '🥅',
            'DF': '🛡️',
            'MF': '⚙️',
            'FW': '⚽'
        }
        return icons.get(self.position, '🏃')
    
    def get_photo_url(self):
        """Get player photo URL - priority: photo_url > placeholder by position"""
        if self.photo_url:
            return self.photo_url
        # Default placeholder based on position
        placeholders = {
            'GK': 'https://via.placeholder.com/300x300/1e40af/white?text=GK',
            'DF': 'https://via.placeholder.com/300x300/166534/white?text=DF',
            'MF': 'https://via.placeholder.com/300x300/854d0e/white?text=MF',
            'FW': 'https://via.placeholder.com/300x300/9d174d/white?text=FW',
        }
        return placeholders.get(self.position, 'https://via.placeholder.com/300x300/1f2937/white?text=Player')
    
    def get_action_photo_url(self):
        """Get action photo URL"""
        return self.action_photo_url
    
    def get_celebration_photo_url(self):
        """Get celebration photo URL"""
        return self.celebration_photo_url
    
    def get_training_photo_url(self):
        """Get training photo URL"""
        return self.training_photo_url
    
    def get_jersey_photo_url(self):
        """Get jersey photo URL"""
        return self.jersey_photo_url
    
    def get_club_logo_url(self):
        """Get club logo URL"""
        return self.club_logo_url


class Stadium(models.Model):
    """Stadium/Venue Model"""
    STATUS_CHOICES = [
        ('active', 'Active'),
        ('under_maintenance', 'Under Maintenance'),
        ('closed', 'Closed'),
    ]
    
    name = models.CharField(max_length=200)
    city = models.CharField(max_length=100)
    country = models.CharField(max_length=100, default='Tanzania')
    capacity = models.IntegerField(validators=[MinValueValidator(1)])
    built_year = models.IntegerField(null=True, blank=True)
    renovated_year = models.IntegerField(null=True, blank=True)
    
    # Location details
    address = models.TextField()
    latitude = models.DecimalField(max_digits=10, decimal_places=7, null=True, blank=True)
    longitude = models.DecimalField(max_digits=10, decimal_places=7, null=True, blank=True)
    
    # Stadium features
    has_floodlights = models.BooleanField(default=True)
    has_roof = models.BooleanField(default=False)
    pitch_type = models.CharField(max_length=50, default='Natural Grass', choices=[
        ('natural', 'Natural Grass'),
        ('artificial', 'Artificial Turf'),
        ('hybrid', 'Hybrid')
    ])
    
    # Stadium Image URLs
    main_image_url = models.URLField(blank=True, null=True,
                                     help_text="URL for main stadium image")
    aerial_image_url = models.URLField(blank=True, null=True,
                                       help_text="URL for aerial view")
    night_image_url = models.URLField(blank=True, null=True,
                                      help_text="URL for night view of stadium")
    pitch_image_url = models.URLField(blank=True, null=True,
                                      help_text="URL for pitch/field image")
    stands_image_url = models.URLField(blank=True, null=True,
                                       help_text="URL for stands/seats image")
    gallery_images = models.JSONField(default=list, blank=True, help_text="List of image URLs for gallery")
    
    # Nearby hotels (link to your existing hotel system)
    nearby_hotels = models.ManyToManyField(Hotel, blank=True, related_name='nearby_stadiums')
    
    # Description
    description = models.TextField(blank=True)
    facilities = models.JSONField(default=list, help_text="List of facilities available")
    transport_info = models.TextField(blank=True, help_text="How to reach the stadium")
    
    # Status
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='active')
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['city', 'name']
    
    def __str__(self):
        return f"{self.name} - {self.city}"
    
    def get_capacity_display(self):
        return f"{self.capacity:,}"
    
    def get_main_image_url(self):
        """Get main stadium image URL"""
        if self.main_image_url:
            return self.main_image_url
        # Default images by city
        default_images = {
            'Dar es Salaam': 'https://images.unsplash.com/photo-1595435934247-5d33b7f92c70?w=800',
            'Arusha': 'https://images.unsplash.com/photo-1516026672322-bc52d61a55d5?w=800',
            'Zanzibar': 'https://images.unsplash.com/photo-1563492065599-3520f775eeed?w=800',
        }
        return default_images.get(self.city, 'https://via.placeholder.com/800x400/1f2937/white?text=Stadium')
    
    def get_aerial_image_url(self):
        """Get aerial image URL"""
        return self.aerial_image_url
    
    def get_night_image_url(self):
        """Get night image URL"""
        return self.night_image_url
    
    def get_pitch_image_url(self):
        """Get pitch image URL"""
        return self.pitch_image_url
    
    def get_stands_image_url(self):
        """Get stands image URL"""
        return self.stands_image_url
    
    def get_gallery_images(self):
        """Get all gallery images as list of URLs"""
        images = []
        if self.gallery_images:
            images.extend(self.gallery_images)
        if self.main_image_url:
            images.append(self.main_image_url)
        if self.aerial_image_url:
            images.append(self.aerial_image_url)
        if self.night_image_url:
            images.append(self.night_image_url)
        return images


class Match(models.Model):
    """Match Fixture and Results Model"""
    MATCH_STATUS = [
        ('scheduled', 'Scheduled'),
        ('live', 'Live'),
        ('finished', 'Finished'),
        ('postponed', 'Postponed'),
        ('cancelled', 'Cancelled'),
    ]
    
    MATCH_TYPE = [
        ('group', 'Group Stage'),
        ('quarterfinal', 'Quarter Final'),
        ('semifinal', 'Semi Final'),
        ('third_place', 'Third Place Playoff'),
        ('final', 'Final'),
    ]
    
    # Match identification
    match_number = models.IntegerField(unique=True, help_text="AFCON 2027 match number")
    match_type = models.CharField(max_length=20, choices=MATCH_TYPE)
    
    # Teams
    home_team = models.ForeignKey(Team, on_delete=models.CASCADE, related_name='home_matches')
    away_team = models.ForeignKey(Team, on_delete=models.CASCADE, related_name='away_matches')
    
    # Venue
    stadium = models.ForeignKey(Stadium, on_delete=models.CASCADE, related_name='matches')
    
    # Date and time
    date = models.DateField()
    time = models.TimeField()
    local_timezone = models.CharField(max_length=50, default='Africa/Dar_es_Salaam')
    
    # Status
    status = models.CharField(max_length=20, choices=MATCH_STATUS, default='scheduled')
    
    # Results (populated when match is finished)
    home_score = models.IntegerField(null=True, blank=True)
    away_score = models.IntegerField(null=True, blank=True)
    home_penalty_score = models.IntegerField(null=True, blank=True)
    away_penalty_score = models.IntegerField(null=True, blank=True)
    winner = models.ForeignKey(Team, on_delete=models.SET_NULL, null=True, blank=True, related_name='matches_won')
    
    # Statistics
    possession_home = models.IntegerField(null=True, blank=True, validators=[MinValueValidator(0), MaxValueValidator(100)])
    possession_away = models.IntegerField(null=True, blank=True, validators=[MinValueValidator(0), MaxValueValidator(100)])
    shots_home = models.IntegerField(null=True, blank=True)
    shots_away = models.IntegerField(null=True, blank=True)
    shots_on_target_home = models.IntegerField(null=True, blank=True)
    shots_on_target_away = models.IntegerField(null=True, blank=True)
    corners_home = models.IntegerField(null=True, blank=True)
    corners_away = models.IntegerField(null=True, blank=True)
    fouls_home = models.IntegerField(null=True, blank=True)
    fouls_away = models.IntegerField(null=True, blank=True)
    
    # Attendance
    attendance = models.IntegerField(null=True, blank=True, help_text="Number of spectators")
    
    # Broadcast
    tv_channels = models.JSONField(default=list, blank=True, help_text="List of TV channels broadcasting")
    live_stream_url = models.URLField(blank=True, help_text="Official streaming link")
    
    # Match Image URLs
    poster_url = models.URLField(blank=True, null=True,
                                 help_text="URL for match poster/cover image")
    highlight_thumbnail_url = models.URLField(blank=True, null=True,
                                              help_text="URL for highlight video thumbnail")
    lineup_image_url = models.URLField(blank=True, null=True,
                                       help_text="URL for team lineup image")
    
    # Metadata
    match_report = models.TextField(blank=True, help_text="Match summary")
    referee = models.CharField(max_length=100, blank=True)
    assistant_referees = models.JSONField(default=list, blank=True)
    fourth_official = models.CharField(max_length=100, blank=True)
    var_referee = models.CharField(max_length=100, blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['date', 'time']
        unique_together = ['date', 'stadium', 'time']
    
    def __str__(self):
        return f"Match {self.match_number}: {self.home_team.short_name} vs {self.away_team.short_name}"
    
    def is_finished(self):
        return self.status == 'finished'
    
    def is_live(self):
        return self.status == 'live'
    
    def get_result(self):
        if self.home_score is not None and self.away_score is not None:
            if self.home_penalty_score is not None and self.away_penalty_score is not None:
                return f"{self.home_score}-{self.away_score} ({self.home_penalty_score}-{self.away_penalty_score} pens)"
            return f"{self.home_score}-{self.away_score}"
        return "vs"
    
    def get_winner_display(self):
        if self.winner:
            return self.winner.name
        if self.home_score == self.away_score:
            return "Draw"
        return "Not decided"
    
    def get_poster_url(self):
        """Get match poster URL"""
        return self.poster_url
    
    def get_highlight_thumbnail_url(self):
        """Get highlight thumbnail URL"""
        return self.highlight_thumbnail_url
    
    def get_lineup_image_url(self):
        """Get lineup image URL"""
        return self.lineup_image_url


class Goal(models.Model):
    """Goal Scorer Model"""
    match = models.ForeignKey(Match, on_delete=models.CASCADE, related_name='goals')
    player = models.ForeignKey(Player, on_delete=models.CASCADE, related_name='player_goals')
    team = models.ForeignKey(Team, on_delete=models.CASCADE, related_name='team_goals')
    minute = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(120)])
    is_penalty = models.BooleanField(default=False)
    is_own_goal = models.BooleanField(default=False)
    is_first_half = models.BooleanField(default=True)
    
    # Goal celebration image
    celebration_image_url = models.URLField(blank=True, null=True,
                                            help_text="URL for goal celebration image")
    
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['match', 'minute']
    
    def __str__(self):
        return f"{self.minute}' - {self.player.name} ({self.team.short_name})"
    
    def get_minute_display(self):
        if self.minute <= 45:
            return f"{self.minute}' (1st Half)"
        elif self.minute <= 90:
            return f"{self.minute}' (2nd Half)"
        else:
            return f"{self.minute}' (Extra Time)"
    
    def get_celebration_image_url(self):
        """Get celebration image URL"""
        return self.celebration_image_url


class GroupStanding(models.Model):
    """Group Stage Standings"""
    team = models.ForeignKey(Team, on_delete=models.CASCADE, related_name='group_standings')
    group = models.CharField(max_length=1)
    played = models.IntegerField(default=0)
    won = models.IntegerField(default=0)
    drawn = models.IntegerField(default=0)
    lost = models.IntegerField(default=0)
    goals_for = models.IntegerField(default=0)
    goals_against = models.IntegerField(default=0)
    points = models.IntegerField(default=0)
    
    class Meta:
        ordering = ['group', '-points', '-goals_for']
        unique_together = ['team', 'group']
    
    def __str__(self):
        return f"{self.team.name} - Group {self.group}"
    
    def goal_difference(self):
        return self.goals_for - self.goals_against
    
    def update_from_matches(self):
        """Calculate standings based on match results"""
        matches = Match.objects.filter(
            models.Q(home_team=self.team) | models.Q(away_team=self.team),
            status='finished'
        )
        
        self.played = matches.count()
        self.won = 0
        self.drawn = 0
        self.lost = 0
        self.goals_for = 0
        self.goals_against = 0
        self.points = 0
        
        for match in matches:
            if match.home_team == self.team:
                self.goals_for += match.home_score or 0
                self.goals_against += match.away_score or 0
                if match.home_score > match.away_score:
                    self.won += 1
                    self.points += 3
                elif match.home_score == match.away_score:
                    self.drawn += 1
                    self.points += 1
                else:
                    self.lost += 1
            else:
                self.goals_for += match.away_score or 0
                self.goals_against += match.home_score or 0
                if match.away_score > match.home_score:
                    self.won += 1
                    self.points += 3
                elif match.away_score == match.home_score:
                    self.drawn += 1
                    self.points += 1
                else:
                    self.lost += 1
        
        self.save()


class Ticket(models.Model):
    """Match Ticket Model"""
    TICKET_CATEGORY = [
        ('vip', 'VIP - Best View + Hospitality'),
        ('premium', 'Premium - Excellent View'),
        ('standard', 'Standard - Good View'),
        ('economy', 'Economy - Behind Goals'),
    ]
    
    TICKET_STATUS = [
        ('available', 'Available'),
        ('reserved', 'Reserved'),
        ('sold', 'Sold'),
        ('cancelled', 'Cancelled'),
    ]
    
    match = models.ForeignKey(Match, on_delete=models.CASCADE, related_name='tickets')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='match_tickets', null=True, blank=True)
    category = models.CharField(max_length=20, choices=TICKET_CATEGORY)
    seat_section = models.CharField(max_length=50)
    seat_row = models.CharField(max_length=10)
    seat_number = models.CharField(max_length=10)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=20, choices=TICKET_STATUS, default='available')
    
    # QR Code for entry
    qr_code = models.CharField(max_length=255, unique=True, blank=True)
    
    # Booking details
    booking_reference = models.CharField(max_length=50, unique=True, blank=True)
    booked_at = models.DateTimeField(auto_now_add=True)
    
    # Additional info
    includes_hospitality = models.BooleanField(default=False)
    includes_parking = models.BooleanField(default=False)
    
    class Meta:
        ordering = ['match', 'category', 'seat_section', 'seat_row', 'seat_number']
    
    def __str__(self):
        return f"{self.match} - {self.category} - {self.seat_section}{self.seat_row}{self.seat_number}"


class MatchNews(models.Model):
    """News and Updates about AFCON"""
    NEWS_CATEGORY = [
        ('match_preview', 'Match Preview'),
        ('match_report', 'Match Report'),
        ('team_news', 'Team News'),
        ('player_interview', 'Player Interview'),
        ('injury_update', 'Injury Update'),
        ('general', 'General News'),
    ]
    
    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)
    content = models.TextField()
    excerpt = models.TextField(blank=True, help_text="Short summary")
    category = models.CharField(max_length=20, choices=NEWS_CATEGORY)
    
    # Related entities
    related_match = models.ForeignKey(Match, on_delete=models.SET_NULL, null=True, blank=True)
    related_team = models.ForeignKey(Team, on_delete=models.SET_NULL, null=True, blank=True)
    related_player = models.ForeignKey(Player, on_delete=models.SET_NULL, null=True, blank=True)
    
    # Media URLs
    featured_image_url = models.URLField(blank=True, null=True, help_text="URL for featured image")
    gallery = models.JSONField(default=list, blank=True, help_text="List of gallery image URLs")
    video_url = models.URLField(blank=True, help_text="URL for video content")
    thumbnail_url = models.URLField(blank=True, null=True, help_text="URL for video thumbnail")
    
    # Publication
    author = models.CharField(max_length=100, default='AFCON Staff')
    published_at = models.DateTimeField(auto_now_add=True)
    is_published = models.BooleanField(default=True)
    
    class Meta:
        ordering = ['-published_at']
        verbose_name_plural = "Match News"
    
    def __str__(self):
        return self.title
    
    def get_featured_image_url(self):
        """Get featured image URL"""
        return self.featured_image_url
    
    def get_thumbnail_url(self):
        """Get thumbnail URL"""
        return self.thumbnail_url


class UserPrediction(models.Model):
    """User predictions for matches"""
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='predictions')
    match = models.ForeignKey(Match, on_delete=models.CASCADE, related_name='predictions')
    predicted_home_score = models.IntegerField()
    predicted_away_score = models.IntegerField()
    predicted_winner = models.ForeignKey(Team, on_delete=models.SET_NULL, null=True, blank=True, related_name='predicted_wins')
    points_earned = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        unique_together = ['user', 'match']
    
    def __str__(self):
        return f"{self.user.username} - {self.match}"
    
    def calculate_points(self):
        """Calculate prediction points after match is finished"""
        if not self.match.is_finished():
            return 0
        
        points = 0
        
        # Exact score: 5 points
        if self.predicted_home_score == self.match.home_score and self.predicted_away_score == self.match.away_score:
            points = 5
        # Correct winner/draw: 3 points
        elif self.predicted_winner == self.match.winner:
            points = 3
        # Correct result direction: 1 point
        elif (self.predicted_home_score - self.predicted_away_score) * (self.match.home_score - self.match.away_score) > 0:
            points = 1
        
        self.points_earned = points
        self.save()
        return points


class MatchAlert(models.Model):
    """User alerts for matches"""
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='match_alerts')
    match = models.ForeignKey(Match, on_delete=models.CASCADE, related_name='alerts')
    alert_before_minutes = models.IntegerField(default=60, help_text="Alert X minutes before match")
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ['user', 'match']
    
    def __str__(self):
        return f"{self.user.username} - {self.match}"


class NewsComment(models.Model):
    """Comments on news articles"""
    news = models.ForeignKey(MatchNews, on_delete=models.CASCADE, related_name='comments')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='news_comments')
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_approved = models.BooleanField(default=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"Comment by {self.user.username} on {self.news.title}"