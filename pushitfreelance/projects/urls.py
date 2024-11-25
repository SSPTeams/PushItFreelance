from django.urls import path
from .views import *


urlpatterns = [
    path("", get_projects, name="projects"),
    path("<int:pk>/", get_project, name="project")
]
