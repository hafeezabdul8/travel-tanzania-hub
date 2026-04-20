from django.urls import path
from . import views

app_name = 'partners'

urlpatterns = [
    # Public routes
    path('register/', views.become_partner, name='become_partner'),
    
    path('', views.partner_list, name='partner_list'),  
    path('<int:partner_id>/', views.partner_detail, name='partner_detail'),  
    path('category/<str:category>/', views.partner_by_category, name='partner_by_category'),  
    path('city/<str:city>/', views.partner_by_city, name='partner_by_city'),  
    path('search/', views.partner_search, name='partner_search'),  
    
    
    # Partner dashboard routes (require partner login)
    path('dashboard/', views.partner_dashboard, name='partner_dashboard'),
    path('bookings/', views.partner_bookings, name='partner_bookings'),
    path('earnings/', views.partner_earnings, name='partner_earnings'),
    path('listings/', views.partner_listings, name='partner_listings'),
    path('settings/', views.partner_settings, name='partner_settings'),
    path('hotels/add/', views.add_hotel, name='add_hotel'),
    path('notifications/<int:notification_id>/read/', views.mark_notification_read, name='mark_notification_read'),
    
    path('<int:partner_id>/book/', views.book_partner_service, name='book_partner_service'),
    path('my-bookings/', views.my_partner_bookings, name='my_partner_bookings'),
    path('booking/<int:booking_id>/cancel/', views.cancel_partner_booking, name='cancel_partner_booking'),
    
    path('images/', views.partner_images, name='partner_images'),
    path('images/add/', views.add_partner_image, name='add_partner_image'),
    path('images/delete/<int:image_id>/', views.delete_partner_image, name='delete_partner_image'),
    path('images/set-primary/<int:image_id>/', views.set_primary_image, name='set_primary_image'),
    path('images/reorder/', views.reorder_images, name='reorder_images'),
        
    # Admin routes
    path('admin/management/', views.admin_partner_management, name='admin_partner_management'),
]