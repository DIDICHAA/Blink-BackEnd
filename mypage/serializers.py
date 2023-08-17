from rest_framework import serializers
from main.models import MainComment, MainReply, MainPost
from community.models import ComComment, ComReply, ComPost
from main.serializers import MainCommentSerializer, MainReplySerializer, MainPostSerializer
from community.serializers import ComCommentSerializer, ComReplySerializer, ComPostSerializer
from accounts.models import User
from dj_rest_auth.serializers import UserDetailsSerializer


class ProfileUpdateSerializer(UserDetailsSerializer):
    old_password = serializers.CharField(write_only=True, required=True)
    new_password = serializers.CharField(write_only=True, required=False)
    new_password_confirm = serializers.CharField(write_only=True, required=False)

    class Meta:
        model = User
        fields = ['profile_image', 'nickname', 'old_password', 'new_password', 'new_password_confirm']

    def validate(self, data):
        new_password = data.get('new_password')
        new_password_confirm = data.get('new_password_confirm')

        if new_password or new_password_confirm:
            if new_password != new_password_confirm:
                raise serializers.ValidationError("새 비밀번호와 새 비밀번호 확인이 일치하지 않습니다.")
            
            # 기존 비밀번호 확인 로직 추가
            old_password = data.get('old_password') 
            if not self.instance.check_password(old_password):
                raise serializers.ValidationError("기존 비밀번호가 일치하지 않습니다.")
            
            # 새 비밀번호 저장 로직 추가
            self.instance.set_password(new_password)
            self.instance.save()

        return data

#---------여기부터 활동관리-------------------
#-----------------------------------------

class CommentContentSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ('content', 'created_at', 'id')

class MainCommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = MainComment
        fields = ('content', 'created_at', 'id')

class MainReplySerializer(serializers.ModelSerializer):
    class Meta:
        model = MainReply
        fields = ('content', 'created_at', 'id')

class ComCommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = ComComment
        fields = ('content', 'created_at', 'id')

class ComReplySerializer(serializers.ModelSerializer):
    class Meta:
        model = ComReply
        fields = ('content', 'created_at', 'id')

class MainPostSerializer(serializers.ModelSerializer):
    class Meta:
        model = MainPost
        fields = ('title', 'updated_at', 'id')

class ComPostSerializer(serializers.ModelSerializer):
    class Meta:
        model = ComPost
        fields = ('title', 'updated_at', 'id')

class CombinedSerializer(serializers.Serializer):
    jebo_true_posts = MainPostSerializer(many=True)
    jebo_false_posts = MainPostSerializer(many=True)
    community_posts = ComPostSerializer(many=True)
    all_comments_and_replies = serializers.SerializerMethodField()

    def get_all_comments_and_replies(self, obj):
        combined = obj['all_comments_and_replies']
        
        serialized_data = []

        for item in combined:
            if isinstance(item, MainComment):
                serialized_data.append(MainCommentSerializer(item).data)
            elif isinstance(item, MainReply):
                serialized_data.append(MainReplySerializer(item).data)
            elif isinstance(item, ComComment):
                serialized_data.append(ComCommentSerializer(item).data)
            elif isinstance(item, ComReply):
                serialized_data.append(ComReplySerializer(item).data)

        return serialized_data

class MainPostDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = MainPost
        fields = '__all__'

class ComPostDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = ComPost
        fields = '__all__'

class MainCommentDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = MainComment
        fields = '__all__'

class MainReplyDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = MainReply
        fields = '__all__'

class ComCommentDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = ComComment
        fields = '__all__'

class ComReplyDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = ComReply
        fields = '__all__'

