from django.urls import path
from . import views

urlpatterns = [
    path('', views.chatbot_view, name='chatbot'),
    path('send/', views.send_message, name='send_message'),
    path('delete-session/<str:session_id>/', views.delete_session, name='delete_session'),
    path('update-profile/', views.update_profile, name='update_profile'),
    path('suggestions/', views.get_suggestions, name='get_suggestions'),
    path('quick-actions/', views.quick_actions, name='quick_actions'),
    path('test-connection/', views.test_ai_connection, name='test_connection'),
]