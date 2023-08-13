from rest_framework import serializers
from .models import MyMainPost, MyComPost, MyCom

class MyMainPostSerializer(serializers.ModelSerializer):
    class Meta:
        model = MyMainPost
        fields = '__all__'

class MyComPostSerializer(serializers.ModelSerializer):
    class Meta:
        model = MyComPost
        fields = '__all__'

class MyComSerializer(serializers.ModelSerializer):
    maincomments = MainCommentSerializer(many=True, read_only=True)
    mainreplies = MainReplySerializer(many=True, read_only=True)
    comcomments = ComCommentSerializer(many=True, read_only=True)
    comreplies = ComReplySerializer(many=True, read_only=True)

    class Meta:
        model = MyCom
        fields = '__all__'
