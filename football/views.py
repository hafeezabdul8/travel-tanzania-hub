from django.shortcuts import redirect, render, get_object_or_404
from django.db.models import Q, Count
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.views.decorators.http import require_GET
from django.contrib import messages
from .models import Team, Player, Stadium, Match, Goal, GroupStanding, Ticket, MatchNews, NewsComment

def match_schedule(request):
    """View all matches"""
    matches = Match.objects.select_related('home_team', 'away_team', 'stadium').all()
    
    # Filter by status
    status = request.GET.get('status', '')
    if status:
        matches = matches.filter(status=status)
    
    # Filter by match type
    match_type = request.GET.get('type', '')
    if match_type:
        matches = matches.filter(match_type=match_type)
    
    # Group matches by date
    matches_by_date = {}
    for match in matches:
        date_str = match.date.strftime('%Y-%m-%d')
        if date_str not in matches_by_date:
            matches_by_date[date_str] = []
        matches_by_date[date_str].append(match)
    
    context = {
        'matches_by_date': matches_by_date,
        'status_filter': status,
        'type_filter': match_type,
    }
    return render(request, 'football/match_schedule.html', context)

def standings(request):
    """Group standings view"""
    groups = ['A', 'B', 'C', 'D', 'E', 'F']
    standings_data = {}
    
    for group in groups:
        standings = GroupStanding.objects.filter(group=group).select_related('team')
        standings_data[group] = standings
    
    context = {
        'standings_data': standings_data,
        'groups': groups,
    }
    return render(request, 'football/standings.html', context)

def teams(request):
    """List all teams"""
    teams = Team.objects.all().prefetch_related('players')
    
    # Filter by group
    group = request.GET.get('group', '')
    if group:
        teams = teams.filter(group=group)
    
    # Search
    search = request.GET.get('search', '')
    if search:
        teams = teams.filter(Q(name__icontains=search) | Q(short_name__icontains=search))
    
    context = {
        'teams': teams,
        'groups': ['A', 'B', 'C', 'D', 'E', 'F'],
        'selected_group': group,
        'search_query': search,
    }
    return render(request, 'football/teams.html', context)

def team_detail(request, team_id):
    """Team detail page"""
    team = get_object_or_404(Team, id=team_id)
    players = team.players.all().order_by('jersey_number')
    matches = Match.objects.filter(
        Q(home_team=team) | Q(away_team=team)
    ).select_related('home_team', 'away_team', 'stadium')[:10]
    
    # Top scorers from this team
    top_scorers = Player.objects.filter(team=team).order_by('-goals')[:5]
    
    context = {
        'team': team,
        'players': players,
        'matches': matches,
        'top_scorers': top_scorers,
    }
    return render(request, 'football/team_detail.html', context)

def player_detail(request, player_id):
    """Player detail page"""
    player = get_object_or_404(Player, id=player_id)
    goals = player.player_goals.all().select_related('match')[:20]
    
    context = {
        'player': player,
        'goals': goals,
    }
    return render(request, 'football/player_detail.html', context)

def stadiums(request):
    """List all stadiums"""
    stadiums = Stadium.objects.all().prefetch_related('nearby_hotels')
    
    # Filter by city
    city = request.GET.get('city', '')
    if city:
        stadiums = stadiums.filter(city__icontains=city)
    
    context = {
        'stadiums': stadiums,
        'cities': ['Dar es Salaam', 'Arusha', 'Zanzibar'],
        'selected_city': city,
    }
    return render(request, 'football/stadiums.html', context)

def stadium_detail(request, stadium_id):
    """Stadium detail page"""
    stadium = get_object_or_404(Stadium, id=stadium_id)
    matches = stadium.matches.all().select_related('home_team', 'away_team')[:10]
    nearby_hotels = stadium.nearby_hotels.all()
    
    context = {
        'stadium': stadium,
        'matches': matches,
        'nearby_hotels': nearby_hotels,
    }
    return render(request, 'football/stadium_detail.html', context)

def top_scorers(request):
    """Top scorers leaderboard"""
    top_scorers = Player.objects.filter(goals__gt=0).order_by('-goals', '-assists')[:20]
    
    context = {
        'top_scorers': top_scorers,
    }
    return render(request, 'football/top_scorers.html', context)

def match_detail(request, match_id):
    """Match detail page"""
    match = get_object_or_404(Match, id=match_id)
    goals = match.goals.all().select_related('player', 'team')
    
    context = {
        'match': match,
        'goals': goals,
    }
    return render(request, 'football/match_detail.html', context)

@login_required
@require_GET
def live_scores(request):
    """Live scores API endpoint"""
    live_matches = Match.objects.filter(status='live').select_related('home_team', 'away_team')
    
    data = []
    for match in live_matches:
        data.append({
            'id': match.id,
            'home_team': match.home_team.name,
            'away_team': match.away_team.name,
            'home_score': match.home_score or 0,
            'away_score': match.away_score or 0,
            'minute': 'Live',
            'status': match.status,
        })
    
    return JsonResponse({'matches': data})


