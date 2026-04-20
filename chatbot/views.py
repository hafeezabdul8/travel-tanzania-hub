from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
import json
import uuid
from .models import ChatProfile, ChatSession, ChatMessage
from .dataset_loader import DatasetLoader

# Initialize dataset loader
dataset = DatasetLoader()

def get_bot_response(message, username):
    """Get response using dataset first, fallback to keyword matching"""
    
    # First, try to match from dataset
    intent, intent_data = dataset.match_intent(message)
    
    if intent_data:
        # Found match in dataset
        response = dataset.get_response(intent, intent_data, username)
        if response:
            print(f"📚 Dataset response for intent: {intent}")
            return response
    
    # Fallback responses (only used if dataset doesn't match)
    print("⚠️ No dataset match, using fallback")
    return get_fallback_response(message, username)

def get_bot_response_with_dataset(message, username):
    """Generate response using dataset first, fallback to keyword matching"""
    
    msg_lower = message.lower()
    
    # Special check for Zanzibar transport (priority)
    if 'zanzibar' in msg_lower and any(word in msg_lower for word in ['go', 'reach', 'get', 'how', 'travel', 'ferry', 'flight']):
        # First try to get transport intent
        intent, intent_data = dataset.match_intent(message)
        if intent == 'transport' and intent_data:
            response = dataset.get_response(intent, intent_data, username)
            if response:
                print(f"📚 Dataset response for transport intent: {intent}")
                return response
    
    # First, try to match from dataset normally
    intent, intent_data = dataset.match_intent(message)
    
    if intent_data:
        # Found match in dataset
        response = dataset.get_response(intent, intent_data, username)
        if response:
            print(f"📚 Dataset response for intent: {intent}")
            return response
    
    # Fallback to keyword-based responses
    print("⚠️ No dataset match, using fallback")
    return get_fallback_response(message, username)

def get_fallback_response(message, username):
    """Fallback responses when dataset doesn't match"""
    msg = message.lower().strip()
    
    # Hotel related
    if any(word in msg for word in ['hotel', 'book', 'room', 'stay']):
        if 'dar' in msg:
            return "🏨 **Hotels in Dar es Salaam**\n\n• Serena Hotel - $250/night\n• Hyatt Regency - $220/night\n• Holiday Inn - $120/night\n• Peacock Hotel - $80/night\n\nWhat's your budget?"
        elif 'arusha' in msg:
            return "🏔️ **Hotels in Arusha**\n\n• Arusha Serena - $180/night\n• Mount Meru Hotel - $150/night\n• Kibo Palace - $100/night\n• Arusha Hotel - $70/night"
        elif 'zanzibar' in msg:
            return "🏖️ **Hotels in Zanzibar**\n\n• Zanzibar Serena - $300/night\n• The Residence - $280/night\n• TUI Blue - $150/night\n• Gold Zanzibar - $90/night"
        else:
            return "📍 Which city? Dar es Salaam, Arusha, or Zanzibar?"
    
    # Tourism related
    elif any(word in msg for word in ['safari', 'serengeti', 'animal']):
        return "🦁 **Serengeti National Park**\n\n• World-famous wildebeest migration\n• Big Five animals\n• Safari packages from $200/day\n• Best time: June-October"
    
    elif any(word in msg for word in ['kilimanjaro', 'mountain', 'climb']):
        return "🗻 **Mount Kilimanjaro**\n\n• Africa's highest peak (5,895m)\n• Climbing tours: $1000-2000\n• Routes: Marangu, Machame, Lemosho\n• Best time: Jan-March, June-Oct"
    
    elif any(word in msg for word in ['beach', 'zanzibar']):
        return "🏝️ **Zanzibar Beaches**\n\n• Nungwi - Most popular\n• Kendwa - All-year swimming\n• Paje - Kite surfing\n• Matemwe - Quiet and romantic"
    
    # AFCON related
    elif any(word in msg for word in ['afcon', 'match', 'football']):
        return "⚽ **AFCON 2027**\n\n• Dates: Jan 10 - Feb 10, 2027\n• Host cities: Dar, Arusha, Zanzibar\n• 24 African nations competing\n• Need help with tickets or hotels?"
    
    # Price related
    elif any(word in msg for word in ['price', 'cost', 'budget']):
        return "💰 **Price Guide**\n\n• Budget hotels: $40-100/night\n• Mid-range: $100-200/night\n• Luxury: $200-500/night\n• Food: $3-20 per meal\n• Transport: $5-50"
    
    # Transport related
    elif any(word in msg for word in ['transport', 'taxi', 'bus', 'ferry']):
        return "🚗 **Transportation**\n\n• Taxis: $5-15 per trip\n• Airport transfer: $20-50\n• Bus Dar-Arusha: $15-25 (8hrs)\n• Ferry Dar-Zanzibar: $25-50 (2hrs)"
    
    # Food related
    elif any(word in msg for word in ['food', 'restaurant', 'eat']):
        return "🍲 **Tanzanian Food**\n\n• Ugali - Cornmeal staple\n• Nyama Choma - Grilled meat\n• Zanzibar Pizza - Stuffed pancake\n• Local meals: $3-8"
    
    # Emergency
    elif any(word in msg for word in ['help', 'emergency', 'police', 'hospital']):
        return "🚨 **Emergency**\n\n• Police: 112\n• Ambulance: 114\n• Tourist Police: +255 22 212 3232\n• Aga Khan Hospital (Dar): +255 22 211 5151"
    
    # Greeting
    elif any(word in msg for word in ['hello', 'hi', 'hey', 'jambo']):
        return f"Jambo {username}! 🇹🇿 Welcome to the AFCON 2027 Assistant! I can help with hotels, tourism, matches, and more. What would you like to know?"
    
    # Default
    else:
        return f"""Hi {username}! I can help with:

🏨 **HOTELS** - "Hotel in Dar es Salaam"
🦁 **TOURISM** - "Safari in Serengeti" 
⚽ **AFCON** - "AFCON 2027 schedule"
💰 **PRICES** - "Hotel prices"
🚗 **TRANSPORT** - "Airport transfer"
🍲 **FOOD** - "Local food"
🚨 **EMERGENCY** - "Emergency help"

What would you like to know about AFCON 2027 in Tanzania?"""

