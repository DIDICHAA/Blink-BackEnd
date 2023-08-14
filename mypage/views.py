from rest_framework import viewsets, mixins
from rest_framework.permissions import IsAuthenticated

from community.models import ComPost, ComComment, ComReply
from main.models import MainPost, MainComment, MainReply
from .serializers import *
from django.shortcuts import redirect, get_object_or_404
from .models import Activity

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import update_session_auth_hash

class ProfileUpdateView(APIView):
    permission_classes = [IsAuthenticated]
    allowed_methods = ['PUT', 'OPTIONS']

    def put(self, request):
        user = request.user
        profile_serializer = ProfileUpdateSerializer(user, data=request.data, partial=True)
        password_serializer = ProfilePasswordChangeSerializer(data=request.data)

        if profile_serializer.is_valid() and password_serializer.is_valid():
            profile_serializer.save()
            
            old_password = password_serializer.validated_data['old_password']
            new_password = password_serializer.validated_data['new_password']

            if not user.check_password(old_password):
                return Response({'error': '기존 비밀번호가 일치하지 않습니다.'}, status=status.HTTP_400_BAD_REQUEST)

            user.set_password(new_password)
            user.save()
            update_session_auth_hash(request, user)

            return Response({'message': '프로필과 비밀번호가 성공적으로 변경되었습니다.'}, status=status.HTTP_200_OK)
        
        return Response({'error': profile_serializer.errors, 'password_error': password_serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
#-----------------여기서부터 글/댓글 목록 불러오는 건데 걍 다 날려도 됨 미친것
def goto_activity(request, related_id):
    activity = get_object_or_404(Activity, id=related_id)
    # 해당 활동에 대한 URL 생성 또는 리다이렉트
    if activity.content_type.model == 'mainpost':
        return redirect('main:mainpost-detail', pk=activity.mainpost.id)
    elif activity.content_type.model == 'compost':
        return redirect('community:compost-detail', pk=activity.compost.id)
    elif activity.content_type.model == 'maincomment':
        return redirect('main:maincomment-detail', pk=activity.maincomment.id)
    elif activity.content_type.model == 'comcomment':
        return redirect('community:comcomment-detail', pk=activity.comcomment.id)
    elif activity.content_type.model == 'mainreply':
        return redirect('main:mainreply-detail', pk=activity.mainreply.id)
    elif activity.content_type.model == 'comreply':
        return redirect('community:comreply-detail', pk=activity.comreply.id)
    else:
        return redirect('mypage:activity-list')


class ActivityViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = ActivitySerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user

        user_composts = ComPost.objects.filter(writer=user)
        user_comcomments = ComComment.objects.filter(writer=user)
        user_comreplies = ComReply.objects.filter(writer=user)
        user_mainposts = MainPost.objects.filter(writer=user)
        user_maincomments = MainComment.objects.filter(writer=user)
        user_mainreplies = MainReply.objects.filter(writer=user)

    # 개별 모델의 쿼리셋을 리스트로 합침
        queryset = list(user_composts) + list(user_comcomments) + list(user_comreplies) + \
        list(user_mainposts) + list(user_maincomments) + list(user_mainreplies)
    
    # 글 쓴 날짜를 기준으로 정렬
        queryset = sorted(queryset, key=lambda x: x.created_at, reverse=True)

    # 새로운 list로 변환하지 않고 그대로 반환
        return queryset


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
        mainposts = MainPost.objects.filter(jebo_bool=self.mainpost_jebo_bool)
        queryset.update(mainposts=mainposts)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

        

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.mainpost_jebo_bool = 1  # 또는 0, 필요한 값으로 초기화

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
        mainposts = MainPost.objects.filter(jebo_bool=self.mainpost_jebo_bool)
        queryset.update(mainposts=mainposts)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)


    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.mainpost_jebo_bool = 0

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

        # MyComPost에 연결된 ComPost들 가져오기
        composts = ComPost.objects.filter(mycompost__user=request.user)
        queryset.update(composts=composts)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)


