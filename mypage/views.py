from rest_framework import viewsets, mixins, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import MyRequest, MyReport, MyComPost, MyCom
from .serializers import (
    MyRequestSerializer,
    MyReportSerializer,
    MyComPostSerializer,
    MyComSerializer,
    MainCommentSerializer, 
    MainReplySerializer,  
    ComCommentSerializer,   
    ComReplySerializer,    
)

class MyPageViewSet(viewsets.GenericViewSet):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = None  # 사용할 시리얼라이저가 없습니다.
    
    def list(self, request, *args, **kwargs):
        user = self.request.user
        
        myrequests = MyRequest.objects.filter(user=user)
        myreports = MyReport.objects.filter(user=user)
        mycomposts = MyComPost.objects.filter(user=user)
        mycoms = MyCom.objects.filter(user=user)
        
        myrequests_serializer = MyRequestSerializer(myrequests, many=True)
        myreports_serializer = MyReportSerializer(myreports, many=True)
        mycomposts_serializer = MyComPostSerializer(mycomposts, many=True)
        mycoms_serializer = MyComSerializer(mycoms, many=True)
        
        response_data = {
            'myrequests': myrequests_serializer.data,
            'myreports': myreports_serializer.data,
            'mycomposts': mycomposts_serializer.data,
            'mycoms': mycoms_serializer.data,
        }
        
        return Response(response_data)

class MyRequestViewSet(
    viewsets.GenericViewSet,
    mixins.ListModelMixin
):
    serializer_class = MyRequestSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        return MyRequest.objects.filter(user=user)

    # list 메서드 수정
    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()

        # jebo_bool 값이 1인 MainPost들 가져오기
        mainposts = MainPost.objects.filter(jebo_bool=1)
        queryset.update(mainposts=mainposts)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

class MyReportViewSet(
    viewsets.GenericViewSet,
    mixins.ListModelMixin
):
    serializer_class = MyReportSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        return MyReport.objects.filter(user=user)

    # list 메서드 수정
    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()

        # jebo_bool 값이 0인 MainPost들 가져오기
        mainposts = MainPost.objects.filter(jebo_bool=0)
        queryset.update(mainposts=mainposts)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

class MyComPostViewSet(
    viewsets.GenericViewSet,
    mixins.ListModelMixin
):
    serializer_class = MyComPostSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        return MyComPost.objects.filter(user=user)

    # list 메서드 수정
    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()

        # MyComPost에 연결된 ComPost들 가져오기
        composts = ComPost.objects.filter(mycompost__user=request.user)
        queryset.update(composts=composts)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

class MyComViewSet(viewsets.ModelViewSet):
    queryset = MyCom.objects.all()
    serializer_class = MyComSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        return MyCom.objects.filter(user=user)

    # list 메서드 수정
    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()

        # MyCom에 연결된 댓글들과 답글들 가져오기
        maincomments = MainComment.objects.filter(mycom__user=request.user)
        mainreplies = MainReply.objects.filter(mycom__user=request.user)
        comcomments = ComComment.objects.filter(mycom__user=request.user)
        comreplies = ComReply.objects.filter(mycom__user=request.user)

        queryset.update(
            maincomments=maincomments,
            mainreplies=mainreplies,
            comcomments=comcomments,
            comreplies=comreplies,
        )

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)