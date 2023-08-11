from rest_framework import serializers
from .models import *

class CommunitySerializer(serializers.ModelSerializer):
    comments = serializers.SerializerMethodField()
    image = serializers.ImageField(use_url=True, required=False)
    like_cnt = serializers.SerializerMethodField()  

    def get_like_cnt(self, instance):
        return instance.reactions.filter(reaction='like').count()

    def get_comments(self, instance):
        serializer = CommentSerializer(instance.comments, many=True)
        return serializer.data

    class Meta:
        model = Community
        fields = "__all__"
        read_only_fields = ['id', 'created_at', 'updated_at', 'like_cnt', 'comments_cnt']

class CommunityListSerializer(serializers.ModelSerializer):
    comments_cnt = serializers.SerializerMethodField()
    like_cnt = serializers.SerializerMethodField() 

    def get_like_cnt(self, instance):
        return instance.reactions.filter(reaction='like').count()

    def get_comments_cnt(self, instance):
        return instance.comments.count()
        
    class Meta:
        model = Community
        fields = [
            'id',
            'title',
            'content',
            'created_at',
            'updated_at',
            'comments_cnt',
            'like_cnt',
        ]
        read_only_fields = ['id','created_at', 'updated_at', 'comments_cnt', 'like_cnt']

class CommentSerializer(serializers.ModelSerializer):

    community = serializers.SerializerMethodField()

    def get_community(self, instance):
        return instance.community.title

    class Meta:
        model = Comment
        fields = '__all__'
        read_only_fields = ['community', 'id']
