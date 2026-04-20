# football/admin.py
from django.contrib import admin
from .models import (
    Team, Player, Stadium, Match, Goal, GroupStanding, 
    Ticket, MatchNews, UserPrediction, MatchAlert, NewsComment
)

@admin.register(Team)
class TeamAdmin(admin.ModelAdmin):
    list_display = ['name', 'short_name', 'group', 'fifa_ranking', 'points']
    list_filter = ['group']
    search_fields = ['name', 'short_name']
    readonly_fields = ['played', 'won', 'drawn', 'lost', 'goals_for', 'goals_against', 'points']
    fieldsets = (
        ('Basic Information', {
            'fields': ('name', 'short_name', 'country_code', 'group', 'fifa_ranking')
        }),
        ('Team Details', {
            'fields': ('coach', 'stadium', 'founded', 'association', 'website', 'social_media')
        }),
        ('Images', {
            'fields': ('flag_url', 'logo_url', 'jersey_url', 'team_photo_url', 'coach_photo_url')
        }),
        ('Tournament Statistics', {
            'fields': ('played', 'won', 'drawn', 'lost', 'goals_for', 'goals_against', 'points')
        }),
        ('Achievements', {
            'fields': ('achievements', 'squad_value')
        }),
    )


@admin.register(Player)
class PlayerAdmin(admin.ModelAdmin):
    list_display = ['name', 'team', 'jersey_number', 'position', 'goals', 'appearances']
    list_filter = ['team', 'position']
    search_fields = ['name', 'team__name']
    readonly_fields = ['age']
    fieldsets = (
        ('Basic Information', {
            'fields': ('team', 'name', 'jersey_number', 'position', 'position_detail')
        }),
        ('Physical Attributes', {
            'fields': ('date_of_birth', 'age', 'height', 'weight', 'preferred_foot')
        }),
        ('Images', {
            'fields': ('photo_url', 'action_photo_url', 'celebration_photo_url', 
                      'training_photo_url', 'jersey_photo_url', 'club_logo_url')
        }),
        ('Career', {
            'fields': ('club', 'club_country', 'market_value', 'bio')
        }),
        ('Tournament Statistics', {
            'fields': ('appearances', 'goals', 'assists', 'yellow_cards', 
                      'red_cards', 'man_of_match', 'minutes_played')
        }),
        ('Social Media', {
            'fields': ('social_media',)
        }),
    )


@admin.register(Stadium)
class StadiumAdmin(admin.ModelAdmin):
    list_display = ['name', 'city', 'capacity', 'status']
    list_filter = ['city', 'status', 'pitch_type']
    search_fields = ['name', 'city']
    filter_horizontal = ['nearby_hotels']
    fieldsets = (
        ('Basic Information', {
            'fields': ('name', 'city', 'country', 'capacity', 'address')
        }),
        ('Location', {
            'fields': ('latitude', 'longitude')
        }),
        ('Images', {
            'fields': ('main_image_url', 'aerial_image_url', 'night_image_url', 
                      'pitch_image_url', 'stands_image_url', 'gallery_images')
        }),
        ('Features', {
            'fields': ('has_floodlights', 'has_roof', 'pitch_type', 'facilities')
        }),
        ('Information', {
            'fields': ('description', 'transport_info', 'status')
        }),
        ('Nearby Hotels', {
            'fields': ('nearby_hotels',)
        }),
    )


