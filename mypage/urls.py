from django.urls import path, include
from rest_framework import routers
from rest_framework.routers import DefaultRouter
from .views import *

app_name = "mypage"

default_router = routers.SimpleRouter(trailing_slash=False)
default_router.register("mypage", ProfileUpdateViewSet, basename="mypage")

urlpatterns = [
    path("", include(default_router.urls)),
    path('mypage/profile', CustomUserDetailsView.as_view(), name='profile'),
    path('mypage/activities', UserPostsAPI.as_view(), name='activities'), 
]

