from django.urls import path, include
from rest_framework.routers import DefaultRouter
#from . import views
from .views import ProfileUpdateView

app_name = 'mypage'



urlpatterns = [
    path('mypage/', ProfileUpdateView.as_view(), name='profile_update'),
]



#router = DefaultRouter()
#router.register(r'activities', views.ActivityViewSet, basename='activity')


#urlpatterns = [
    #path('', include(router.urls)),
    #path('activities/<int:related_id>/', views.goto_activity, name='goto-activity'),
#]
