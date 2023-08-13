from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import MyPageViewSet, MyRequestViewSet, MyReportViewSet, MyComPostViewSet, MyComViewSet

router = DefaultRouter()

router.register(r'myrequests', MyRequestViewSet, basename='myrequest')
router.register(r'myreports', MyReportViewSet, basename='myreport')
router.register(r'mycomposts', MyComPostViewSet, basename='mycompost')
router.register(r'mycoms', MyComViewSet, basename='mycom')

urlpatterns = [
    path('mypage/', MyPageViewSet.as_view({'get': 'list'}), name='mypage'),
    path('mypage/', include(router.urls)),
]