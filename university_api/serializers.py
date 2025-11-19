from rest_framework import serializers
from university.models import University, Employee


class EmployeeShortSerializer(serializers.ModelSerializer):
    class Meta:
        model = Employee
        fields = ["first_name", "last_name", "image"]

class UniversitySerializer(serializers.ModelSerializer):
    employee = EmployeeShortSerializer(many=True, read_only=True)
    class Meta:
        model = University
        fields = ["name", "postal_address", "region", "employee", "phone_number", "email", "website", "image"]


class UniversityListSerializer(serializers.ModelSerializer):
    class Meta:
        model = University
        fields = ["name", "region", "phone_number", "image"]