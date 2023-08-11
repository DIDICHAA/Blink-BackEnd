from rest_framework import serializers
from .models import *

# Mainposts/<int:mainpost_id> (delete랑 comment보기, 달기)
class MainPostSerializer(serializers.ModelSerializer):
    # detail 화면에서 comments 가져오기
    comments = serializers.SerializerMethodField()
    # replies = serializers.SerializerMethodField()
    
    def get_comments(self, instance):
        serializers = MainCommentSerializer(instance.comments, many=True)
        return serializers.data
    
    class Meta:
        model = MainPost
        # 직렬화에 포함되는 필드 목록 (all이어도 모두쓰기)
        fields = [
            'id',
            'title',
            'writer',
            'content',
            'created_at',
            'comments',
            # location, category, filmed_at, media 차후 수정예정
        ]
        # 읽기전용 필드 목록
        read_only_field = [
            'id',
            'created_at',
        ]

class MainPostListSerializer(serializers.ModelSerializer):
    comments_cnt = serializers.IntegerField()
    # like_cnt = serializers.IntegerField()

    class Meta:
        model = MainPost
        # 직렬화에 포함되는 필드 목록 (all이어도 모두쓰기)
        fields = [
            'id',
            'title',
            'writer',
            'content',
            'created_at',
            'comments_cnt',
            # 'like_cnt',
        ]
        # 읽기전용 필드 목록
        # read_only_field = [
        #     'id', 
        #     'writer',
        #     'created_at',
        #     'commtents_cnt',
        #     'like_cnt',
        # ]
    
class MainCommentSerializer(serializers.ModelSerializer):
    content = serializers.CharField()
    replies = serializers.SerializerMethodField()
    
    def get_replies(self, instance):
        serializers = MainReplySerializer(instance.replies, many=True)
        return serializers.data
    
    class Meta:
        model = MainComment
        # 직렬화에 포함되는 필드 목록 (all이어도 모두쓰기)
        fields = [
            'id',
            'writer',
            'content',
            'created_at',
            'mainpost',
            'replies',
        ]
        read_only_field = [
            'mainpost',
        ]

class MainReplySerializer(serializers.ModelSerializer):
    class Meta:
        model = MainReply
        # 직렬화에 포함되는 필드 목록 (all이어도 모두쓰기)
        fields = [
            'id',
            'writer',
            'content',
            'created_at',
            'maincomment',
        ]
        read_olny_field = [
            'maincomment',
        ]



