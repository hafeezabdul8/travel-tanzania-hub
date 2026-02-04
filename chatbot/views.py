# chatbot/views.py
import json
import uuid
import logging
import google.genai as genai
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse, HttpResponseServerError
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST, require_http_methods
from django.utils import timezone
from django.conf import settings

from .models import ChatProfile, ChatSession, ChatMessage
from hotels.models import Hotel, Booking
from tourism.models import TouristAttraction

logger = logging.getLogger(__name__)

# ========== GEMINI AI SERVICE ==========
class GeminiAIService:
    """Google Gemini AI Integration"""
    
    def __init__(self):
        self.api_key = getattr(settings, 'GEMINI_API_KEY', None)
        self.model_name = "gemini-pro"
        self.client = None
        
        if self.api_key:
            try:
                self.client = genai.Client(api_key=self.api_key)
                logger.info("Gemini AI Service initialized successfully")
            except Exception as e:
                logger.error(f"Failed to initialize Gemini: {str(e)}")
                self.client = None
        else:
            logger.warning("GEMINI_API_KEY not found, using simple AI fallback")
    
    def generate_response(self, user_message: str, profile_data: dict, context: dict) -> dict:
        """Generate response using Gemini API with fallback"""
        
        # Try Gemini API first if configured
        if self.client:
            try:
                return self._call_gemini_api(user_message, profile_data, context)
            except Exception as e:
                logger.error(f"Gemini API call failed: {str(e)}")
        
        # Fallback to simple AI
        logger.info("Using simple AI fallback")
        simple_service = SimpleAIService()
        return simple_service.generate_response(user_message, profile_data, context)
    
    def _call_gemini_api(self, user_message: str, profile_data: dict, context: dict) -> dict:
        """Call Gemini API directly"""
        
        # Build AFCON 2027 specific prompt
        prompt = self._build_afcon_prompt(user_message, profile_data, context)
        
        # Generate response
        response = self.client.models.generate_content(
            model=self.model_name,
            contents=prompt,
            config={
                "temperature": 0.8,
                "top_p": 0.95,
                "max_output_tokens": 800,
            }
        )
        
        ai_text = response.text.strip()
        
        # Analyze response
        return {
            'text': ai_text,
            'intent': self._detect_intent(ai_text, user_message),
            'sentiment': self._analyze_sentiment(ai_text),
            'entities': self._extract_entities(ai_text),
            'recommendation': self._has_recommendation(ai_text),
            'actions': self._get_actions(ai_text),
            'keywords': self._extract_keywords(ai_text),
            'confidence': 0.95,
            'model': self.model_name,
        }
    
    def _build_afcon_prompt(self, user_message: str, profile_data: dict, context: dict) -> str:
        """Build AFCON 2027 specific prompt for Gemini"""
        
        # User context
        interests = profile_data.get('interests', [])
        budget = profile_data.get('travel_budget', 'midrange')
        group = profile_data.get('travel_group', 'solo')
        
        # Conversation context
        last_intent = context.get('last_intent', '')
        current_city = context.get('city', '')
        step = context.get('step', 1)
        
        # Current date
        current_date = timezone.now().strftime("%B %d, %Y")
        
        prompt = f"""# Role: Safari AI - AFCON 2027 Travel Expert

You are "Safari AI", an expert travel assistant for the Africa Cup of Nations 2027 in Tanzania.

# User Context:
- Interests: {', '.join(interests) if interests else 'Exploring Tanzania'}
- Budget: {budget}
- Travel Group: {group}
- Previous Topic: {last_intent if last_intent else 'New conversation'}
- Current City: {current_city if current_city else 'Open to all Tanzania'}

# Tournament Info:
- Event: Africa Cup of Nations 2027
- Host Country: Tanzania
- Host Cities: Dar es Salaam, Arusha, Zanzibar
- Current Date: {current_date}

# Response Guidelines:
1. Be specific with hotel and attraction names
2. Use emojis appropriately 🇹🇿⚽🏨🦁🏖️
3. Ask follow-up questions
4. Include practical travel tips
5. Keep responses friendly and helpful

# User Message:
"{user_message}"

# Your Response (as Safari AI):
"""
        
        return prompt
    
    def _detect_intent(self, ai_text: str, user_message: str) -> str:
        """Detect intent from text"""
        message_lower = user_message.lower()
        
        if any(word in message_lower for word in ['hotel', 'accommodation', 'stay', 'room']):
            return 'hotel_search'
        elif any(word in message_lower for word in ['attraction', 'tourist', 'visit', 'see', 'place', 'safari']):
            return 'attraction_search'
        elif any(word in message_lower for word in ['afcon', 'football', 'match', 'game', 'stadium']):
            return 'afcon_info'
        elif any(word in message_lower for word in ['book', 'reservation', 'booking']):
            return 'booking'
        elif any(word in message_lower for word in ['hello', 'hi', 'hey', 'greetings']):
            return 'greeting'
        elif any(word in message_lower for word in ['help', 'assist', 'support']):
            return 'help'
        else:
            return 'general'
    
    def _analyze_sentiment(self, text: str) -> str:
        """Simple sentiment analysis"""
        text_lower = text.lower()
        positive_words = ['great', 'excellent', 'wonderful', 'amazing', 'fantastic', 'perfect', 'awesome', 'best']
        negative_words = ['sorry', 'unfortunately', 'cannot', 'problem', 'issue', 'difficult', 'expensive']
        
        pos_count = sum(1 for word in positive_words if word in text_lower)
        neg_count = sum(1 for word in negative_words if word in text_lower)
        
        if pos_count > neg_count:
            return 'positive'
        elif neg_count > pos_count:
            return 'negative'
        return 'neutral'
    
    def _extract_entities(self, text: str) -> dict:
        """Extract entities from text"""
        entities = {'cities': [], 'categories': []}
        text_lower = text.lower()
        
        cities = ['dar es salaam', 'dar', 'arusha', 'zanzibar', 'tanzania']
        for city in cities:
            if city in text_lower:
                entities['cities'].append(city)
        
        categories = ['nature', 'beach', 'culture', 'adventure', 'food', 'shopping', 'wildlife', 'safari']
        for category in categories:
            if category in text_lower:
                entities['categories'].append(category)
        
        return entities
    
    def _has_recommendation(self, text: str) -> bool:
        """Check if text contains recommendations"""
        keywords = ['recommend', 'suggest', 'you should', 'try', 'check out', 'visit', 'must see']
        text_lower = text.lower()
        return any(keyword in text_lower for keyword in keywords)
    
    def _extract_keywords(self, text: str) -> list:
        """Extract important keywords"""
        stop_words = {'the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for', 'of', 'with', 'by'}
        words = text.lower().split()
        keywords = [word for word in words if word not in stop_words and len(word) > 3]
        return list(set(keywords))[:10]
    
    def _get_actions(self, text: str) -> list:
        """Get suggested actions from text"""
        actions = []
        text_lower = text.lower()
        
        if any(word in text_lower for word in ['hotel', 'accommodation', 'stay']):
            actions.extend(['view_hotels', 'compare_prices', 'book_hotel'])
        
        if any(word in text_lower for word in ['attraction', 'tourist', 'visit', 'safari']):
            actions.extend(['view_attractions', 'book_tour', 'get_directions'])
        
        if any(word in text_lower for word in ['afcon', 'football', 'match']):
            actions.extend(['view_match_schedule', 'find_nearby_hotels'])
        
        return actions[:5]

