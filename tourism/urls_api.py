from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views_api import TouristAttractionViewSet, TourPackageViewSet

router = DefaultRouter()
router.register(r'attractions', TouristAttractionViewSet)
router.register(r'packages', TourPackageViewSet)

urlpatterns = [
    path('', include(router.urls)),
]