# chatbot/dataset_loader.py
import csv
import random
from pathlib import Path

class DatasetLoader:
    def __init__(self, csv_path='chatbot/data/training_data.csv'):
        self.csv_path = Path(csv_path)
        self.intents = {}
        self.load_dataset()
    
    def load_dataset(self):
        """Load intents from CSV file"""
        if not self.csv_path.exists():
            print(f"⚠️ Dataset not found at {self.csv_path}")
            print("Using default responses")
            return
        
        with open(self.csv_path, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                intent = row['intent']
                
                if intent not in self.intents:
                    self.intents[intent] = {
                        'patterns': [],
                        'responses': [],
                        'category': row.get('category', 'general')
                    }
                
                # Add pattern from text column
                if 'text' in row and row['text']:
                    self.intents[intent]['patterns'].append(row['text'].lower())
                
                # Add response
                if 'response' in row and row['response']:
                    self.intents[intent]['responses'].append(row['response'])
        
        print(f"✅ Loaded {len(self.intents)} intents from dataset")
        for intent, data in self.intents.items():
            print(f"   - {intent}: {len(data['patterns'])} patterns, {len(data['responses'])} responses")
    
    def match_intent(self, message):
        """Match user message to intent using enhanced keyword matching"""
        message_lower = message.lower()
        
        # First, check for transport to Zanzibar specifically
        if 'zanzibar' in message_lower or 'zan' in message_lower:
            if any(word in message_lower for word in ['go', 'reach', 'get', 'how', 'travel', 'ferry', 'flight', 'boat', 'plane']):
                return 'transport', self.intents.get('transport')
        
        # Check each intent
        for intent, data in self.intents.items():
            for pattern in data['patterns']:
                # Exact pattern match
                if pattern in message_lower:
                    return intent, data
                
                # Word-by-word matching for better accuracy
                pattern_words = pattern.split()
                matched_words = 0
                total_words = len(pattern_words)
                
                for word in pattern_words:
                    if len(word) > 2 and word in message_lower:
                        matched_words += 1
                
                # If more than 60% of words match
                if total_words > 0 and matched_words / total_words >= 0.6:
                    return intent, data
        
        return None, None
    
    def get_response(self, intent, data=None, username=None):
        """Get random response for intent"""
        if data is None and intent in self.intents:
            data = self.intents[intent]
        
        if data and data['responses']:
            response = random.choice(data['responses'])
            if username:
                response = response.replace('{name}', username)
            return response
        
        return None
    
    def get_all_intents(self):
        """Return all available intents"""
        return list(self.intents.keys())
    
    def get_stats(self):
        """Get dataset statistics"""
        total_patterns = sum(len(data['patterns']) for data in self.intents.values())
        total_responses = sum(len(data['responses']) for data in self.intents.values())
        
        return {
            'intents': len(self.intents),
            'patterns': total_patterns,
            'responses': total_responses,
            'categories': list(set(data['category'] for data in self.intents.values()))
        }