from rest_framework import serializers
from university.models import University


class UniversitySerializer(serializers.ModelSerializer):
    class Meta:
        model = University
        fields = ["name", "postal_address", "region", "phone_number", "email", "website", "image"]



class UniversityListSerializer(serializers.ModelSerializer):
    class Meta:
        model = University
        fields = ["name", "region", "phone_number", "image"]
