from django.urls import path
from .views import ProjectViewSet
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'projects', ProjectViewSet)

urlpatterns = [
]

urlpatterns += router.urls