# ========== SIMPLE AI FALLBACK SERVICE ==========
class SimpleAIService:
    """Simple AI service that works without external APIs"""
    
    def generate_response(self, user_message: str, profile_data: dict, context: dict) -> dict:
        """Generate a response based on user message"""
        message_lower = user_message.lower()
        
        # Detect intent
        if any(word in message_lower for word in ['hotel', 'accommodation', 'stay', 'room']):
            return self._hotel_response(message_lower, profile_data)
        elif any(word in message_lower for word in ['attraction', 'tourist', 'visit', 'see', 'place']):
            return self._attraction_response(message_lower, profile_data)
        elif any(word in message_lower for word in ['afcon', 'football', 'match', 'game', 'stadium']):
            return self._afcon_response(message_lower)
        elif any(word in message_lower for word in ['hello', 'hi', 'hey', 'greetings']):
            return self._greeting_response(profile_data)
        elif any(word in message_lower for word in ['help', 'assist', 'support']):
            return self._help_response()
        elif any(word in message_lower for word in ['book', 'reservation', 'booking']):
            return self._booking_response(message_lower)
        elif any(word in message_lower for word in ['safari', 'wildlife', 'animals']):
            return self._safari_response(message_lower)
        else:
            return self._general_response()
    
    def _hotel_response(self, message: str, profile: dict) -> dict:
        """Generate hotel response"""
        cities = {'dar': 'Dar es Salaam', 'arusha': 'Arusha', 'zanzibar': 'Zanzibar'}
        detected_city = None
        
        for city_key, city_name in cities.items():
            if city_key in message:
                detected_city = city_name
                break
        
        if detected_city:
            response = f"🏨 Great choice! {detected_city} has excellent hotels for AFCON 2027. Check our hotel listings in {detected_city}."
        else:
            response = "🏨 I can help you find hotels in Tanzania! Which city are you interested in? (Dar es Salaam, Arusha, or Zanzibar)"
        
        return {
            'text': response,
            'intent': 'hotel_search',
            'sentiment': 'positive',
            'entities': {'city': detected_city} if detected_city else {},
            'recommendation': True,
            'actions': ['view_hotels', 'compare_prices'],
            'keywords': ['hotel', 'accommodation'],
            'confidence': 0.8
        }
    
    def _attraction_response(self, message: str, profile: dict) -> dict:
        """Generate attraction response"""
        categories = {
            'nature': 'Nature & Wildlife',
            'beach': 'Beaches & Coast',
            'culture': 'Culture & History',
            'adventure': 'Adventure & Sports',
            'food': 'Food & Dining',
            'shopping': 'Shopping & Markets'
        }
        
        detected_category = None
        for cat_key, cat_name in categories.items():
            if cat_key in message:
                detected_category = cat_name
                break
        
        if detected_category:
            response = f"🌍 For {detected_category.lower()} experiences in Tanzania, check out Serengeti National Park, Stone Town Zanzibar, and Nungwi Beach!"
        else:
            response = "🌍 Tanzania has amazing attractions! Are you interested in nature, beaches, culture, adventure, food, or shopping?"
        
        return {
            'text': response,
            'intent': 'attraction_search',
            'sentiment': 'positive',
            'entities': {'category': detected_category} if detected_category else {},
            'recommendation': True,
            'actions': ['view_attractions', 'book_tour'],
            'keywords': ['attraction', 'tourist'],
            'confidence': 0.8
        }
    
    def _safari_response(self, message: str) -> dict:
        """Generate safari-specific response"""
        if 'arusha' in message.lower():
            response = "🦁 Perfect! For safaris near Arusha, I recommend Arusha National Park, Tarangire National Park, and Ngorongoro Conservation Area."
        else:
            response = "🦁 Tanzania is safari paradise! The best options are Serengeti National Park, Ngorongoro Crater, and Selous Game Reserve."
        
        return {
            'text': response,
            'intent': 'attraction_search',
            'sentiment': 'positive',
            'entities': {},
            'recommendation': True,
            'actions': ['view_safari_tours', 'book_safari'],
            'keywords': ['safari', 'wildlife'],
            'confidence': 0.9
        }
    
    def _afcon_response(self, message: str) -> dict:
        """Generate AFCON response"""
        response = "⚽ AFCON 2027 in Tanzania will be amazing! Book hotels early near stadiums and plan match day transportation in advance."
        
        return {
            'text': response,
            'intent': 'afcon_info',
            'sentiment': 'positive',
            'entities': {},
            'recommendation': True,
            'actions': ['view_match_schedule', 'find_nearby_hotels'],
            'keywords': ['afcon', 'football'],
            'confidence': 0.9
        }
    
    def _greeting_response(self, profile: dict) -> dict:
        """Generate greeting response"""
        interests = profile.get('interests', [])
        
        if interests:
            response = f"👋 Welcome back! I see you're interested in {', '.join(interests)}. How can I help with your AFCON 2027 trip?"
        else:
            response = "👋 Hello! I'm Safari AI, your AFCON 2027 travel assistant for Tanzania. What would you like to know?"
        
        return {
            'text': response,
            'intent': 'greeting',
            'sentiment': 'positive',
            'entities': {},
            'recommendation': False,
            'actions': ['get_started', 'view_tips'],
            'keywords': ['hello', 'welcome'],
            'confidence': 0.9
        }
    
    def _help_response(self) -> dict:
        """Generate help response"""
        response = "🆘 I can help you with hotels, attractions, AFCON 2027 planning, bookings, and travel tips for Tanzania!"
        
        return {
            'text': response,
            'intent': 'help',
            'sentiment': 'positive',
            'entities': {},
            'recommendation': False,
            'actions': ['view_help', 'contact_support'],
            'keywords': ['help', 'assist'],
            'confidence': 0.9
        }
    
    def _booking_response(self, message: str) -> dict:
        """Generate booking response"""
        response = "📅 I can help with bookings! Tell me what city, travel dates, number of people, and budget."
        
        return {
            'text': response,
            'intent': 'booking',
            'sentiment': 'positive',
            'entities': {},
            'recommendation': False,
            'actions': ['proceed_booking', 'check_availability'],
            'keywords': ['book', 'reservation'],
            'confidence': 0.8
        }
    
    def _general_response(self) -> dict:
        """Generate general response"""
        response = "I'm here to help with your AFCON 2027 trip to Tanzania! You can ask me about hotels, attractions, or travel planning."
        
        return {
            'text': response,
            'intent': 'general',
            'sentiment': 'positive',
            'entities': {},
            'recommendation': False,
            'actions': ['ask_follow_up', 'get_started'],
            'keywords': ['general', 'help'],
            'confidence': 0.7
        }

