from rest_framework import serializers
from .models import *
from rest_framework.serializers import ListField

class ComPostMediaSerializer(serializers.ModelSerializer):
    class Meta:
        model = ComPostMedia
        fields = ['media']

class ComPostSerializer(serializers.ModelSerializer):
    writer = serializers.CharField(source='writer.nickname', read_only=True)
    comcomments = serializers.SerializerMethodField()
    medias = ComPostMediaSerializer(many=True, required=False)
    like_cnt = serializers.SerializerMethodField()  

    def get_like_cnt(self, instance):
        return instance.reactions.filter(reaction='like').count()

    def get_comcomments(self, instance):
        serializer = ComCommentSerializer(instance.comcomments, many=True)
        return serializer.data

    def create(self, validated_data):
        medias_data = self.context['request'].FILES
        writer_id = self.context['request'].user.id  # 현재 로그인한 사용자의 ID를 가져옴
        compost = ComPost.objects.create(writer_id=writer_id, **validated_data)  # 작성자 ID를 포함하여 MainPost 생성
        for media_data in medias_data.getlist('media'):
            ComPostMedia.objects.create(compost=compost, media=media_data)
        return compost

    class Meta:
        model = ComPost
        fields = [
            'id',
            'title',
            'writer',
            'content',
            'created_at',
            'updated_at',
            'comcomments',
            'comcomments_cnt',
            'medias',
            'like_cnt'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at', 'like_cnt', 'writer', 'comcomments_cnt', 'comcomments']

class ComPostListSerializer(serializers.ModelSerializer):
    writer = serializers.CharField(source='writer.nickname', read_only=True)
    comcomments_cnt = serializers.SerializerMethodField()
    like_cnt = serializers.SerializerMethodField()
    medias = serializers.FileField(use_url=True, required=False)

    def get_like_cnt(self, instance):
        return instance.reactions.filter(reaction='like').count()

    def get_comcomments_cnt(self, instance):
        return instance.comcomments.count()
        
    class Meta:
        model = ComPost
        fields = [
            'id',
            'title',
            'content',
            'created_at',
            'updated_at',
            'comcomments_cnt',
            'like_cnt',
            'medias',
            'writer',
        ]
        read_only_fields = ['id', 'writer', 'created_at', 'updated_at', 'comcomments_cnt', 'like_cnt']

class ComCommentSerializer(serializers.ModelSerializer):
    writer = serializers.CharField(source='writer.nickname', read_only=True)
    compost = serializers.SerializerMethodField()
    medias = serializers.FileField(use_url=True, required=False)
    replies = serializers.SerializerMethodField()

    def get_compost(self, instance):
        return instance.compost.title
    
    def get_replies(self, instance):
        serializers = ComReplySerializer(instance.replies, many=True)
        return serializers.data

    class Meta:
        model = ComComment
        fields = '__all__'
        read_only_fields = ['compost', 'id']

class ComReplySerializer(serializers.ModelSerializer):
    writer = serializers.CharField(source='writer.nickname', read_only=True)
    class Meta:
        model = ComReply
        # 직렬화에 포함되는 필드 목록 (all이어도 모두쓰기)
        fields = [
            'id',
            'writer',
            'content',
            'created_at',
            'comcomment',
        ]
        read_only_fields = [
            'comcomment',
        ]
