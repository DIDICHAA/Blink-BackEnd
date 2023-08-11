from django.shortcuts import render, get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from django.db.models import Count, Q

from rest_framework import viewsets, mixins
from rest_framework.response import Response
from rest_framework.decorators import api_view, action
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from rest_framework.pagination import PageNumberPagination

from .models import Community, Comment
from .serializers import *
from .permissions import IsOwnerOrReadOnly
from .paginations import CommunityPagination


class CommunityViewSet(viewsets.ModelViewSet):
    queryset = Community.objects.annotate(
        like_cnt=Count(
            "reactions", filter=Q(reactions__reaction="like"),distinct=True
        ),

    )
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ["title", "content"]
    search_fields = ["title", "content"]
    #ordering_fields = ["title", "created_at"]
    pagination_class = CommunityPagination
    

    def get_permissions(self):
        if self.action in ["update", "destroy", "partial_update"]:
            return [IsAdminUser()]
        elif self.action in ["likes"]:
            return [IsAuthenticated()]
        return []
    
    def get_serializer_class(self):
        if self.action == "list":
            return CommunityListSerializer
        return CommunitySerializer

    def create(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)

        return Response(serializer.data)

    def perform_update(self, serializer):
        community = serializer.save()

    @action(methods=["POST"], detail=True, permission_classes=[IsAuthenticated])
    def like(self, request, pk=None):
        community = self.get_object()
        user = request.user

        try:
            existing_reaction = CommunityReaction.objects.get(post=post, user=user, reaction="like")
            existing_reaction.delete()
            return Response({"detail": "Like removed."}, status=status.HTTP_200_OK)
        except PostReaction.DoesNotExist:
            CommunityReaction.objects.create(community=community, user=user, reaction="like")
            return Response({"detail": "Like added."}, status=status.HTTP_201_CREATED)

    @action(detail=False, methods=["GET"])
    def cmt(self, request):
        communities = self.queryset.order_by("-comments_cnt")
        serializer = self.get_serializer(communities, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(detail=False, methods=["GET"])
    def popular(self, request):
        communities = self.queryset.order_by("-like_cnt")
        serializer = self.get_serializer(communities, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(detail=False, methods=["GET"])
    def recent(self, request):
        communities = self.queryset.order_by("-created_at")
        serializer = self.get_serializer(communities, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=["GET"])
    def oldest(self, request):
        communities = self.queryset.order_by("created_at")
        serializer = self.get_serializer(communities, many=True)
        return Response(serializer.data)

class CommentViewSet(
    viewsets.GenericViewSet, 
    mixins.RetrieveModelMixin, 
    mixins.DestroyModelMixin,
    ):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer

    def get_permissions(self):
        if self.action in ["update", "destroy"]:
            return [IsOwnerOrReadOnly()]
        return []

    def get_objects(self):
        obj = super().get_object()
        return obj

class CommunityCommentViewSet(
    viewsets.GenericViewSet, 
    mixins.ListModelMixin, 
    mixins.CreateModelMixin,
    ):
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        community = self.kwargs.get("community_id")
        queryset = Comment.objects.filter(community_id=community)
        return queryset

    def create(self, request, community_id=None):
        community = get_object_or_404(Community, id=community_id)
        serializer = self.get_serializer(data=request.data)
        self.is_valid(raise_exception=True)
        serializer.save(community=community)
        return Response(serializer.data)