# Create AI service instance
ai_service = GeminiAIService()

# ========== VIEW FUNCTIONS ==========

@login_required
def chatbot_view(request):
    """Main chatbot interface"""
    try:
        # Get or create chat profile
        profile, created = ChatProfile.objects.get_or_create(user=request.user)
        
        # Get or create session
        session_id = request.GET.get('session', '')
        if session_id:
            session = get_object_or_404(ChatSession, session_id=session_id, user=request.user)
        else:
            # Create new session
            session = ChatSession.objects.create(
                user=request.user,
                session_id=str(uuid.uuid4()),
                title="AFCON 2027 Planning",
                context={
                    'step': 1,
                    'conversation_type': 'afcon_planning',
                    'last_intent': None,
                    'city': None,
                    'interests': profile.interests or [],
                }
            )
        
        # Get user's recent sessions
        sessions = ChatSession.objects.filter(user=request.user).order_by('-updated_at')[:10]
        
        # Get conversation messages
        messages = session.messages.all().order_by('timestamp')
        
        # Get stats for dashboard
        hotels_count = Hotel.objects.count()
        attractions_count = TouristAttraction.objects.count()
        user_bookings = Booking.objects.filter(user=request.user).count() if request.user.is_authenticated else 0
        
        # Check if Gemini is configured
        gemini_configured = bool(getattr(settings, 'GEMINI_API_KEY', None))
        
        context = {
            'profile': profile,
            'session': session,
            'sessions': sessions,
            'messages': messages,
            'hotels_count': hotels_count,
            'attractions_count': attractions_count,
            'user_bookings': user_bookings,
            'ai_service': 'gemini' if gemini_configured else 'simple_ai',
            'gemini_configured': gemini_configured,
        }
        
        return render(request, 'chatbot/chat.html', context)
        
    except Exception as e:
        logger.error(f"Error in chatbot_view: {str(e)}")
        return HttpResponseServerError("Error loading chatbot. Please try again later.")

