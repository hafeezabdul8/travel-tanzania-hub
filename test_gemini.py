# test_gemini.py
import os
import sys
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'your_project_name.settings')
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
django.setup()

try:
    from chatbot.gemini_service_v2 import gemini_service
except ImportError:
    from .chatbot.gemini_service_v2 import gemini_service

def test_gemini():
    """Test the Gemini integration"""
    print("🤖 Testing Gemini AI Integration...")
    print("=" * 50)
    
    # Test connection
    print("1. Testing API connection...")
    connected = gemini_service.test_connection()
    print(f"   Connection: {'✅ Connected' if connected else '❌ Failed'}")
    
    if connected:
        # Test responses
        test_cases = [
            "Hello! I'm planning my AFCON 2027 trip to Tanzania.",
            "Find me hotels in Dar es Salaam near the stadium.",
            "What tourist attractions are in Zanzibar?",
            "How can I plan my match days during AFCON?",
            "What's the best time to visit Serengeti?",
        ]
        
        profile_data = {
            'interests': ['football', 'nature', 'culture'],
            'travel_budget': 'midrange',
            'travel_group': 'friends',
        }
        
        context = {
            'step': 1,
            'conversation_type': 'afcon_planning',
            'last_intent': None,
        }
        
        for i, message in enumerate(test_cases, 2):
            print(f"\n{i}. Testing: '{message}'")
            print("-" * 50)
            
            try:
                response = gemini_service.generate_response(message, profile_data, context)
                
                print(f"   Response: {response['text'][:100]}...")
                print(f"   Intent: {response['intent']}")
                print(f"   Sentiment: {response['sentiment']}")
                print(f"   Confidence: {response['confidence']}")
                print(f"   Recommendation: {'✅' if response['recommendation'] else '❌'}")
                print(f"   Model: {response.get('model', 'unknown')}")
                
                # Update context for next test
                context['last_intent'] = response['intent']
                context['step'] += 1
                
            except Exception as e:
                print(f"   ❌ Error: {str(e)}")
    
    print("\n" + "=" * 50)
    print("Test completed!")

if __name__ == "__main__":
    test_gemini()