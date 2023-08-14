from django.urls import path, include
from .views import *
from rest_framework import routers
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.views import TokenRefreshView

default_router = routers.SimpleRouter(trailing_slash=False)
default_router.register("signup", SignUpViewSet, basename="signup")

urlpatterns = [
    path('auth/token', TokenObtainPairView.as_view(), name='token_obtain_pair'), # refresh token, access token 확인
    path('auth/token/refresh', TokenRefreshView.as_view(), name='token_refresh'), # refresh token 입력 시 새로운 access token
    path('auth/', include(default_router.urls)),
    path('auth/login', LoginAPIView.as_view(), name='login'),
    path('auth/password/change', CustomPasswordChangeView.as_view(), name='rest_password_change'),
    path('dj-rest-auth/', include('dj_rest_auth.urls')),
]