@login_required
@require_POST
@csrf_exempt
def send_message(request):
    """Handle chat messages"""
    try:
        data = json.loads(request.body)
        session_id = data.get('session_id')
        message = data.get('message', '').strip()
        
        if not message:
            return JsonResponse({'error': 'Message cannot be empty'}, status=400)
        
        if not session_id:
            return JsonResponse({'error': 'Session ID required'}, status=400)
        
        # Get session and profile
        session = get_object_or_404(ChatSession, session_id=session_id, user=request.user)
        profile = ChatProfile.objects.get(user=request.user)
        
        # Prepare profile data
        interests_list = []
        if profile.interests:
            if isinstance(profile.interests, str):
                interests_list = [profile.interests]
            elif isinstance(profile.interests, list):
                interests_list = profile.interests
        
        profile_data = {
            'interests': interests_list,
            'travel_budget': profile.travel_budget,
            'travel_group': profile.travel_group,
        }
        
        # Get conversation context
        context = session.context or {}
        
        # Generate AI response
        ai_analysis = ai_service.generate_response(message, profile_data, context)
        
        # Determine which service was used
        gemini_configured = bool(getattr(settings, 'GEMINI_API_KEY', None))
        used_service = 'gemini' if ('model' in ai_analysis and ai_analysis.get('model') == 'gemini-pro') else 'simple_ai'
        
        # Save user message
        user_message = ChatMessage.objects.create(
            session=session,
            message_type='user',
            content=message,
            intent=ai_analysis.get('intent', 'general'),
            sentiment=ai_analysis.get('sentiment', 'neutral'),
            entities=ai_analysis.get('entities', {}),
            confidence=ai_analysis.get('confidence', 0.8),
            metadata={
                'ai_service': used_service,
                'has_recommendation': ai_analysis.get('recommendation', False),
            }
        )
        
        # Save AI response
        ai_response = ChatMessage.objects.create(
            session=session,
            message_type='bot',
            content=ai_analysis['text'],
            intent=ai_analysis.get('intent', 'general'),
            entities=ai_analysis.get('entities', {}),
            sentiment=ai_analysis.get('sentiment', 'neutral'),
            metadata={
                'recommendation': ai_analysis.get('recommendation', False),
                'actions': ai_analysis.get('actions', []),
                'keywords': ai_analysis.get('keywords', []),
                'model': ai_analysis.get('model', 'simple_ai'),
            }
        )
        
        # Update session context
        if not session.context:
            session.context = {}
        
        # Update city if mentioned
        entities = ai_analysis.get('entities', {})
        if 'cities' in entities and entities['cities']:
            session.context['city'] = entities['cities'][0]
        
        # Update intent tracking
        session.context['last_intent'] = ai_analysis.get('intent', 'general')
        session.context['last_query'] = message
        session.context['step'] = session.context.get('step', 1) + 1
        
        # Update session title if first message
        if session.messages.filter(message_type='user').count() == 1:
            title = f"{message[:30]}..." if len(message) > 30 else message
            session.title = title
        
        session.updated_at = timezone.now()
        session.save()
        
        # Update profile stats
        profile.conversation_count += 1
        profile.save()
        
        # Prepare response
        response_data = {
            'success': True,
            'user_message': {
                'id': user_message.id,
                'content': user_message.content,
                'timestamp': user_message.timestamp.strftime('%I:%M %p'),
                'sentiment': user_message.sentiment,
                'intent': user_message.intent,
                'type': 'user',
            },
            'bot_message': {
                'id': ai_response.id,
                'content': ai_response.content,
                'timestamp': ai_response.timestamp.strftime('%I:%M %p'),
                'intent': ai_response.intent,
                'type': 'bot',
                'has_recommendation': ai_analysis.get('recommendation', False),
                'actions': ai_analysis.get('actions', []),
                'is_ai_generated': True,
                'model': ai_analysis.get('model', 'simple_ai'),
            },
            'analysis': {
                'intent': ai_analysis.get('intent', 'general'),
                'sentiment': ai_analysis.get('sentiment', 'neutral'),
                'keywords': ai_analysis.get('keywords', []),
                'entities': ai_analysis.get('entities', {}),
                'confidence': ai_analysis.get('confidence', 0.8),
            },
            'metadata': {
                'session_id': session.session_id,
                'message_count': session.messages.count(),
                'ai_service': used_service,
                'gemini_used': used_service == 'gemini',
            },
        }
        
        return JsonResponse(response_data)
        
    except Exception as e:
        logger.error(f"Error in send_message: {str(e)}")
        
        error_response = {
            'success': False,
            'error': 'Sorry, I encountered an issue.',
            'fallback_response': "I'm having trouble right now. Please try again in a moment.",
        }
        
        return JsonResponse(error_response, status=500)

