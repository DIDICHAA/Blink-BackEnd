from rest_framework import viewsets, status, mixins, generics
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.response import Response
from rest_framework.views import APIView

from django.shortcuts import render
from django.contrib.sites.shortcuts import get_current_site
from django.contrib.auth import authenticate, login
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.urls import reverse
from django.core.mail import EmailMessage
from django.core.exceptions import ObjectDoesNotExist
from dj_rest_auth.views import PasswordChangeView
from django.db import IntegrityError


from .serializers import UserLoginSerializer, UserRegisterSerializer, CustomPasswordChangeSerializer
from .models import User


class SignUpViewSet(mixins.CreateModelMixin, viewsets.GenericViewSet):
    queryset = User.objects.all()
    serializer_class = UserRegisterSerializer

    def create(self, request):
        password = request.data.get('password')

        user_data = {
            'email' : request.data['email'],
            'nickname' : request.data['nickname'],
        }

        try:
            user = User.objects.create(**user_data)
            user.set_password(password)
            user.save()

            refresh = RefreshToken.for_user(user)
            access_token = str(refresh.access_token)

            res = Response(
                {
                    "message": "회원가입 성공!",
                    "token": {
                        "access": access_token,
                        "refresh": str(refresh),
                    }
                },

                status=status.HTTP_201_CREATED,
            )
            return res
        except IntegrityError:
            return Response({'error': '이미 사용 중인 이메일입니다.'}, status=status.HTTP_400_BAD_REQUEST)

class LoginAPIView(APIView):
    queryset = User.objects.all()
    serializer_class = UserLoginSerializer

    def post(self, request, *args, **kwargs):
        email = request.data.get('email')
        password = request.data.get('password')

        try:
            user = User.objects.get(email=email)
        except ObjectDoesNotExist:
            return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)

        user = User.objects.get(email=email)
        user = authenticate(request, email=email,password=password)
        if user is not None:
            refresh = RefreshToken.for_user(user)
            access_token = str(refresh.access_token)
            # 로그인 성공 시, update_second_last_login 함수 호출
            user.update_second_last_login()
            login(request, user)
            res = Response(
                {
                    "user": {
                        'nickname': user.nickname,
                        'email': user.email,
                        'password' : user.password
                    },
                    "message": "로그인 성공!",
                    "token": {
                        "access": access_token,
                        "refresh": str(refresh),
                    },
                },
                status=status.HTTP_200_OK,
                )
            return res
        return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)
    
class CustomPasswordChangeView(PasswordChangeView):
    serializer_class = CustomPasswordChangeSerializer

