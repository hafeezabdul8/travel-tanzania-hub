from django.contrib import admin
from .models import ChatProfile, ChatSession, ChatMessage

@admin.register(ChatProfile)
class ChatProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'conversation_count', 'created_at']
    search_fields = ['user__username']

@admin.register(ChatSession)
class ChatSessionAdmin(admin.ModelAdmin):
    list_display = ['user', 'title', 'created_at', 'updated_at']
    list_filter = ['created_at']
    search_fields = ['user__username', 'title']

@admin.register(ChatMessage)
class ChatMessageAdmin(admin.ModelAdmin):
    list_display = ['session', 'message_type', 'content', 'timestamp']
    list_filter = ['message_type', 'timestamp']
    search_fields = ['content']