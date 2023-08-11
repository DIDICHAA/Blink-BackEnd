from rest_framework import serializers
from .models import *
from rest_framework.serializers import ListField

class ComPostSerializer(serializers.ModelSerializer):
    comcomments = serializers.SerializerMethodField()
    media = serializers.FileField(use_url=True, required=False)
    like_cnt = serializers.SerializerMethodField()  

    def get_like_cnt(self, instance):
        return instance.reactions.filter(reaction='like').count()

    def get_comcomments(self, instance):
        serializer = ComCommentSerializer(instance.comcomments, many=True)
        return serializer.data

    class Meta:
        model = ComPost
        fields = "__all__"
        read_only_fields = ['id', 'created_at', 'updated_at', 'like_cnt']

class ComPostListSerializer(serializers.ModelSerializer):
    comcomments_cnt = serializers.SerializerMethodField()
    like_cnt = serializers.SerializerMethodField()
    media = serializers.FileField(use_url=True, required=False)

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
            'media'
        ]
        read_only_fields = ['id','created_at', 'updated_at', 'comcomments_cnt', 'like_cnt', 'media']

class ComCommentSerializer(serializers.ModelSerializer):

    compost = serializers.SerializerMethodField()

    def get_compost(self, instance):
        return instance.compost.title

    class Meta:
        model = ComComment
        fields = '__all__'
        read_only_fields = ['compost', 'id']

class ComReplySerializer(serializers.ModelSerializer):
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
