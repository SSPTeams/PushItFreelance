from rest_framework import serializers
from users.models import User, EmployeeProfile, EmployerProfile


class UserSerializer(serializers.Serializer):
    class Meta:
        model = User
        fields = '__all__'


class UserThumbnailSerializer(serializers.Serializer):
    class Meta:
        model = User
        fields = ['id', 'username']



class EmployeeProfileSerializer(serializers.Serializer):
    user = UserThumbnailSerializer()

    class Meta:
        model = EmployeeProfile
        fields = '__all__'

class EmployerProfileSerializer(serializers.Serializer):
    user = UserThumbnailSerializer()

    class Meta:
        model = EmployerProfile
        fields = '__all__'

