from django.urls import path
from . import views

urlpatterns = [
    path('', views.tourism_view, name='tourism'),
    path('attraction/<int:attraction_id>/', views.attraction_detail, name='attraction_detail'),
    path('packages/', views.tour_packages_view, name='tour_packages'),
    path('package/book/<int:package_id>/', views.book_tour_package, name='book_tour_package'),
    path('booking/confirmation/<int:booking_id>/', views.tour_booking_confirmation, name='tour_booking_confirmation'),
    path('my-bookings/', views.my_tour_bookings, name='my_tour_bookings'),
    path('booking/cancel/<int:booking_id>/', views.cancel_tour_booking, name='cancel_tour_booking'),
    path('api/package/<int:package_id>/quick-view/', views.package_quick_view, name='package_quick_view'),
    path('attraction/<int:attraction_id>/review/', views.add_review, name='add_review'),
]