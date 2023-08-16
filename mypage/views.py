from rest_framework import viewsets, mixins, status, generics
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action

from community.models import ComPost, ComComment, ComReply
from main.models import MainPost, MainComment, MainReply
from .serializers import *
from django.shortcuts import redirect, get_object_or_404
from .models import *

from rest_framework.views import APIView
from rest_framework.response import Response
from django.contrib.auth import update_session_auth_hash

from dj_rest_auth.views import UserDetailsView

from django.contrib.auth import update_session_auth_hash



class ProfileUpdateViewSet(viewsets.ViewSet):
    permission_classes = [IsAuthenticated]

    @action(detail=False, methods=['put'])
    def update_profile(self, request):
        user = request.user
        profile_serializer = ProfileUpdateSerializer(user, data=request.data, partial=True)

        if profile_serializer.is_valid():
            old_password = profile_serializer.validated_data.get('old_password')
            new_password = profile_serializer.validated_data.get('new_password')
            new_password_confirm = profile_serializer.validated_data.get('new_password_confirm')

            if not user.check_password(old_password):
                return Response({'error': '기존 비밀번호가 일치하지 않습니다.'}, status=status.HTTP_400_BAD_REQUEST)

            if new_password:
                if new_password != new_password_confirm:
                    return Response({'error': '새 비밀번호와 새 비밀번호 확인이 일치하지 않습니다.'}, status=status.HTTP_400_BAD_REQUEST)

                user.set_password(new_password)
                user.save()

                # 세션 인증 해시 업데이트
                update_session_auth_hash(request, user)

            profile_serializer.save()

            return Response({'message': '프로필 정보가 성공적으로 변경되었습니다.'}, status=status.HTTP_200_OK)

        return Response({'error': profile_serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

class CustomUserDetailsView(UserDetailsView):
    serializer_class = ProfileUpdateSerializer

# 나머지 내용은 그대로 유지하며, 필요에 따라 수정해주시면 됩니다.


#-----------------여기서부터 글/댓글 목록 불러오는 건데 걍 다 날려도 됨 미친것

class UserPostsAPI(generics.ListAPIView):

    def get_queryset(self):
        user = self.request.user

        jebo_true_posts = MainPost.objects.filter(writer=user, jebo_bool=1)
        jebo_false_posts = MainPost.objects.filter(writer=user, jebo_bool=0)
        community_posts = ComPost.objects.filter(writer=user)
        
        main_comments = list(MainComment.objects.filter(writer=user))
        main_replies = list(MainReply.objects.filter(writer=user))
        com_comments = list(ComComment.objects.filter(writer=user))
        com_replies = list(ComReply.objects.filter(writer=user))

        all_comments_and_replies = main_comments + main_replies + com_comments + com_replies

        return {
            "jebo_true_posts": jebo_true_posts,
            "jebo_false_posts": jebo_false_posts,
            "community_posts": community_posts,
            "all_comments_and_replies": all_comments_and_replies
        }


    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = CombinedSerializer(queryset, context={'request':'request'})
        return Response(serializer.data)

