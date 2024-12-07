from rest_framework import serializers
from rest_framework.authtoken.models import Token

from users.models import EmployeeProfile, EmployerProfile, User


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True, min_length=8)

    class Meta:
        model = User
        fields = ['username', 'password', 'email']

    def create(self, validated_data):
        # Создаем пользователя
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password']
        )
        # Генерируем токен
        Token.objects.create(user=user)
        return user


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'telegram_id', 'password']
        extra_kwargs = {
            'password': {'write_only': True},  # Скрываем пароль в ответе
        }

    def create(self, validated_data):
        # Создаем пользователя с хэшированием пароля
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data.get('email', ''),
            password=validated_data['password'],
            telegram_id=validated_data.get('telegram_id', None)
        )
        return user

    def update(self, instance, validated_data):
        # Обновляем пользователя, поддерживаем смену пароля
        password = validated_data.pop('password', None)
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        if password:
            instance.set_password(password)
        instance.save()
        return instance

class EmployeeProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = EmployeeProfile
        fields = ['id', 'description']

class EmployerProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = EmployerProfile
        fields = ['id']