# ========== MISSING FUNCTIONS - ADD THESE ==========

@login_required
@require_http_methods(["DELETE"])
@csrf_exempt
def delete_session(request, session_id):
    """Delete a chat session"""
    try:
        session = get_object_or_404(ChatSession, session_id=session_id, user=request.user)
        session.delete()
        return JsonResponse({
            'success': True,
            'message': 'Session deleted successfully'
        })
    except Exception as e:
        logger.error(f"Error deleting session: {str(e)}")
        return JsonResponse({
            'success': False,
            'error': 'Failed to delete session'
        }, status=500)

@login_required
@require_http_methods(["POST"])
@csrf_exempt
def update_profile(request):
    """Update user profile"""
    try:
        profile = ChatProfile.objects.get(user=request.user)
        
        data = json.loads(request.body)
        
        # Update preferences
        if 'language' in data:
            profile.preferred_language = data['language']
        if 'interests' in data and isinstance(data['interests'], list):
            profile.interests = data['interests'][0] if data['interests'] else 'football'
        if 'travel_budget' in data:
            profile.travel_budget = data['travel_budget']
        if 'travel_group' in data:
            profile.travel_group = data['travel_group']
        
        profile.save()
        
        return JsonResponse({
            'success': True,
            'message': 'Profile updated!',
            'profile': {
                'interests': profile.interests,
                'budget': profile.travel_budget,
                'group': profile.travel_group,
                'language': profile.preferred_language
            }
        })
        
    except Exception as e:
        logger.error(f"Error updating profile: {str(e)}")
        return JsonResponse({
            'success': False,
            'error': str(e)
        }, status=400)

