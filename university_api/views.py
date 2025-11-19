from university.models import University
from university_api.serializers import UniversitySerializer, UniversityListSerializer
from rest_framework import filters, generics
from django_filters.rest_framework import DjangoFilterBackend


class UniversityDetailView(generics.RetrieveAPIView):
    queryset = University.objects.all()
    serializer_class = UniversitySerializer

class UniversityListView(generics.ListAPIView):
    queryset = University.objects.all()
    serializer_class = UniversityListSerializer

    filter_backends = (DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter)
    filterset_fields = ('region',)
    search_fields = ('name', 'website',)