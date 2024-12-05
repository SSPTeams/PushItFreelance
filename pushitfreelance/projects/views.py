from django.http import JsonResponse
from rest_framework import filters
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.decorators import action

from .models import Project
from rest_framework import viewsets, views

from .serializers import ProjectSerializer
from rest_framework import permissions
from .filters import ProjectFilter



'''
class ProjectView(views.APIView):
    def get(self):
        projects = Project.objects.all()
        return projects
'''




class ProjectViewSet(viewsets.ModelViewSet):
    serializer_class = ProjectSerializer
    queryset = Project.objects.all()
    permission_classes = [permissions.AllowAny]


    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    search_fields = ['description']  # Поле для поиска по описанию
    filterset_class = ProjectFilter


    @action(detail=True, methods=['post'])
    def confirm(self, request, pk=None):
        project = self.get_object()
        project.is_confirmed = True
        project.save()

        # notify employer
        # notify freelancers


        return JsonResponse({'status': 'ok'})



class Meta:
        model = Project
        fields = '__all__'