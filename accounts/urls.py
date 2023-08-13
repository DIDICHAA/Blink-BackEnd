from django.urls import path
from accounts import views
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.views import TokenRefreshView
urlpatterns = [
    path('google/login', views.google_login, name='google_login'),
    path('google/callback/', views.google_callback, name='google_callback'),  
    path('google/login/finish/', views.GoogleLogin.as_view(), name='google_login_todjango'),
    path('kakao/login/', views.kakao_login, name='kakao_login'),
    path('kakao/callback/', views.kakao_callback, name='kakao_callback'),
    path('kakao/login/finish/', views.KakaoLogin.as_view(), name='kakao_login_todjango'),
    path('rest-auth/naver/', views.NaverLogin.as_view(), name='naver'),
    path('auth/token', TokenObtainPairView.as_view(), name='token_obtain_pair'), # refresh token, access token 확인
    path('auth/token/refresh', TokenRefreshView.as_view(), name='token_refresh'), # refresh token 입력 시 새로운 access token
]