@admin.register(Match)
class MatchAdmin(admin.ModelAdmin):
    list_display = ['match_number', 'home_team', 'away_team', 'date', 'time', 'stadium', 'status']
    list_filter = ['match_type', 'status', 'date', 'stadium__city']
    search_fields = ['home_team__name', 'away_team__name']
    readonly_fields = ['created_at', 'updated_at']
    fieldsets = (
        ('Match Information', {
            'fields': ('match_number', 'match_type', 'home_team', 'away_team', 'stadium')
        }),
        ('Schedule', {
            'fields': ('date', 'time', 'local_timezone')
        }),
        ('Images', {
            'fields': ('poster_url', 'highlight_thumbnail_url', 'lineup_image_url')
        }),
        ('Status & Results', {
            'fields': ('status', 'home_score', 'away_score', 'home_penalty_score', 
                      'away_penalty_score', 'winner')
        }),
        ('Statistics', {
            'fields': ('possession_home', 'possession_away', 'shots_home', 'shots_away', 
                      'shots_on_target_home', 'shots_on_target_away', 'corners_home', 'corners_away',
                      'fouls_home', 'fouls_away')
        }),
        ('Broadcast & Attendance', {
            'fields': ('attendance', 'tv_channels', 'live_stream_url')
        }),
        ('Officials', {
            'fields': ('referee', 'assistant_referees', 'fourth_official', 'var_referee')
        }),
        ('Report', {
            'fields': ('match_report',)
        }),
    )


@admin.register(Goal)
class GoalAdmin(admin.ModelAdmin):
    list_display = ['match', 'player', 'team', 'minute', 'is_penalty', 'is_own_goal']
    list_filter = ['is_penalty', 'is_own_goal']
    search_fields = ['player__name', 'team__name']
    fieldsets = (
        ('Goal Information', {
            'fields': ('match', 'player', 'team', 'minute')
        }),
        ('Details', {
            'fields': ('is_penalty', 'is_own_goal', 'is_first_half', 'celebration_image_url')
        }),
    )


@admin.register(GroupStanding)
class GroupStandingAdmin(admin.ModelAdmin):
    list_display = ['team', 'group', 'played', 'won', 'drawn', 'lost', 'points', 'goal_difference']
    list_filter = ['group']
    search_fields = ['team__name']
    readonly_fields = ['played', 'won', 'drawn', 'lost', 'goals_for', 'goals_against', 'points']
    fieldsets = (
        ('Standing Information', {
            'fields': ('team', 'group')
        }),
        ('Statistics', {
            'fields': ('played', 'won', 'drawn', 'lost', 'goals_for', 'goals_against', 'points')
        }),
    )


@admin.register(Ticket)
class TicketAdmin(admin.ModelAdmin):
    list_display = ['match', 'category', 'seat_section', 'status', 'price', 'user']
    list_filter = ['category', 'status', 'match__stadium__city']
    search_fields = ['booking_reference', 'qr_code', 'user__username']


@admin.register(MatchNews)
class MatchNewsAdmin(admin.ModelAdmin):
    list_display = ['title', 'category', 'published_at', 'is_published']
    list_filter = ['category', 'is_published']
    search_fields = ['title', 'content']
    prepopulated_fields = {'slug': ('title',)}
    fieldsets = (
        ('Basic Information', {
            'fields': ('title', 'slug', 'category', 'content', 'excerpt')
        }),
        ('Images', {
            'fields': ('featured_image_url', 'thumbnail_url', 'gallery', 'video_url')
        }),
        ('Related Content', {
            'fields': ('related_match', 'related_team', 'related_player')
        }),
        ('Publication', {
            'fields': ('author', 'is_published')
        }),
    )


@admin.register(UserPrediction)
class UserPredictionAdmin(admin.ModelAdmin):
    list_display = ['user', 'match', 'predicted_home_score', 'predicted_away_score', 'points_earned']
    list_filter = ['match__status']
    search_fields = ['user__username', 'match__home_team__name', 'match__away_team__name']


@admin.register(MatchAlert)
class MatchAlertAdmin(admin.ModelAdmin):
    list_display = ['user', 'match', 'alert_before_minutes', 'is_active']
    list_filter = ['is_active']
    search_fields = ['user__username', 'match__home_team__name']


@admin.register(NewsComment)
class NewsCommentAdmin(admin.ModelAdmin):
    list_display = ['user', 'news', 'created_at', 'is_approved']
    list_filter = ['is_approved', 'created_at']
    search_fields = ['user__username', 'content']