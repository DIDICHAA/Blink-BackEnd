from rest_framework import serializers
from .models import MyReport, MyRequest, MyComPost, MyCom, User
from main.models import MainComment, MainReply, MainPost
from community.models import ComComment, ComReply, ComPost
from main.serializers import MainCommentSerializer, MainReplySerializer, MainPostSerializer
from community.serializers import ComCommentSerializer, ComReplySerializer, ComPostSerializer
from accounts.models import User
from dj_rest_auth.serializers import UserDetailsSerializer

class ProfileUpdateSerializer(UserDetailsSerializer):
    class Meta:
        model = User
        fields = ['profile_image', 'nickname']

class ProfilePasswordChangeSerializer(serializers.Serializer):
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)


#---------여기부터 활동관리-------------------
#-----------------------------------------
class ActivitySerializer(serializers.Serializer):
    user = serializers.StringRelatedField(source='writer')
    activity_type = serializers.SerializerMethodField()
    activity_data = serializers.SerializerMethodField()

    def get_activity_type(self, instance):
        if isinstance(instance, MyRequest):
            return 'my_request'
        elif isinstance(instance, MyReport):
            return 'my_report'
        elif isinstance(instance, MyComPost):
            return 'my_compost'
        elif isinstance(instance, MyCom):
            return 'my_comment_reply'
        else:
            return 'unknown'

    def get_activity_data(self, instance):
        if isinstance(instance, MyRequest) or isinstance(instance, MyReport):
            return None
        elif isinstance(instance, MyComPost):
            serializer = ComPostSerializer(instance.composts.all(), many=True)
        elif isinstance(instance, MyCom):
            comcomments = instance.comcomments.all()
            comreplies = instance.comreplies.all()
            maincomments = instance.maincomments.all()
            mainreplies = instance.mainreplies.all()
            comcomments_serializer = ComCommentSerializer(comcomments, many=True)
            comreplies_serializer = ComReplySerializer(comreplies, many=True)
            maincomments_serializer = MainCommentSerializer(maincomments, many=True)
            mainreplies_serializer = MainReplySerializer(mainreplies, many=True)
            serializer = {
                'comcomments': comcomments_serializer.data,
                'comreplies': comreplies_serializer.data,
                'maincomments': maincomments_serializer.data,
                'mainreplies': mainreplies_serializer.data
            }
        return serializer.data

    def get_related_id(self, instance):
        if instance.content_type.model == 'mainpost':
            return instance.mainpost.id
        elif instance.content_type.model == 'compost':
            return instance.compost.id
        elif instance.content_type.model == 'maincomment':
            return instance.maincomment.id
        elif instance.content_type.model == 'comcomment':
            return instance.comcomment.id
        elif instance.content_type.model == 'mainreply':
            return instance.mainreply.id
        elif instance.content_type.model == 'comreply':
            return instance.comreply.id
        else:
            return None


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


