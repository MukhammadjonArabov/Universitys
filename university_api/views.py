from rest_framework.generics import RetrieveAPIView, ListAPIView
from university.models import University
from university_api.serializers import UniversitySerializer, UniversityListSerializer


class UniversityDetailView(RetrieveAPIView):
    queryset = University.objects.all()
    serializer_class = UniversitySerializer

class UniversityListView(ListAPIView):
    queryset = University.objects.all()
    serializer_class = UniversityListSerializer