from django.db import models
from django.contrib.auth.models import User
import json

class ChatProfile(models.Model):
    LANGUAGES = [
        ('en', 'English'),
        ('sw', 'Swahili'),
        ('fr', 'French'),
        ('ar', 'Arabic'),
    ]
    
    INTERESTS = [
        ('football', '⚽ Football'),
        ('safari', '🦁 Safari & Wildlife'),
        ('beach', '🏖️ Beach & Relaxation'),
        ('culture', '🎭 Culture & History'),
        ('adventure', '🗻 Adventure & Hiking'),
        ('food', '🍲 Food & Dining'),
        ('shopping', '🛍️ Shopping'),
        ('luxury', '🌟 Luxury Travel'),
    ]
    
    TRAVEL_BUDGET = [
        ('budget', '💰 Budget (< $100/night)'),
        ('midrange', '💵 Mid-range ($100-$300/night)'),
        ('luxury', '💎 Luxury ($300+/night)'),
    ]
    
    TRAVEL_GROUP = [
        ('solo', '👤 Solo Traveler'),
        ('couple', '👫 Couple'),
        ('family', '👨‍👩‍👧‍👦 Family'),
        ('friends', '👥 Friends'),
        ('business', '💼 Business'),
    ]
    
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='chat_profile')
    preferred_language = models.CharField(max_length=2, choices=LANGUAGES, default='en')
    interests = models.CharField(max_length=50, choices=INTERESTS, default='football')
    conversation_count = models.IntegerField(default=0)
    
    # New fields for personalization
    travel_budget = models.CharField(max_length=20, choices=TRAVEL_BUDGET, default='midrange')
    travel_group = models.CharField(max_length=20, choices=TRAVEL_GROUP, default='solo')
    
    # Context memory
    last_hotel_query = models.JSONField(default=dict, blank=True)
    last_tour_query = models.JSONField(default=dict, blank=True)
    preferences = models.JSONField(default=dict, blank=True)  # Store user preferences
    
    # Add last_active field
    last_active = models.DateTimeField(auto_now=True)  # ADDED THIS LINE
    
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.user.username}'s Chat Profile"
    
    def get_interests_display(self):
        return dict(self.INTERESTS).get(self.interests, 'Football')
    
    def get_travel_budget_display(self):
        return dict(self.TRAVEL_BUDGET).get(self.travel_budget, 'Mid-range')
    
    def get_travel_group_display(self):
        return dict(self.TRAVEL_GROUP).get(self.travel_group, 'Solo Traveler')
    
    def add_preference(self, key, value):
        """Add or update user preference"""
        if not self.preferences:
            self.preferences = {}
        self.preferences[key] = value
        self.save()
    
    def get_preference(self, key, default=None):
        """Get user preference"""
        return self.preferences.get(key, default)

class ChatSession(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='chat_sessions')
    session_id = models.CharField(max_length=100, unique=True)
    title = models.CharField(max_length=200, default="New Conversation")
    
    # Context tracking
    context = models.JSONField(default=dict, blank=True)  # Track conversation context
    intent = models.CharField(max_length=50, blank=True)  # Current intent
    entities = models.JSONField(default=list, blank=True)  # Extracted entities
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.user.username} - {self.title}"
    
    def update_context(self, key, value):
        """Update conversation context"""
        if not self.context:
            self.context = {}
        self.context[key] = value
        self.save()
    
    def get_context(self, key, default=None):
        """Get conversation context"""
        return self.context.get(key, default)
    
    class Meta:
        ordering = ['-updated_at']

class ChatMessage(models.Model):
    MESSAGE_TYPES = [
        ('user', 'User'),
        ('bot', 'Bot'),
        ('system', 'System'),
    ]
    
    session = models.ForeignKey(ChatSession, on_delete=models.CASCADE, related_name='messages')
    message_type = models.CharField(max_length=10, choices=MESSAGE_TYPES)
    content = models.TextField()
    
    # Enhanced fields
    intent = models.CharField(max_length=50, blank=True, null=True)  # Detected intent
    entities = models.JSONField(default=dict, blank=True)  # Named entities
    sentiment = models.CharField(max_length=20, default='neutral')  # Sentiment
    confidence = models.FloatField(default=0.8)  # Confidence score
    
    # New fields needed for your view code
    metadata = models.JSONField(default=dict, blank=True)  # Metadata field
    
    timestamp = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['timestamp']
    
    def __str__(self):
        return f"{self.get_message_type_display()}: {self.content[:50]}..."
    
    def add_metadata(self, key, value):
        """Add metadata to message"""
        if not self.metadata:
            self.metadata = {}
        self.metadata[key] = value
        self.save()
    
    def get_metadata(self, key, default=None):
        """Get metadata from message"""
        return self.metadata.get(key, default)