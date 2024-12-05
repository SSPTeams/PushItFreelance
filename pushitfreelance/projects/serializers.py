from rest_framework import serializers

from users.serializers import UserSerializer, EmployerProfileSerializer
from .models import Project


class ProjectSerializer(serializers.ModelSerializer):
    employer = EmployerProfileSerializer()

    class Meta:
        model = Project
        fields = '__all__'