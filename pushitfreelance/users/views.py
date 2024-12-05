from django.contrib.auth.views import LoginView, LogoutView
from django.http import HttpResponse
from django.shortcuts import render, redirect
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
        return render(request, "auth/register.html", {"form": form})

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
    template_name = 'auth/login.html'
    fields = '__all__'
    redirect_authenticated_user = True

    def get_success_url(self):
        return reverse_lazy('projects')

class UserLogoutView(LogoutView):
    next_page = 'login'


from django.views import View
from django.http import JsonResponse
from django.contrib.auth import login
from django.conf import settings
import hashlib
import hmac
import time
import json

class TelegramAuthView(View):
    def post(self, request):
        # Получаем данные из тела запроса
        try:
            data = json.loads(request.body)
        except json.JSONDecodeError:
            return JsonResponse({'success': False, 'error': 'Некорректный формат JSON'}, status=400)

        # Извлекаем hash из данных
        hash_ = data.pop('hash', None)
        if not hash_:
            return JsonResponse({'success': False, 'error': 'Отсутствует hash'}, status=400)

        auth_date = data.get('auth_date')
        if not auth_date:
            return JsonResponse({'success': False, 'error': 'Отсутствует auth_date'}, status=400)

        # Проверяем подлинность данных от Telegram
        if not self.verify_telegram_auth(data, hash_):
            return JsonResponse({'success': False, 'error': 'Неверные данные авторизации'}, status=400)

        # Проверяем срок действия auth_date (опционально)
        if time.time() - int(auth_date) > 86400:
            return JsonResponse({'success': False, 'error': 'Срок действия авторизации истек'}, status=400)

        # Получаем данные пользователя
        telegram_id = data.get('id')
        if not telegram_id:
            return JsonResponse({'success': False, 'error': 'Отсутствует telegram_id'}, status=400)

        username = data.get('username', f"tg_user_{telegram_id}")
        first_name = data.get('first_name', '')
        last_name = data.get('last_name', '')

        # Получаем или создаем пользователя
        user, created = User.objects.get_or_create(
            telegram_id=telegram_id,
            defaults={
                'username': username,
                'first_name': first_name,
                'last_name': last_name            }
        )

        # Обновляем информацию о пользователе (если необходимо)
        if not created:
            user.username = username
            user.first_name = first_name
            user.last_name = last_name
            user.save()

        # Аутентифицируем пользователя
        login(request, user)

        # Возвращаем успешный ответ
        return redirect('/projects')

    def verify_telegram_auth(self, data, hash_):
        # Сортируем данные и формируем строку
        data_check_arr = [f"{k}={v}" for k, v in data.items()]
        data_check_arr.sort()
        data_check_string = '\n'.join(data_check_arr)

        # Вычисляем секретный ключ
        secret_key = hashlib.sha256(settings.TELEGRAM_BOT_TOKEN.encode()).digest()

        # Вычисляем хэш
        hmac_hash = hmac.new(secret_key, msg=data_check_string.encode(), digestmod=hashlib.sha256).hexdigest()

        # Сравниваем хэши
        return hmac.compare_digest(hmac_hash, hash_)

