from rest_framework import serializers
from .models import MyReport, MyRequest, MyComPost, MyCom
from main.models import MainComment, MainReply, MainPost
from community.models import ComComment, ComReply, ComPost
from main.serializers import MainCommentSerializer, MainReplySerializer
from community.serializers import ComCommentSerializer, ComReplySerializer

class MyRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = MyRequest
        fields = '__all__'

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['mainposts'] = [str(mainpost) for mainpost in instance.mainposts.all()]
        return representation

class MyReportSerializer(serializers.ModelSerializer):
    class Meta:
        model = MyReport
        fields = '__all__'

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['mainposts'] = [str(mainpost) for mainpost in instance.mainposts.all()]
        return representation

class MyComPostSerializer(serializers.ModelSerializer):
    class Meta:
        model = MyComPost
        fields = '__all__'

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['composts'] = [str(compost) for compost in instance.composts.all()]
        return representation

class MyComSerializer(serializers.ModelSerializer):
    maincomments = MainCommentSerializer(source='maincomments.all', many=True, read_only=True)
    mainreplies = MainReplySerializer(source='mainreplies.all', many=True, read_only=True)
    comcomments = ComCommentSerializer(source='comcomments.all', many=True, read_only=True)
    comreplies = ComReplySerializer(source='comreplies.all', many=True, read_only=True)

    class Meta:
        model = MyCom
        fields = '__all__'

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['maincomments'] = [str(maincomment) for maincomment in instance.maincomments.all()]
        representation['mainreplies'] = [str(mainreply) for mainreply in instance.mainreplies.all()]
        representation['comcomments'] = [str(comcomment) for comcomment in instance.comcomments.all()]
        representation['comreplies'] = [str(comreply) for comreply in instance.comreplies.all()]
        return representation

class MyPageSerializer(serializers.Serializer):
    myrequests = MyRequestSerializer(many=True, read_only=True)
    myreports = MyReportSerializer(many=True, read_only=True)
    mycomposts = MyComPostSerializer(many=True, read_only=True)
    mycoms = MyComSerializer(many=True, read_only=True)