@login_required
def chatbot_view(request):
    """Main chatbot view"""
    profile, created = ChatProfile.objects.get_or_create(user=request.user)
    
    session_id = request.GET.get('session', '')
    if session_id:
        try:
            session = ChatSession.objects.get(session_id=session_id, user=request.user)
        except ChatSession.DoesNotExist:
            session = ChatSession.objects.create(
                user=request.user,
                session_id=str(uuid.uuid4()),
                title="New Conversation"
            )
    else:
        session = ChatSession.objects.create(
            user=request.user,
            session_id=str(uuid.uuid4()),
            title="New Conversation"
        )
    
    sessions = ChatSession.objects.filter(user=request.user).order_by('-updated_at')[:10]
    messages = session.messages.all().order_by('timestamp')[:50]
    
    # Get dataset stats
    stats = dataset.get_stats()
    
    context = {
        'profile': profile,
        'session': session,
        'sessions': sessions,
        'messages': messages,
        'dataset_stats': stats,
    }
    return render(request, 'chatbot/chat.html', context)

@login_required
@require_POST
@csrf_exempt
def send_message(request):
    """Process message using dataset-powered responses"""
    try:
        data = json.loads(request.body)
        session_id = data.get('session_id')
        message = data.get('message', '').strip()
        
        if not message:
            return JsonResponse({'error': 'Empty message'}, status=400)
        
        session = ChatSession.objects.get(session_id=session_id, user=request.user)
        
        # Save user message
        ChatMessage.objects.create(
            session=session,
            message_type='user',
            content=message
        )
        
        # Get response using dataset
        response = get_bot_response(message, request.user.username)
        
        # Save bot response
        ChatMessage.objects.create(
            session=session,
            message_type='bot',
            content=response
        )
        
        if session.messages.count() == 2:
            session.title = message[:50] + ('...' if len(message) > 50 else '')
            session.save()
        
        profile, _ = ChatProfile.objects.get_or_create(user=request.user)
        profile.conversation_count += 1
        profile.save()
        
        return JsonResponse({
            'success': True,
            'response': response,
        })
        
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)
    
