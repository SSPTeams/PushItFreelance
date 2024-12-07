from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import UserViewSet, EmployeeProfileView, EmployerProfileView

router = DefaultRouter()
router.register(r'users', UserViewSet, basename='user')



urlpatterns = [
    path('', include(router.urls)),
    path('<int:user_id>/employee-profile/', EmployeeProfileView.as_view(), name='user-employee-profile'),
    path('<int:user_id>/employer-profile/', EmployerProfileView.as_view(), name='user-employer-profile'),
]
