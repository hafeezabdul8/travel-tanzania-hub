from django.urls import path
from . import views

app_name = 'football'

urlpatterns = [
    
    path('', views.match_schedule, name='match_schedule'),
    path('standings/', views.standings, name='standings'),
    path('teams/', views.teams, name='teams'),
    path('teams/<int:team_id>/', views.team_detail, name='team_detail'),
    path('players/<int:player_id>/', views.player_detail, name='player_detail'),
    path('players/', views.players_list, name='players_list'),
    path('stadiums/', views.stadiums, name='stadiums'),
    path('stadiums/<int:stadium_id>/', views.stadium_detail, name='stadium_detail'),
    path('top-scorers/', views.top_scorers, name='top_scorers'),
    path('matches/<int:match_id>/', views.match_detail, name='match_detail'),
    path('live-scores/', views.live_scores, name='live_scores'),
    path('news/', views.news_list, name='news'),
    path('news/<slug:slug>/', views.news_detail, name='news_detail'),
    path('news/<slug:slug>/comment/', views.add_comment, name='add_comment'),
]