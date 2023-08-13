from rest_framework import viewsets, mixins
from rest_framework.response import Response
from rest_framework.decorators import action
from .models import MyAct
from .serializers import MyActSerializer, CombinedActSerializer

class MyActViewSet(
    viewsets.GenericViewSet, 
    mixins.ListModelMixin, 
    mixins.RetrieveModelMixin
    ):
    queryset = MyAct.objects.all()
    serializer_class = MyActSerializer

    @action(methods=['GET'], detail=True, url_path='combined-acts')
    def combined_acts(self, request, pk=None):
        my_act = self.get_object()
        serializer = CombinedActSerializer(my_act)
        return Response(serializer.data)
