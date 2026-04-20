from django.urls import path
from . import views

urlpatterns = [
    path('', views.admin_dashboard, name='admin_dashboard'),
    path('reports/', views.financial_reports, name='financial_reports'),
    path('partners/', views.partner_management, name='partner_management'),
    path('bookings/', views.booking_management, name='booking_management'),
    
    path('add-training/', views.add_training_example, name='add_training_example'),
    path('training-stats/', views.training_stats_view, name='training_stats'),
    path('bulk-import/', views.bulk_import_training, name='bulk_import_training'),
    path('export-training/', views.export_training_data, name='export_training_data'),
]