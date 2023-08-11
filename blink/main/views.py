from django.shortcuts import render
from rest_framework import viewsets, mixins
from rest_framework.response import Response
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from rest_framework.decorators import action


from django.shortcuts import get_object_or_404
from django.db.models import Count, Q


from .models import *
from .serializers import *

# Create your views here.
#======================================================================================
# mainpost create 관련 뷰셋 (mainposts)
class MainPostViewSet(
    viewsets.GenericViewSet,
    mixins.CreateModelMixin,
    mixins.ListModelMixin,
    mixins.DestroyModelMixin,
    mixins.RetrieveModelMixin
    ):

    queryset = MainPost.objects.annotate(
        comments_cnt = Count("comments"),
        # like_cnt 해야해요
        )
    
    def get_serializer_class(self):
        if self.action == "list":
            return MainPostListSerializer
        return MainPostSerializer
    
    def get_permission(self):
        if self.action in ['create', 'destroy']:
            return [IsAuthenticated()]
        return []
    
    @action(methods=['GET'], detail=False)
    def recent(self, request):
        queryset = self.get_queryset().order_by("-created_at")
        serializer = MainPostListSerializer(queryset, many=True)
        return Response(serializer.data)
    
    @action(methods=['GET'], detail=False)
    def oldest(self, request):
        queryset = self.get_queryset().order_by("created_at")
        serializer = MainPostListSerializer(queryset, many=True)
        return Response(serializer.data)

#======================================================================================
# comments detail 관련 뷰셋 (maincomments/<int:maincomment_id>)
class MainCommentViewSet(
    viewsets.GenericViewSet, 
    mixins.CreateModelMixin,
    mixins.DestroyModelMixin,
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin
    ):
    queryset = MainComment.objects.all()
    serializer_class = MainCommentSerializer

    # 읽기만 가능
    def get_permissions(self):
        if self.action in ['create', 'destroy']:
            return [IsAuthenticated()]
        return []

#======================================================================================
# comments create 관련 뷰셋 (mainposts/<int:mainpost_id>/comments)
class MainPostCommentViewSet(
    viewsets.GenericViewSet,
    mixins.ListModelMixin,
    mixins.CreateModelMixin,
    ):
    serializer_class = MainCommentSerializer

    # url 에서 mainpost_id 를 가져옴
    def get_queryset(self):
        mainpost = self.kwargs.get("mainpost_id")
        queryset = MainComment.objects.filter(mainpost_id=mainpost)
        return queryset

    def get_permissions(self):
        if self.action in ['create', 'destroy']:
            return [IsAuthenticated()]
        return []
    
    def create(self, request, mainpost_id=None):
        mainpost = get_object_or_404(MainPost, id=mainpost_id)
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(mainpost=mainpost)
        return Response(serializer.data)
    
#======================================================================================
# replies create 관련 뷰셋 (maincomments/<int:maincomment_id>/replies)
class MainCommentReplyViewSet(
    viewsets.GenericViewSet, 
    mixins.CreateModelMixin,
    mixins.ListModelMixin,
    ):
    # queryset = MainComment.objects.all()
    serializer_class = MainReplySerializer

    # url 에서 maincomment_id 를 가져옴
    def get_queryset(self):
        maincomment = self.kwargs.get("maincomment_id")
        queryset = MainReply.objects.filter(maincomment_id=maincomment)
        return queryset
    
    def get_permissions(self):
        if self.action in ['create', 'destroy']:
            return [IsAuthenticated()]
        return []
    
    def create(self, request, maincomment_id=None):
        maincomment = get_object_or_404(MainComment, id=maincomment_id)
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(maincomment=maincomment)
        return Response(serializer.data)
    
#======================================================================================
# replies detail 관련 뷰셋
class MainReplyViewSet(
    viewsets.GenericViewSet, 
    mixins.DestroyModelMixin,
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin
    ):
    queryset = MainReply.objects.all()
    serializer_class = MainReplySerializer

    # 읽기만 가능
    def get_permissions(self):
        if self.action in ['create', 'destroy']:
            return [IsAuthenticated()]
        return []
    
#======================================================================================