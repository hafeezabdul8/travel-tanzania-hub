from django.urls import path
from . import views

urlpatterns = [
    path('', views.admin_dashboard, name='admin_dashboard'),
    path('reports/', views.financial_reports, name='financial_reports'),
    path('partners/', views.partner_management, name='partner_management'),
    path('bookings/', views.booking_management, name='booking_management'),
]