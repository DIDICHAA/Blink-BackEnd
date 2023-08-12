from rest_framework import serializers
from .models import *

# 다중 파일에 사용하는 serializer
class MainPostMediaSerializer(serializers.ModelSerializer):
    class Meta:
        model = MainPostMedia
        fields = ['media']

# /mainposts, 
# /mainposts/<int:mainpost_id> 
# (post create, delete, 특정 post의 comment list에 사용하는 serializer)
class MainPostSerializer(serializers.ModelSerializer):
    # detail 화면에서 comments 가져오기
    comments = serializers.SerializerMethodField()
    # replies = serializers.SerializerMethodField()
    medias = MainPostMediaSerializer(many=True, required=False)
    
    def get_comments(self, instance):
        serializers = MainCommentSerializer(instance.comments, many=True)
        return serializers.data
    
    def get_medias(self, instance):
        serializers = MainPostSerializer(instance.medias, many=True)
        return serializers.data
    
    def create(self, validated_data):
        medias_data = self.context['request'].FILES
        writer_id = self.context['request'].user.id  # 현재 로그인한 사용자의 ID를 가져옴
        mainpost = MainPost.objects.create(writer_id=writer_id, **validated_data)  # 작성자 ID를 포함하여 MainPost 생성
        for media_data in medias_data.getlist('media'):
            MainPostMedia.objects.create(mainpost=mainpost, media=media_data)
        return mainpost

    
    # def create(self, validated_data):
    #     medias_data = self.context['request'].FILES
    #     mainpost = MainPost.objects.create(**validated_data)
    #     for media_data in medias_data.getlist('media'):
    #         MainPostMedia.objects.create(mainpost=mainpost, media=media_data)
    #     return mainpost
    class Meta:
        model = MainPost
        # 직렬화에 포함되는 필드 목록 (all이어도 모두쓰기)
        fields = [
            'id',
            'created_at',
            'writer',
            'title',
            'content',
            'comments',
            'medias',
            # 'category',
            # location, category, filmed_at 차후 수정예정
        ]
        # 읽기전용 필드 목록
        read_only_fields = [
            'id',
            'created_at',
            'writer',
        ]

# /mainposts 
# (post list에 사용하는 serializer)
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
            # 'category',
            # 'like_cnt',
        ]

# /mainposts/<int:mainpost_id>/maincomments, 
# /maincomments, 
# /maincomments/<int:maincomment_id> 
# (comment list, delete,특정 comment의 reply create, list에 사용하는 serializer)
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
        read_only_fields = [
            'id',
            'created_at',
        ]

# /mainreplies, /mainreplies/<int:mainreply_id> (reply list, delete에 사용하는 serializer)
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
        read_only_fields = [
            'id',
            'created_at'
        ]


