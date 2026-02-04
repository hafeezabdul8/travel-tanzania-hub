from django.contrib import admin
from .models import ChatProfile, ChatSession, ChatMessage

@admin.register(ChatProfile)
class ChatProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'preferred_language', 'interests', 'conversation_count']
    list_filter = ['preferred_language', 'interests']
    search_fields = ['user__username']

class ChatMessageInline(admin.TabularInline):
    model = ChatMessage
    extra = 0
    readonly_fields = ['timestamp']

@admin.register(ChatSession)
class ChatSessionAdmin(admin.ModelAdmin):
    list_display = ['user', 'title', 'created_at', 'message_count']
    list_filter = ['created_at']
    search_fields = ['user__username', 'title']
    inlines = [ChatMessageInline]
    readonly_fields = ['created_at', 'updated_at']
    
    def message_count(self, obj):
        return obj.messages.count()
    message_count.short_description = 'Messages'