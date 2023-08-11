from django.urls import path, include
from .views import *
from rest_framework import routers
from django.conf import settings
from django.conf.urls.static import static

app_name = "community"

default_router = routers.SimpleRouter()
default_router.register("composts", CommunityViewSet, basename="composts")

comment_router = routers.SimpleRouter()
comment_router.register("comcomments", CommentViewSet, basename="comcomments")

community_comment_router = routers.SimpleRouter()
community_comment_router.register("comcomments", CommunityCommentViewSet, basename="comcomments")

urlpatterns = [
    path("", include(default_router.urls)),
    path("", include(comment_router.urls)),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)