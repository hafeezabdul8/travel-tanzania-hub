# chatbot/gemini_service_v2.py
import google.generativeai as genai
import os
import json
import logging
from typing import Dict, List, Optional
from django.conf import settings
from datetime import datetime

logger = logging.getLogger(__name__)

class GeminiAIService:
    """Google Gemini AI Integration for AFCON 2027 Chatbot (Updated for google-genai)"""
    
    def __init__(self):
        """Initialize Gemini AI with AFCON 2027 context"""
        try:
            # Configure Gemini
            api_key = getattr(settings, 'GEMINI_API_KEY', None)
            if not api_key:
                logger.warning("GEMINI_API_KEY not found in settings. Using fallback mode.")
                raise ValueError("API key not configured")
            
            # Configure with new API
            genai.configure(api_key=api_key)
            
            # Set up the model - Using gemini-1.5-flash for speed and free tier
            self.model_name = "gemini-1.5-flash"  # Free tier friendly
            self.model = genai.GenerativeModel(self.model_name)
            
            # AFCON 2027 system prompt
            self.system_prompt = self._create_system_prompt()
            
            logger.info(f"Gemini AI Service initialized successfully with model: {self.model_name}")
            
        except Exception as e:
            logger.error(f"Failed to initialize Gemini AI: {str(e)}")
            raise
    
    def _create_system_prompt(self) -> str:
        """Create the system prompt for AFCON 2027 context"""
        current_date = datetime.now().strftime("%B %d, %Y")
        
        return f"""You are Safari AI, an expert travel assistant for AFCON 2027 in Tanzania.
        
CONTEXT:
- Tournament: Africa Cup of Nations 2027
- Host Country: Tanzania
- Host Cities: Dar es Salaam, Arusha, Zanzibar
- Current Date: {current_date}

YOUR ROLE:
- Help users find hotels, attractions, and plan their trip
- Provide specific recommendations with details
- Offer practical travel tips for Tanzania
- Be enthusiastic about football and Tanzanian culture
- Use emojis occasionally to make responses engaging

RESPONSE STYLE:
- Friendly and helpful tone
- Provide specific names when recommending places
- Ask follow-up questions to understand needs better
- Keep responses concise but informative
- Format lists with bullet points when helpful

EXAMPLE RESPONSES:
User: "Find hotels in Dar es Salaam"
You: "Great choice for AFCON 2027! 🏨 Dar es Salaam has excellent hotels:
• Sea Cliff Hotel - Luxury with ocean views, near Benjamin Mkapa Stadium
• Hyatt Regency - Modern amenities in city center
• Southern Sun - Great value with pool

Tip: Book early as hotels fill up fast during AFCON!"

User: "What to do in Zanzibar?"
You: "Zanzibar is paradise! Beyond football: 🌴
• Stone Town - UNESCO site with rich history
• Nungwi Beach - Perfect white sand beaches
• Spice Tour - Discover why it's called Spice Island
• Jozani Forest - See rare red colobus monkeys

Want help planning day trips?"

Now respond to the user's query based on this context and style."""
    
    def generate_response(self, user_message: str, profile_data: Dict, context: Dict) -> Dict:
        """Generate AI response using Gemini API"""
        try:
            # Prepare conversation history
            conversation = []
            
            # Add system prompt
            conversation.append({
                "role": "user",
                "parts": [self.system_prompt]
            })
            conversation.append({
                "role": "model", 
                "parts": ["I understand. I'm ready to help as Safari AI for AFCON 2027 Tanzania!"]
            })
            
            # Add profile context if available
            if profile_data:
                context_msg = "User Profile:\n"
                if profile_data.get('interests'):
                    context_msg += f"Interests: {', '.join(profile_data['interests'])}\n"
                if profile_data.get('travel_budget'):
                    context_msg += f"Budget: {profile_data['travel_budget']}\n"
                
                conversation.append({
                    "role": "user",
                    "parts": [context_msg]
                })
                conversation.append({
                    "role": "model",
                    "parts": ["Thanks for sharing your profile! I'll personalize my recommendations."]
                })
            
            # Add user message
            conversation.append({
                "role": "user",
                "parts": [user_message]
            })
            
            # Generate response
            response = self.model.generate_content(conversation)
            
            ai_text = response.text.strip()
            
            # Analyze the response
            analysis = self._analyze_response(ai_text, user_message)
            
            return {
                'text': ai_text,
                'intent': analysis['intent'],
                'sentiment': analysis['sentiment'],
                'entities': analysis['entities'],
                'recommendation': analysis['has_recommendation'],
                'actions': analysis['actions'],
                'keywords': analysis['keywords'],
                'confidence': 0.9,
                'model': self.model_name,
            }
            
        except Exception as e:
            logger.error(f"Gemini API error: {str(e)}", exc_info=True)
            return self._get_fallback_response(user_message)
    
    def _analyze_response(self, ai_text: str, user_message: str) -> Dict:
        """Analyze the AI response for metadata"""
        text_lower = ai_text.lower()
        user_lower = user_message.lower()
        
        # Detect intent
        intent = self._detect_intent(user_lower, text_lower)
        
        # Analyze sentiment
        sentiment = self._analyze_sentiment(text_lower)
        
        # Check for recommendations
        has_recommendation = any(keyword in text_lower for keyword in [
            'recommend', 'suggest', 'you should', 'try', 'check out', 'visit'
        ])
        
        # Extract simple entities
        entities = {
            'cities': [],
            'categories': []
        }
        
        cities = ['dar es salaam', 'dar', 'arusha', 'zanzibar']
        for city in cities:
            if city in text_lower:
                entities['cities'].append(city)
        
        # Extract actions
        actions = []
        if intent == 'hotel':
            actions = ['view_hotels', 'compare_prices']
        elif intent == 'attraction':
            actions = ['view_attractions', 'get_directions']
        
        # Extract keywords
        keywords = self._extract_keywords(ai_text)
        
        return {
            'intent': intent,
            'sentiment': sentiment,
            'entities': entities,
            'has_recommendation': has_recommendation,
            'actions': actions,
            'keywords': keywords,
        }
    
    def _detect_intent(self, user_message: str, ai_response: str) -> str:
        """Detect the intent of the conversation"""
        if any(word in user_message for word in ['hotel', 'accommodation', 'stay', 'room']):
            return 'hotel'
        elif any(word in user_message for word in ['attraction', 'tourist', 'visit', 'see', 'place']):
            return 'attraction'
        elif any(word in user_message for word in ['afcon', 'football', 'match', 'game']):
            return 'afcon'
        elif any(word in user_message for word in ['book', 'reservation']):
            return 'booking'
        elif any(word in user_message for word in ['hello', 'hi', 'hey']):
            return 'greeting'
        
        return 'general'
    
    def _analyze_sentiment(self, text: str) -> str:
        """Simple sentiment analysis"""
        positive_words = ['great', 'excellent', 'wonderful', 'amazing', 'fantastic']
        negative_words = ['sorry', 'unfortunately', 'cannot', 'problem']
        
        if any(word in text for word in positive_words):
            return 'positive'
        elif any(word in text for word in negative_words):
            return 'negative'
        return 'neutral'
    
    def _extract_keywords(self, text: str) -> List[str]:
        """Extract important keywords from text"""
        stop_words = {'the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to'}
        words = text.lower().split()
        keywords = [word for word in words if word not in stop_words and len(word) > 3]
        return list(set(keywords))[:5]
    
    def _get_fallback_response(self, user_message: str) -> Dict:
        """Provide a fallback response when Gemini fails"""
        message_lower = user_message.lower()
        
        if 'hotel' in message_lower:
            response = "I can help you find hotels in Tanzania! Which city are you interested in? 🏨"
            intent = 'hotel'
        elif 'attraction' in message_lower:
            response = "Tanzania has incredible attractions! What type of experience are you looking for? 🦁"
            intent = 'attraction'
        elif 'afcon' in message_lower:
            response = "AFCON 2027 in Tanzania will be amazing! Need help with match planning? ⚽"
            intent = 'afcon'
        else:
            response = "Hello! I'm your AFCON 2027 travel assistant. How can I help today? 😊"
            intent = 'greeting'
        
        return {
            'text': response,
            'intent': intent,
            'sentiment': 'positive',
            'entities': {},
            'recommendation': False,
            'actions': [],
            'keywords': [],
            'confidence': 0.7,
            'model': 'fallback',
        }
    
    def test_connection(self) -> bool:
        """Test the Gemini API connection"""
        try:
            test_prompt = "Hello! Are you working?"
            response = self.model.generate_content(test_prompt)
            return response.text is not None
        except Exception as e:
            logger.error(f"Gemini connection test failed: {str(e)}")
            return False


# Create singleton instance
gemini_service = GeminiAIService()