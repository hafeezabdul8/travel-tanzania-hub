import random
import re
import json
from textblob import TextBlob

class AdvancedChatbotAI:
    def __init__(self):
        # Knowledge base
        self.knowledge_base = self.load_knowledge_base()
        
    def load_knowledge_base(self):
        """Load domain-specific knowledge"""
        return {
            'hotels': {
                'dar_es_salaam': [
                    {'name': 'Serena Hotel', 'price': 250, 'rating': 4.8, 'features': ['pool', 'wifi', 'spa']},
                    {'name': 'Hyatt Regency', 'price': 300, 'rating': 4.7, 'features': ['beachfront', 'gym', 'restaurant']},
                    {'name': 'Southern Sun', 'price': 180, 'rating': 4.3, 'features': ['city center', 'pool', 'bar']},
                ],
                'arusha': [
                    {'name': 'Arusha Serena', 'price': 220, 'rating': 4.6, 'features': ['safari tours', 'pool', 'spa']},
                    {'name': 'Mount Meru Hotel', 'price': 150, 'rating': 4.2, 'features': ['mountain view', 'restaurant']},
                    {'name': 'Kibo Palace', 'price': 120, 'rating': 4.0, 'features': ['budget', 'wifi', 'breakfast']},
                ],
                'zanzibar': [
                    {'name': 'Zanzibar Serena', 'price': 280, 'rating': 4.9, 'features': ['beachfront', 'spa', 'diving']},
                    {'name': 'The Residence', 'price': 400, 'rating': 4.8, 'features': ['luxury', 'private pool', 'butler']},
                    {'name': 'Fumba Beach Lodge', 'price': 200, 'rating': 4.5, 'features': ['eco-friendly', 'snorkeling']},
                ]
            },
            'attractions': {
                'dar_es_salaam': ['National Museum', 'Bongoyo Island', 'Kivukoni Fish Market', 'Village Museum'],
                'arusha': ['Mount Kilimanjaro', 'Serengeti National Park', 'Ngorongoro Crater', 'Arusha National Park'],
                'zanzibar': ['Stone Town', 'Prison Island', 'Spice Farms', 'Nungwi Beach', 'Jozani Forest']
            },
            'afcon_info': {
                'dates': 'January - February 2027',
                'venues': ['Benjamin Mkapa Stadium (Dar)', 'Arusha Stadium', 'Amaan Stadium (Zanzibar)'],
                'teams': '24 African nations',
                'tickets': 'Available from October 2026'
            }
        }
    
    def analyze_sentiment(self, text):
        """Analyze sentiment of text"""
        try:
            blob = TextBlob(text)
            return blob.sentiment.polarity  # -1 to 1
        except:
            return 0.0
    
    def detect_intent(self, text):
        """Detect user intent"""
        text_lower = text.lower()
        
        intents = {
            'greeting': ['hello', 'hi', 'hey', 'greetings', 'good morning', 'good afternoon'],
            'farewell': ['bye', 'goodbye', 'see you', 'ciao', 'later'],
            'hotel_booking': ['hotel', 'book hotel', 'accommodation', 'stay', 'room', 'reservation'],
            'tourist_info': ['attraction', 'tourist', 'visit', 'see', 'place', 'sightseeing'],
            'afcon_info': ['match', 'afcon', 'football', 'game', 'schedule', 'fixture', 'team'],
            'transport': ['transport', 'taxi', 'bus', 'car', 'airport', 'transfer'],
            'price': ['price', 'cost', 'expensive', 'cheap', 'budget', 'affordable'],
            'recommendation': ['recommend', 'suggest', 'best', 'good', 'popular', 'top'],
            'help': ['help', 'assist', 'support', 'what can you do'],
            'thanks': ['thanks', 'thank you', 'appreciate'],
            'city_info': ['dar es salaam', 'arusha', 'zanzibar', 'tanzania'],
        }
        
        for intent, keywords in intents.items():
            for keyword in keywords:
                if keyword in text_lower:
                    return intent
        
        # Use pattern matching
        patterns = {
            r'book.*hotel.*': 'hotel_booking',
            r'where.*stay.*': 'hotel_booking',
            r'hotel.*in.*': 'hotel_booking',
            r'what.*see.*': 'tourist_info',
            r'attraction.*': 'tourist_info',
            r'afcon.*match.*': 'afcon_info',
            r'when.*match.*': 'afcon_info',
            r'how much.*': 'price',
            r'cost.*': 'price',
            r'recommend.*': 'recommendation',
            r'best.*': 'recommendation',
        }
        
        for pattern, intent in patterns.items():
            if re.search(pattern, text_lower):
                return intent
        
        return 'general_query'
    
    def extract_keywords(self, text):
        """Extract important keywords"""
        # Simple keyword extraction
        words = text.lower().split()
        stopwords = {'a', 'an', 'the', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for', 'of', 'with', 'by', 'is', 'are', 'was', 'were'}
        keywords = [word for word in words if word not in stopwords and len(word) > 2]
        return list(set(keywords))
    
    def get_recommendation(self, intent, profile, context=None):
        """Get personalized recommendations"""
        budget_map = {
            'budget': {'min': 0, 'max': 100},
            'midrange': {'min': 100, 'max': 300},
            'luxury': {'min': 300, 'max': 1000}
        }
        
        if intent == 'hotel_booking':
            city = context.get('city', 'dar es salaam') if context else 'dar es salaam'
            city_key = city.replace(' ', '_')
            budget = budget_map.get(profile.travel_budget, {'min': 100, 'max': 300})
            
            hotels = self.knowledge_base['hotels'].get(city_key, [])
            filtered_hotels = [h for h in hotels if budget['min'] <= h['price'] <= budget['max']]
            
            if filtered_hotels:
                hotel = random.choice(filtered_hotels)
                return f"Based on your {profile.get_travel_budget_display()} preferences, I recommend {hotel['name']} in {city.title()} (${hotel['price']}/night, ⭐{hotel['rating']}). Features: {', '.join(hotel['features'])}"
        
        elif intent == 'tourist_info':
            city = context.get('city', 'dar es salaam') if context else 'dar es salaam'
            city_key = city.replace(' ', '_')
            attractions = self.knowledge_base['attractions'].get(city_key, [])
            
            if attractions:
                return f"Top attractions in {city.title()}: {', '.join(attractions[:3])}. Which one interests you?"
        
        return None
    
    def generate_response(self, user_message, profile, session_context=None):
        """Generate intelligent response"""
        # Analyze message
        intent = self.detect_intent(user_message)
        sentiment = self.analyze_sentiment(user_message)
        keywords = self.extract_keywords(user_message)
        
        # Get personalized recommendation
        recommendation = self.get_recommendation(intent, profile, session_context)
        
        # Base response structure
        response = {
            'text': '',
            'intent': intent,
            'sentiment': sentiment,
            'entities': [],
            'keywords': keywords,
            'recommendation': recommendation is not None,
            'actions': []
        }
        
        # Generate response based on intent
        if intent == 'greeting':
            greetings = [
                f"Jambo! 👋 Welcome to AFCON 2027 Assistant. I see you're interested in {profile.get_interests_display()}. How can I help?",
                f"Habari yako! Ready for AFCON 2027? As a {profile.get_interests_display()} fan, I have great recommendations!",
                f"Hello {profile.user.username}! 🇹🇿 Welcome to Tanzania AFCON 2027 planning. What can I assist you with today?"
            ]
            response['text'] = random.choice(greetings)
            
        elif intent == 'hotel_booking':
            if recommendation:
                response['text'] = recommendation
                response['actions'].append({'type': 'hotel_booking', 'data': {'recommended': True}})
            else:
                responses = [
                    f"I can help you find the perfect hotel! What's your preferred city? (Dar es Salaam, Arusha, or Zanzibar)",
                    f"Looking for accommodation? Tell me your budget and preferred location for personalized recommendations.",
                    f"Hotels are filling up fast for AFCON 2027! Which city are you planning to stay in?"
                ]
                response['text'] = random.choice(responses)
                
        elif intent == 'tourist_info':
            if recommendation:
                response['text'] = recommendation
            else:
                responses = [
                    f"Tanzania has amazing attractions! Are you interested in wildlife, beaches, or cultural sites?",
                    f"Between matches, explore Tanzania's wonders! What type of attraction interests you?",
                    f"I can recommend tourist spots based on your interest in {profile.get_interests_display()}. Any specific city?"
                ]
                response['text'] = random.choice(responses)
                
        elif intent == 'afcon_info':
            info = self.knowledge_base['afcon_info']
            response['text'] = f"⚽ AFCON 2027 Info:\n• Dates: {info['dates']}\n• Venues: {', '.join(info['venues'])}\n• Teams: {info['teams']}\n• Tickets: {info['tickets']}"
            response['actions'].append({'type': 'afcon_info', 'data': info})
            
        elif intent == 'city_info':
            city_responses = {
                'dar es salaam': "Dar es Salaam is Tanzania's commercial capital with vibrant nightlife and beach resorts. Home to the National Stadium for AFCON finals!",
                'arusha': "Arusha is the safari capital, gateway to Serengeti and Kilimanjaro. Perfect for combining football with wildlife adventures!",
                'zanzibar': "Zanzibar offers pristine beaches, historic Stone Town, and spice tours. A tropical paradise for post-match relaxation!"
            }
            
            for city, city_response in city_responses.items():
                if city in user_message.lower():
                    response['text'] = city_response
                    break
            
            if not response['text']:
                response['text'] = "Tanzania has three amazing host cities: Dar es Salaam (commercial hub), Arusha (safari gateway), and Zanzibar (beach paradise). Which one interests you?"
                
        elif intent == 'recommendation':
            if profile.interests == 'football':
                response['text'] = "⚽ For football fans: Book hotels near stadiums, join fan zones, and don't miss the opening ceremony at National Stadium!"
            elif profile.interests == 'safari':
                response['text'] = "🦁 Safari lovers: Combine AFCON with Serengeti tours. Many hotels offer match-day safari packages!"
            elif profile.interests == 'beach':
                response['text'] = "🏖️ Beach enthusiasts: Zanzibar resorts offer stadium shuttles. Relax on Nungwi Beach between matches!"
            else:
                response['text'] = recommendation or "I'd recommend checking our curated packages that match your interests!"
                
        elif intent == 'farewell':
            farewells = [
                "Kwaheri! Enjoy AFCON 2027 in Tanzania! 🇹🇿",
                "Goodbye! Hope to assist you again with your Tanzania travel plans!",
                "See you later! Don't forget to book early for the best deals!"
            ]
            response['text'] = random.choice(farewells)
            
        elif intent == 'thanks':
            response['text'] = "You're welcome! Karibu Tanzania! Let me know if you need anything else. 🇹🇿"
            
        else:
            # Personalized fallback
            fallbacks = [
                f"I'm your AFCON 2027 assistant. I can help with hotels, attractions, and match info. What specifically do you need?",
                f"Based on your interest in {profile.get_interests_display()}, I think you'd enjoy our curated recommendations. Would you like to see them?",
                "Could you rephrase that? I'm here to help with hotel bookings, tourist attractions, and AFCON 2027 information.",
                "I'm still learning about your needs. Try asking about hotels, tourist spots, or match schedules!"
            ]
            response['text'] = random.choice(fallbacks)
        
        # Add sentiment-based emoji
        if sentiment > 0.3:
            response['text'] += " 😊"
        elif sentiment < -0.3:
            response['text'] += " 😔 Let me know how I can help make your trip better!"
        
        return response

# Singleton instance
ai_service = AdvancedChatbotAI()