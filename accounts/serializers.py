from .models import User
from rest_framework import serializers
from dj_rest_auth.serializers import PasswordChangeSerializer

class UserRegisterSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ['nickname', 'email', 'password']
        extra_kwargs = {'password': {'write_only': True}}

class UserLoginSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ['email', 'password']
        extra_kwargs = {
            'password': {'write_only': True}
        }

class CustomPasswordChangeSerializer(PasswordChangeSerializer):
    origin_password = serializers.CharField(required=True)