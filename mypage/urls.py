from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import MyActViewSet

router = DefaultRouter()
router.register(r'myacts', MyActViewSet)

urlpatterns = [
    path('', include(router.urls)),
]