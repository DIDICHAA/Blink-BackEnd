from rest_framework import serializers
from .models import MyAct, MainComment, MainReply, ComComment, ComReply

class MyActSerializer(serializers.ModelSerializer):
    class Meta:
        model = MyAct
        fields = '__all__'

class CombinedActSerializer(serializers.Serializer):
    act = serializers.SerializerMethodField()

    def get_act(self, obj):
        combined_acts = []

        combined_acts.extend(obj.maincomments.all())
        combined_acts.extend(obj.mainreplies.all())
        combined_acts.extend(obj.comcomments.all())
        combined_acts.extend(obj.comreplies.all())

        combined_acts.sort(key=lambda x: x.created_at, reverse=True)
        
        return combined_acts