# Add these imports at the top
from django.contrib.admin.views.decorators import staff_member_required
from django.shortcuts import redirect
from django.contrib import messages
import csv
from pathlib import Path

@staff_member_required
def admin_dashboard(request):
    """Admin dashboard for managing the platform"""
    from hotels.models import Booking, Hotel
    from django.db.models import Sum, Count, Q
    from django.utils import timezone
    from datetime import timedelta
    
    today = timezone.now().date()
    month_ago = today - timedelta(days=30)
    
    # Financial statistics
    total_revenue = Booking.objects.filter(status='confirmed').aggregate(
        total=Sum('total_price'))['total'] or 0
    platform_commission = total_revenue * 0.10  # 10% commission
    
    today_bookings = Booking.objects.filter(
        status='confirmed',
        created_at__date=today
    )
    today_revenue = today_bookings.aggregate(total=Sum('total_price'))['total'] or 0
    today_commission = today_revenue * 0.10
    
    monthly_bookings = Booking.objects.filter(
        status='confirmed',
        created_at__gte=month_ago
    )
    monthly_revenue = monthly_bookings.aggregate(total=Sum('total_price'))['total'] or 0
    monthly_commission = monthly_revenue * 0.10
    
    # Hotel statistics
    top_hotels = Booking.objects.filter(status='confirmed').values(
        'hotel__name', 'hotel__city'
    ).annotate(
        total_bookings=Count('id'),
        total_commission=Sum('total_price') * 0.10
    ).order_by('-total_commission')[:5]
    
    # City statistics
    city_stats = Booking.objects.filter(status='confirmed').values('hotel__city').annotate(
        bookings=Count('id'),
        revenue=Sum('total_price')
    ).order_by('-revenue')
    
    # Recent bookings with commission
    recent_bookings = Booking.objects.filter(status='confirmed').select_related(
        'user', 'hotel'
    ).order_by('-created_at')[:10]
    
    # Add platform commission to each booking
    for booking in recent_bookings:
        booking.platform_commission = booking.total_price * 0.10
    
    context = {
        'today': today,
        'financial_stats': {
            'total_revenue': total_revenue,
            'total_commission': platform_commission,
            'today_revenue': today_revenue,
            'today_commission': today_commission,
            'monthly_revenue': monthly_revenue,
            'monthly_commission': monthly_commission,
        },
        'hotel_stats': {
            'total_bookings': Booking.objects.filter(status='confirmed').count(),
        },
        'top_hotels': top_hotels,
        'city_stats': city_stats,
        'recent_bookings': recent_bookings,
    }
    
    return render(request, 'admin_dashboard.html', context)

@staff_member_required
def add_training_example(request):
    """Add a new training example to the CSV file"""
    if request.method == 'POST':
        text = request.POST.get('text', '').strip()
        intent = request.POST.get('intent', '').strip()
        response = request.POST.get('response', '').strip()
        category = request.POST.get('category', 'general')
        keywords = request.POST.get('keywords', '')
        
        if not text or not intent or not response:
            messages.error(request, 'Please fill in all required fields')
            return redirect('add_training_example')
        
        # Path to CSV file
        csv_path = Path('chatbot/data/training_data.csv')
        
        # Check if file exists
        file_exists = csv_path.exists()
        
        # Append to CSV
        with open(csv_path, 'a', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            if not file_exists:
                writer.writerow(['text', 'intent', 'response', 'category', 'keywords'])
            writer.writerow([text, intent, response, category, keywords])
        
        messages.success(request, f'Training example added successfully! The chatbot will now respond to "{text}"')
        
        # Reload the dataset
        from .dataset_loader import DatasetLoader
        global dataset
        dataset = DatasetLoader()
        
        return redirect('add_training_example')
    
    return render(request, 'chatbot/add_training.html')

@staff_member_required
def training_stats(request):
    """View training statistics"""
    from .dataset_loader import DatasetLoader
    dataset = DatasetLoader()
    stats = dataset.get_stats()
    
    return JsonResponse(stats)