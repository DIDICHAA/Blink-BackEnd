from django.shortcuts import render
from django.utils import timezone
from django.shortcuts import get_object_or_404
from django.db.models import Count, Q

from rest_framework import viewsets, mixins
from rest_framework.response import Response
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from rest_framework.decorators import action
from rest_framework import status
from django_filters import rest_framework as filters
from django_filters.rest_framework import DjangoFilterBackend

from .models import *
from .serializers import *

class MainPostFilter(filters.FilterSet):
    category = filters.ChoiceFilter(choices=MainPost.category_choices)
    title_contains = filters.CharFilter(field_name='title', lookup_expr='icontains')
    location_contains = filters.CharFilter(field_name='location', lookup_expr='icontains')
    
    class Meta:
        model = MainPost
        fields = ['category', 'title_contains', 'location_contains']

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
    # Define the filter backend class and the filter class
    filter_backends = [DjangoFilterBackend]
    filterset_class = MainPostFilter

    def get_queryset(self):
        queryset = MainPost.objects.annotate(
            comments_cnt=Count("comments"),
        )
        return queryset
    
    def get_serializer_class(self):
        if self.action == "list":
            return MainPostListSerializer
        return MainPostSerializer
    
    def get_permissions(self):
        if self.action in ['create', 'destroy', 'update', 'partial_update', 'notification']:
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

    @action(methods=['GET'], detail=False)
    def notification(self, request):
        user = request.user

        if user.is_anonymous:
            return Response({"message": "You must be logged in to access this feature."}, status=status.HTTP_401_UNAUTHORIZED)

        last_second_login = user.last_second_login
        
        # 로그인한 사용자가 작성한 MainPost 중 updated_at이 last_second_login보다 늦은 게시물들을 가져옴
        queryset = self.get_queryset().filter(writer=user, updated_at__gt=last_second_login, comments_cnt__gt=0).order_by('updated_at')
        
        serializer = MainPostNotificationSerializer(queryset, many=True)
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

        # 업데이트된 updated_at 필드 처리
        mainpost.updated_at = timezone.now()
        mainpost.save()
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
    mixins.CreateModelMixin,
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