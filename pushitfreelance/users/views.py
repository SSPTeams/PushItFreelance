from django.contrib.auth.views import LoginView, LogoutView
from django.http import HttpResponse
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views import View
from django.views.decorators.csrf import csrf_exempt

from users.forms import UserForm
from users.models import User


class UserView(View):
    def get(self, request):
        users = User.objects.all()
        return render(request, "users/users_list.html", {"users": users})



class RegisterView(View):
    form_class = UserForm

    def get(self, request):
        form = self.form_class()
        return render(request, "users/register.html", {"form": form})

    @csrf_exempt
    def post(self, request):
        username = request.POST.get("username")
        email = request.POST.get("email")
        password = request.POST.get("password")
        user = User.objects.create_user(username=username, email=email, password=password)
        return HttpResponse(f"User {user.username} created successfully!")


class UserDetailView(View):
    def get(self, request, pk):
        user = User.objects.get(pk=pk)
        return render(request, "users/user_template.html", {"user": user})


class UserLoginView(LoginView):
    template_name = 'users/login.html'
    fields = '__all__'
    redirect_authenticated_user = True

    def get_success_url(self):
        return reverse_lazy('projects')

class UserLogoutView(LogoutView):
    next_page = 'login'