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

    path('mainpost/<int:pk>/', MainPostDetailView.as_view(), name='mainpost-detail'),
    path('compost/<int:pk>/', ComPostDetailView.as_view(), name='compost-detail'),

    # 댓글과 대댓글의 디테일을 가져오는 엔드포인트 근데 이걸 이렇게 하나하나 연결하는 게 맞나? 순회하면서 타입으로 분류하고 연결한다고 하네염
    path('maincomment/<int:pk>/', MainCommentDetailView.as_view(), name='maincomment-detail'),
    path('mainreply/<int:pk>/', MainReplyDetailView.as_view(), name='mainreply-detail'),
    path('comcomment/<int:pk>/', ComCommentDetailView.as_view(), name='comcomment-detail'),
    path('comreply/<int:pk>/', ComReplyDetailView.as_view(), name='comreply-detail'),
]

