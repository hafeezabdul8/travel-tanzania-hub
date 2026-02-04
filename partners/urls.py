from django.urls import path
from . import views

urlpatterns = [
    # Public routes
    path('register/', views.become_partner, name='become_partner'),
    
    # Partner dashboard routes (require partner login)
    path('dashboard/', views.partner_dashboard, name='partner_dashboard'),
    path('bookings/', views.partner_bookings, name='partner_bookings'),
    path('earnings/', views.partner_earnings, name='partner_earnings'),
    path('listings/', views.partner_listings, name='partner_listings'),
    path('settings/', views.partner_settings, name='partner_settings'),
    path('hotels/add/', views.add_hotel, name='add_hotel'),
    path('notifications/<int:notification_id>/read/', views.mark_notification_read, name='mark_notification_read'),
    
    # Admin routes
    path('admin/management/', views.admin_partner_management, name='admin_partner_management'),
]