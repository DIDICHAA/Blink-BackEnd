from django.shortcuts import render
from rest_framework import viewsets, mixins
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from django.db.models import Count, Q


from .models import MainPost
from .serializers import MainPostSerializer, MainPostListSerializer

# Create your views here.

#mainpostviewset은 POST기능만 있음.
class MainPostViewSet(viewsets.GenericViewSet, mixins.ListModelMixin, mixins.DestroyModelMixin):

    queryset = MainPost.objects.annotate(
        comments_cnt = Count("comments"),
        # like_cnt 해야해요
        )
    
    def get_serializer_class(self):
        if self.action == "list":
            return MainPostListSerializer
        return MainPostSerializer
    
    # def get_permission

    # create(self, request):

    # aciton(최신순)

    # action(오래된 순)

# class MainCommentViewSet()

# class MainReplyViewSet()