def news_list(request):
    """AFCON news list"""
    news = MatchNews.objects.filter(is_published=True).select_related('related_match', 'related_team')
    
    # Filter by category
    category = request.GET.get('category', '')
    if category:
        news = news.filter(category=category)
    
    # Add a method to get image URL for each news item
    for item in news:
        # Use featured_image_url instead of featured_image
        if item.featured_image_url:
            item.image_url = item.featured_image_url
        else:
            item.image_url = None
    
    context = {
        'news': news,
        'categories': MatchNews.NEWS_CATEGORY,
        'selected_category': category,
    }
    return render(request, 'football/news.html', context)

def news_detail(request, slug):
    """News detail page"""
    news = get_object_or_404(MatchNews, slug=slug, is_published=True)
    
    # Get related news (same category, excluding current)
    related_news = MatchNews.objects.filter(
        category=news.category,
        is_published=True
    ).exclude(id=news.id)[:3]
    
    # Get comments
    comments = news.comments.filter(is_approved=True)[:20]
    
    context = {
        'news': news,
        'related_news': related_news,
        'comments': comments,
    }
    return render(request, 'football/news_detail.html', context)

from django.core.paginator import Paginator

def players_list(request):
    """List all players with filtering"""
    players = Player.objects.select_related('team').all()
    
    # Filter by team
    team_id = request.GET.get('team', '')
    if team_id:
        players = players.filter(team_id=team_id)
    
    # Filter by position
    position = request.GET.get('position', '')
    if position:
        players = players.filter(position=position)
    
    # Search by name
    search = request.GET.get('search', '')
    if search:
        players = players.filter(name__icontains=search)
    
    # Sorting
    sort_by = request.GET.get('sort', 'name')
    if sort_by == 'goals':
        players = players.order_by('-goals', '-assists')
    elif sort_by == 'assists':
        players = players.order_by('-assists', '-goals')
    elif sort_by == 'jersey_number':
        players = players.order_by('jersey_number')
    else:
        players = players.order_by('name')
    
    # Get top stats
    top_scorer = Player.objects.order_by('-goals').first()
    top_assister = Player.objects.order_by('-assists').first()
    most_appearances = Player.objects.order_by('-appearances').first()
    
    # Pagination
    paginator = Paginator(players, 24)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    # Get all teams for filter dropdown
    teams = Team.objects.all().order_by('name')
    
    context = {
        'players': page_obj,
        'teams': teams,
        'top_scorer': top_scorer,
        'top_assister': top_assister,
        'most_appearances': most_appearances,
        'selected_team': team_id,
        'selected_position': position,
        'sort_by': sort_by,
        'search_query': search,
    }
    return render(request, 'football/players_list.html', context)

from django.core.paginator import Paginator

def players_list(request):
    """List all players with filtering and pagination"""
    players = Player.objects.select_related('team').all()
    
    # Filter by team
    team_id = request.GET.get('team', '')
    if team_id:
        players = players.filter(team_id=team_id)
    
    # Filter by position
    position = request.GET.get('position', '')
    if position:
        players = players.filter(position=position)
    
    # Search by name
    search = request.GET.get('search', '')
    if search:
        players = players.filter(name__icontains=search)
    
    # Sorting
    sort_by = request.GET.get('sort', 'name')
    if sort_by == 'goals':
        players = players.order_by('-goals', '-assists')
    elif sort_by == 'assists':
        players = players.order_by('-assists', '-goals')
    elif sort_by == 'jersey_number':
        players = players.order_by('jersey_number')
    else:
        players = players.order_by('name')
    
    # Get top stats
    top_scorer = Player.objects.order_by('-goals').first()
    top_assister = Player.objects.order_by('-assists').first()
    most_appearances = Player.objects.order_by('-appearances').first()
    
    # Pagination
    paginator = Paginator(players, 24)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    # Get all teams for filter dropdown
    teams = Team.objects.all().order_by('name')
    
    context = {
        'players': page_obj,
        'teams': teams,
        'top_scorer': top_scorer,
        'top_assister': top_assister,
        'most_appearances': most_appearances,
        'selected_team': team_id,
        'selected_position': position,
        'sort_by': sort_by,
        'search_query': search,
    }
    return render(request, 'football/players_list.html', context)


@login_required
def add_comment(request, slug):
    """Add a comment to a news article"""
    news = get_object_or_404(MatchNews, slug=slug)
    
    if request.method == 'POST':
        content = request.POST.get('comment', '').strip()
        
        if content:
            NewsComment.objects.create(
                news=news,
                user=request.user,
                content=content
            )
            messages.success(request, 'Your comment has been posted!')
        else:
            messages.error(request, 'Comment cannot be empty.')
    
    return redirect('football:news_detail', slug=slug)