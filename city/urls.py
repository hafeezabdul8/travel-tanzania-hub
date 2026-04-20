from django.urls import path
from . import views

app_name = 'city'

urlpatterns = [
    path('<slug:slug>/', views.city_detail, name='city_detail'),
]