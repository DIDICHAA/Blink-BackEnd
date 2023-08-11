from django.urls import path, include
from rest_framework import routers
from .views import *

app_name = "main"
default_router = routers.SimpleRouter(trailing_slash=False)
default_router.register("mainposts", MainPostViewSet, basename="mainposts")

maincomment_router = routers.SimpleRouter(trailing_slash=False)
maincomment_router.register("maincomments", MainCommentViewSet, basename="maincomments")

mainreply_router = routers.SimpleRouter(trailing_slash=False)
mainreply_router.register("mainreplies", MainReplyViewSet, basename="mainreplies")

mainpost_comment_router = routers.SimpleRouter(trailing_slash=False)
mainpost_comment_router.register("maincomments", MainPostCommentViewSet, basename="maincomments")

maincomment_reply_router = routers.SimpleRouter(trailing_slash=False)
maincomment_reply_router.register("mainreplies", MainCommentReplyViewSet, basename="mainreplies")

urlpatterns = [
    path("", include(default_router.urls)),
    path("", include(maincomment_router.urls)),
    path("", include(mainreply_router.urls)),
    path("mainposts/<int:mainpost_id>/", include(mainpost_comment_router.urls)),
    path("maincomments/<int:maincomment_id>/", include(maincomment_reply_router.urls)),
]