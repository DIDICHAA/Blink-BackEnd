from django.shortcuts import render, get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from django.db.models import Count, Q

from rest_framework import viewsets, mixins
from rest_framework.response import Response
from rest_framework.decorators import api_view, action
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from rest_framework.pagination import PageNumberPagination
from rest_framework import status


from .models import *
from .serializers import *
from .permissions import IsOwnerOrReadOnly
from .paginations import ComPostPagination


class ComPostViewSet(viewsets.ModelViewSet):
    queryset = ComPost.objects.annotate(
        like_cnt=Count(
            "reactions", filter=Q(reactions__reaction="like"),distinct=True
        ),

    )
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ["title", "content"]
    search_fields = ["title", "content"]
    #ordering_fields = ["title", "created_at"]
    pagination_class = ComPostPagination
    

    def get_permissions(self):
        if self.action in ["update", "destroy", "partial_update"]:
            return [IsAdminUser()]
        elif self.action in ["likes"]:
            return [IsAuthenticated()]
        return []
    
    def get_serializer_class(self):
        if self.action == "list":
            return ComPostListSerializer
        return ComPostSerializer

    def create(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)

        return Response(serializer.data)

    def perform_update(self, serializer):
        compost = serializer.save()

    @action(methods=["POST"], detail=True, permission_classes=[IsAuthenticated])
    def like(self, request, pk=None):
        compost = self.get_object()
        user = request.user

        try:
            existing_reaction = CommunityReaction.objects.get(compost=compost, user=user, reaction="like")
            existing_reaction.delete()
            return Response({"detail": "Like removed."}, status=status.HTTP_200_OK)
        except CommunityReaction.DoesNotExist:
            CommunityReaction.objects.create(compost=compost, user=user, reaction="like")
            return Response({"detail": "Like added."}, status=status.HTTP_201_CREATED)

#게시글 댓글 많은 순
    @action(detail=False, methods=["GET"])
    def cmt(self, request):
        composts = self.queryset.order_by("-comments_cnt")
        serializer = self.get_serializer(composts, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

#게시글 좋아요 많은 순
    @action(detail=False, methods=["GET"])
    def popular(self, request):
        composts = self.queryset.order_by("-like_cnt")
        serializer = self.get_serializer(composts, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

#게시글 최근 순
    @action(detail=False, methods=["GET"])
    def recent(self, request):
        composts = self.queryset.order_by("-created_at")
        serializer = self.get_serializer(composts, many=True)
        return Response(serializer.data)

#게시글 오래된 순
    @action(detail=False, methods=["GET"])
    def oldest(self, request):
        composts = self.queryset.order_by("created_at")
        serializer = self.get_serializer(composts, many=True)
        return Response(serializer.data)

#댓글 detail 뷰셋
class ComCommentViewSet(
    viewsets.GenericViewSet, 
    mixins.RetrieveModelMixin, 
    mixins.DestroyModelMixin,
    ):
    queryset = ComComment.objects.all()
    serializer_class = ComCommentSerializer

    def get_permissions(self):
        if self.action in ["update", "destroy"]:
            return [IsOwnerOrReadOnly()]
        return []

    def get_objects(self):
        obj = super().get_object()
        return obj

#댓글 작성 뷰셋 
class CommunityComCommentViewSet(
    viewsets.GenericViewSet, 
    mixins.ListModelMixin,
    mixins.CreateModelMixin,
    ):
    serializer_class = ComCommentSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        compost = self.kwargs.get("compost_id")
        queryset = ComComment.objects.filter(compost_id=compost)
        return queryset

    def create(self, request, compost_id=None):
        compost = get_object_or_404(ComPost, id=compost_id)
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(compost=compost)
        return Response(serializer.data)

#대댓글 작성 관련 뷰셋
class CommunityComReplyViewSet(
    viewsets.GenericViewSet, 
    mixins.CreateModelMixin,
    mixins.ListModelMixin,
    ):
    # queryset = MainComment.objects.all()
    serializer_class = ComReplySerializer

    # url 에서 maincomment_id 를 가져옴
    def get_queryset(self):
        comcomment = self.kwargs.get("comcomment_id")
        queryset = ComReply.objects.filter(comcomment_id=comcomment)
        return queryset
    
    def get_permissions(self):
        if self.action in ['create', 'destroy']:
            return [IsAuthenticated()]
        return []
    
    def create(self, request, comcomment_id=None):
        comcomment = get_object_or_404(ComComment, id=comcomment_id)
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(comcomment=comcomment)
        return Response(serializer.data)

#comment 대댓글 detail 관련 뷰셋
class ComReplyViewSet(
    viewsets.GenericViewSet, 
    mixins.DestroyModelMixin, 
    mixins.ListModelMixin, 
    mixins.RetrieveModelMixin
    ):
    queryset = ComReply.objects.all()
    serializer_class = ComReplySerializer

    # 읽기만 가능
    def get_permissions(self):
        if self.action in ['create', 'destroy']:
            return [IsAuthenticated()]
        return []