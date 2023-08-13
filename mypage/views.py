from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import MyMainPost, MyComPost, MyCom
from .serializers import MyMainPostSerializer, MyComPostSerializer, MyComSerializer

class MyMainPostViewSet(viewsets.ModelViewSet):
    queryset = MyMainPost.objects.all()
    serializer_class = MyMainPostSerializer

class MyComPostViewSet(viewsets.ModelViewSet):
    queryset = MyComPost.objects.all()
    serializer_class = MyComPostSerializer

class MyComViewSet(viewsets.ModelViewSet):
    queryset = MyCom.objects.all()
    serializer_class = MyComSerializer
