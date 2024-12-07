from django.http import JsonResponse
from rest_framework import filters
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.decorators import action

from .models import Project
from rest_framework import viewsets, views

from .serializers import ProjectSerializer
from rest_framework import permissions
from .filters import ProjectFilter




class ProjectViewSet(viewsets.ModelViewSet):
    serializer_class = ProjectSerializer
    queryset = Project.objects.all()
    permission_classes = [permissions.AllowAny]


    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    search_fields = ['description']
    filterset_class = ProjectFilter


