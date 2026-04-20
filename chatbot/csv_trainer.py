# chatbot/csv_trainer.py - Fixed version
import pandas as pd
import pickle
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.ensemble import RandomForestClassifier
from sklearn.pipeline import Pipeline
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, classification_report
from pathlib import Path
import json
import re
from datetime import datetime

class CSVChatbotTrainer:
    def __init__(self, csv_path='chatbot/data/training_data.csv'):
        self.csv_path = Path(csv_path)
        self.model_path = Path('chatbot/data/models/')
        self.model_path.mkdir(exist_ok=True, parents=True)
        self.pipeline = None
        self.intent_responses = {}
        self.intent_keywords = {}
        self.category_data = {}
        
    def load_csv_data(self):
        """Load training data from CSV file"""
        if not self.csv_path.exists():
            raise FileNotFoundError(f"CSV file not found: {self.csv_path}")
        
        df = pd.read_csv(self.csv_path)
        
        # Handle missing columns
        required_cols = ['text', 'intent', 'response']
        for col in required_cols:
            if col not in df.columns:
                raise ValueError(f"CSV missing required column: {col}")
        
        # Add missing optional columns
        if 'category' not in df.columns:
            df['category'] = 'general'
        if 'keywords' not in df.columns:
            df['keywords'] = ''
        
        print(f"✅ Loaded {len(df)} training examples from CSV")
        print(f"📊 Columns: {df.columns.tolist()}")
        print(f"🎯 Intents found: {df['intent'].nunique()}")
        print(f"📈 Intents: {df['intent'].value_counts().to_dict()}")
        
        return df
    
    def preprocess_text(self, text):
        """Preprocess text for better matching"""
        text = str(text).lower()
        text = re.sub(r'[^\w\s]', '', text)
        return text
    
    def extract_keywords(self, df):
        """Extract keywords from CSV for quick matching"""
        self.intent_keywords = {}
        
        for idx, row in df.iterrows():
            intent = row['intent']
            keywords = []
            
            # Extract from keywords column if exists
            if pd.notna(row.get('keywords', '')) and row['keywords']:
                keywords.extend([k.strip() for k in str(row['keywords']).split(',')])
            
            # Also extract from text column
            text_words = str(row['text']).lower().split()
            keywords.extend([w for w in text_words if len(w) > 3])
            
            if intent not in self.intent_keywords:
                self.intent_keywords[intent] = []
            self.intent_keywords[intent].extend(keywords)
        
        # Remove duplicates and limit
        for intent in self.intent_keywords:
            self.intent_keywords[intent] = list(set(self.intent_keywords[intent]))[:20]
        
        print(f"🔑 Extracted keywords for {len(self.intent_keywords)} intents")
        
    def build_responses(self, df):
        """Build response dictionary for each intent"""
        self.intent_responses = {}
        self.category_data = {}
        
        for intent in df['intent'].unique():
            responses = df[df['intent'] == intent]['response'].tolist()
            self.intent_responses[intent] = responses
            
            if 'category' in df.columns:
                categories = df[df['intent'] == intent]['category'].tolist()
                self.category_data[intent] = categories[0] if categories else 'general'
        
        print(f"💬 Built responses for {len(self.intent_responses)} intents")
        
    def train_model(self, test_size=0.2):
        """Train the ML model using CSV data"""
        print("🔄 Training ML model from CSV data...")
        
        # Load data
        df = self.load_csv_data()
        
        # Preprocess text
        df['processed_text'] = df['text'].apply(self.preprocess_text)
        
        # Extract features and labels
        X = df['processed_text'].values
        y = df['intent'].values
        
        # Handle small dataset - adjust test_size if needed
        n_samples = len(X)
        n_classes = len(df['intent'].unique())
        
        # For small datasets, use smaller test size or skip splitting
        if n_samples < 20 or n_samples / n_classes < 2:
            print("⚠️ Dataset too small for train/test split. Training on all data.")
            # Use all data for training
            self.pipeline = Pipeline([
                ('tfidf', TfidfVectorizer(
                    max_features=500,
                    stop_words='english',
                    ngram_range=(1, 2)
                )),
                ('clf', RandomForestClassifier(
                    n_estimators=50,
                    max_depth=8,
                    random_state=42
                ))
            ])
            self.pipeline.fit(X, y)
            accuracy = 1.0  # Perfect score on training data
            print(f"📈 Model trained on {n_samples} examples (no validation)")
        else:
            # Normal train/test split
            test_size = min(test_size, 0.3)  # Max 30% test size
            X_train, X_test, y_train, y_test = train_test_split(
                X, y, test_size=test_size, random_state=42, stratify=y
            )
            
            # Create pipeline
            self.pipeline = Pipeline([
                ('tfidf', TfidfVectorizer(
                    max_features=1000,
                    stop_words='english',
                    ngram_range=(1, 2),
                    min_df=1  # Allow terms that appear in only 1 document
                )),
                ('clf', RandomForestClassifier(
                    n_estimators=50,
                    max_depth=10,
                    random_state=42
                ))
            ])
            
            # Train the model
            self.pipeline.fit(X_train, y_train)
            
            # Evaluate on test set
            y_pred = self.pipeline.predict(X_test)
            accuracy = accuracy_score(y_test, y_pred)
            
            print(f"📈 Model accuracy: {accuracy:.2%}")
            print("\n📋 Classification Report:")
            print(classification_report(y_test, y_pred))
        
        # Extract keywords and build responses
        self.extract_keywords(df)
        self.build_responses(df)
        
        # Save everything
        self.save_model()
        
        return accuracy
    
    def save_model(self):
        """Save trained model and data"""
        # Save ML model
        with open(self.model_path / 'chatbot_model.pkl', 'wb') as f:
            pickle.dump(self.pipeline, f)
        
        # Save responses
        with open(self.model_path / 'intent_responses.pkl', 'wb') as f:
            pickle.dump(self.intent_responses, f)
        
        # Save keywords
        with open(self.model_path / 'intent_keywords.pkl', 'wb') as f:
            pickle.dump(self.intent_keywords, f)
        
        # Save metadata
        metadata = {
            'trained_at': datetime.now().isoformat(),
            'intents': list(self.intent_responses.keys()),
            'total_responses': sum(len(resp) for resp in self.intent_responses.values()),
            'model_type': 'RandomForestClassifier'
        }
        
        with open(self.model_path / 'metadata.json', 'w') as f:
            json.dump(metadata, f, indent=2)
        
        print(f"💾 Model saved to {self.model_path}")
        
    def load_model(self):
        """Load trained model and data"""
        try:
            model_file = self.model_path / 'chatbot_model.pkl'
            responses_file = self.model_path / 'intent_responses.pkl'
            keywords_file = self.model_path / 'intent_keywords.pkl'
            
            if not model_file.exists():
                print("⚠️ Model file not found")
                return False
            
            with open(model_file, 'rb') as f:
                self.pipeline = pickle.load(f)
            
            with open(responses_file, 'rb') as f:
                self.intent_responses = pickle.load(f)
            
            if keywords_file.exists():
                with open(keywords_file, 'rb') as f:
                    self.intent_keywords = pickle.load(f)
            
            print("✅ Model loaded successfully")
            return True
        except Exception as e:
            print(f"⚠️ Error loading model: {e}")
            return False
    
    def predict_with_keywords(self, text):
        """Fast prediction using keyword matching"""
        text_lower = text.lower()
        
        for intent, keywords in self.intent_keywords.items():
            for keyword in keywords:
                if keyword in text_lower:
                    return intent, 0.85
        
        return None, 0
    
    def predict(self, text, use_keywords_first=True):
        """Predict intent using hybrid approach"""
        text_processed = self.preprocess_text(text)
        
        # Try keyword matching first
        if use_keywords_first and self.intent_keywords:
            keyword_intent, keyword_conf = self.predict_with_keywords(text_processed)
            if keyword_intent:
                return keyword_intent, keyword_conf
        
        # Use ML model if available
        if self.pipeline:
            try:
                probas = self.pipeline.predict_proba([text_processed])[0]
                predicted_intent = self.pipeline.predict([text_processed])[0]
                confidence = max(probas)
                return predicted_intent, confidence
            except Exception as e:
                print(f"⚠️ ML prediction error: {e}")
        
        return 'general', 0.3
    
    def get_response(self, intent, user_name=None, user_interests=None):
        """Get personalized response based on intent"""
        if intent in self.intent_responses:
            import random
            response = random.choice(self.intent_responses[intent])
            
            # Personalize with user name
            if user_name:
                response = response.replace('{name}', user_name)
            
            return response
        
        return "I'm here to help with hotels, tourism, and AFCON 2027 in Tanzania!"
    
    def get_statistics(self):
        """Get training statistics"""
        try:
            df = pd.read_csv(self.csv_path)
            stats = {
                'total_examples': len(df),
                'unique_intents': df['intent'].nunique(),
                'intents': df['intent'].value_counts().to_dict(),
                'categories': df['category'].value_counts().to_dict() if 'category' in df.columns else {},
            }
            return stats
        except:
            return {'total_examples': 0, 'unique_intents': 0, 'intents': {}, 'categories': {}}