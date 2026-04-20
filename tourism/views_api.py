from rest_framework import viewsets, permissions, filters
from django_filters.rest_framework import DjangoFilterBackend
from .models import TouristAttraction, TourPackage, UserReview
from .serializers import TouristAttractionSerializer, TourPackageSerializer

class TouristAttractionViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = TouristAttraction.objects.all()
    serializer_class = TouristAttractionSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['city', 'category']
    search_fields = ['name', 'description', 'location']

class TourPackageViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = TourPackage.objects.filter(is_featured=True) | TourPackage.objects.all()
    serializer_class = TourPackageSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['attraction__city']