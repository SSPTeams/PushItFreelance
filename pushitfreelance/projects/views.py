from django.shortcuts import render
from .models import Project


# Create your views here.

def get_projects(request):
    projects = Project.objects.all()
    return render(request, "projects/projects_list.html", {"projects": projects})


def get_project(request, pk):
    project = Project.objects.get(pk=pk)
    return render(request, "projects/project_template.html", {"project": project})