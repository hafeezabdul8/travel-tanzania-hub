from django.contrib import admin
from django.urls import path, include
from django.shortcuts import render

def home_view(request):
    return render(request, 'home.html')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home_view, name='home'),
    path('accounts/', include('accounts.urls')),  
    path('hotels/', include('hotels.urls')),
    path('chatbot/', include('chatbot.urls')),
    path('tourism/', include('tourism.urls')),
    path('dashboard/', include('dashboard.urls')),  
    path('partners/', include('partners.urls')),
      
]
