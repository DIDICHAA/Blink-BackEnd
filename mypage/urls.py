from django.urls import path, include
from rest_framework import routers
from rest_framework.routers import DefaultRouter

from .views import ProfileUpdateViewSet, CustomUserDetailsView, ActivityViewSet, MyRequestViewSet, MyReportViewSet, MyComPostViewSet, MyComViewSet

app_name = "community"

default_router = routers.SimpleRouter(trailing_slash=False)
default_router.register("mypage", ProfileUpdateViewSet, basename="mypage")

#router.register(r'activity', ActivityViewSet, basename='activity')
#router.register(r'myrequests', MyRequestViewSet, basename='myrequest')
#router.register(r'myreports', MyReportViewSet, basename='myreport')
#router.register(r'mycomposts', MyComPostViewSet, basename='mycompost')
#router.register(r'mycoms', MyComViewSet, basename='mycom')

urlpatterns = [
    path("", include(default_router.urls)),
    path('user/details/', CustomUserDetailsView.as_view(), name='user-details'),
]
