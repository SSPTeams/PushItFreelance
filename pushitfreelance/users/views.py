from django.shortcuts import render, redirect
from django.views import View
from django.http import JsonResponse
from django.contrib.auth import login
from django.conf import settings
import hashlib
import hmac
import time
import json
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.decorators import action
from rest_framework.authtoken.models import Token
from rest_framework.views import APIView

from .models import User, EmployeeProfile, EmployerProfile
from .serializers import UserSerializer, EmployeeProfileSerializer, EmployerProfileSerializer


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def get_permissions(self):
        # Регистрация доступна всем, а остальные действия — только аутентифицированным пользователям
        if self.action in ['create']:
            return [AllowAny()]
        return [IsAuthenticated()]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            token, created = Token.objects.get_or_create(user=user)
            return Response({
                "message": "User registered successfully",
                "token": token.key,
                "user": {
                    "id": user.id,
                    "username": user.username,
                    "email": user.email,
                    "telegram_id": user.telegram_id,
                }
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['get'], permission_classes=[IsAuthenticated])
    def me(self, request):
        # Возвращаем данные текущего пользователя
        serializer = self.get_serializer(request.user)
        return Response(serializer.data)

    @action(detail=False, methods=['post'], permission_classes=[IsAuthenticated])
    def change_password(self, request):
        # Позволяет сменить пароль
        user = request.user
        password = request.data.get('password')
        if not password:
            return Response({"error": "Password is required"}, status=status.HTTP_400_BAD_REQUEST)
        user.set_password(password)
        user.save()
        return Response({"message": "Password updated successfully"})


class EmployeeProfileView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, user_id):
        profile = EmployeeProfile.objects.filter(user_id=user_id).first()
        if not profile:
            return Response({"detail": "Not found"}, status=404)
        serializer = EmployeeProfileSerializer(profile)
        return Response(serializer.data)

    def post(self, request, user_id):
        # Создание или обновление единственного профиля для user_id
        profile, created = EmployeeProfile.objects.get_or_create(user_id=user_id)
        serializer = EmployeeProfileSerializer(profile, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201 if created else 200)
        return Response(serializer.errors, status=400)

    def patch(self, request, user_id):
        profile = EmployeeProfile.objects.filter(user_id=user_id).first()
        if not profile:
            return Response({"detail": "Not found"}, status=404)
        serializer = EmployeeProfileSerializer(profile, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=400)


class EmployerProfileView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, user_id):
        profile = EmployerProfile.objects.filter(user_id=user_id).first()
        if not profile:
            return Response({"detail": "Not found"}, status=404)
        serializer = EmployerProfileSerializer(profile)
        return Response(serializer.data)

    def post(self, request, user_id):
        # Создание или обновление единственного профиля для user_id
        profile, created = EmployerProfile.objects.get_or_create(user_id=user_id)
        serializer = EmployerProfileSerializer(profile, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201 if created else 200)
        return Response(serializer.errors, status=400)




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

