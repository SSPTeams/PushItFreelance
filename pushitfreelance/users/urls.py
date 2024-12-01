from django.urls import path
from .views import *


urlpatterns = [
    path("", UserView.as_view(), name="users"),
    path("register/", RegisterView.as_view(), name="register"),
    path("<int:pk>/", UserDetailView.as_view(), name="user"),
    path("login/", UserLoginView.as_view(), name="login"),
    path("logout/", UserLogoutView.as_view(), name="logout"),
]