@login_required
def get_suggestions(request):
    """Get personalized suggestions"""
    try:
        profile = ChatProfile.objects.get(user=request.user)
        
        suggestions = {
            'hotels': [],
            'attractions': [],
        }
        
        # Hotel suggestions
        budget_map = {
            'budget': (0, 100),
            'midrange': (100, 300),
            'luxury': (300, 1000)
        }
        
        min_price, max_price = budget_map.get(profile.travel_budget, (100, 300))
        hotels = Hotel.objects.filter(price_per_night__gte=min_price, price_per_night__lte=max_price)[:3]
        
        for hotel in hotels:
            suggestions['hotels'].append({
                'id': hotel.id,
                'name': hotel.name,
                'city': hotel.get_city_display(),
                'price': float(hotel.price_per_night),
            })
        
        # Attraction suggestions
        interest_map = {
            'football': ['culture', 'adventure'],
            'safari': ['nature'],
            'beach': ['beach'],
            'culture': ['culture'],
            'adventure': ['adventure', 'nature']
        }
        
        categories = []
        if profile.interests:
            categories = interest_map.get(profile.interests, ['culture', 'nature'])
        
        attractions = TouristAttraction.objects.filter(category__in=categories)[:3]
        
        for attraction in attractions:
            suggestions['attractions'].append({
                'id': attraction.id,
                'name': attraction.name,
                'city': attraction.get_city_display(),
                'category': attraction.get_category_display(),
            })
        
        return JsonResponse({'suggestions': suggestions})
        
    except Exception as e:
        logger.error(f"Error getting suggestions: {str(e)}")
        return JsonResponse({
            'suggestions': {
                'hotels': [],
                'attractions': [],
            }
        })

@login_required
def quick_actions(request):
    """Handle quick actions"""
    try:
        action = request.GET.get('action', '')
        
        if action == 'book_hotel':
            return JsonResponse({
                'action': 'redirect',
                'url': '/hotels/',
                'message': 'Taking you to hotel bookings...'
            })
        
        elif action == 'view_attractions':
            return JsonResponse({
                'action': 'redirect',
                'url': '/tourism/',
                'message': 'Showing tourist attractions...'
            })
        
        elif action == 'my_bookings':
            return JsonResponse({
                'action': 'redirect',
                'url': '/hotels/my-bookings/',
                'message': 'Showing your bookings...'
            })
        
        return JsonResponse({
            'error': 'Unknown action',
            'available_actions': ['book_hotel', 'view_attractions', 'my_bookings']
        }, status=400)
        
    except Exception as e:
        logger.error(f"Error in quick_actions: {str(e)}")
        return JsonResponse({
            'error': 'Action failed'
        }, status=500)

def test_ai_connection(request):
    """Test AI connection"""
    gemini_configured = bool(getattr(settings, 'GEMINI_API_KEY', None))
    
    if gemini_configured:
        return JsonResponse({
            'connected': True,
            'service': 'gemini',
            'message': 'Gemini API is configured',
        })
    else:
        return JsonResponse({
            'connected': False,
            'service': 'simple_ai',
            'message': 'Using simple AI fallback',
        })