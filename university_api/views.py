from django.views.generic import ListView
from rest_framework.generics import RetrieveAPIView

from university.models import University
from university_api.serializers import UniversitySerializer


class UniversityDetailView(RetrieveAPIView):
    queryset = University.objects.all()
    serializer_class = UniversitySerializer