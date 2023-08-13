from django.db import models
from accounts.models import User
from main.models import MainPost, MainComment, MainReply
from community.models import ComPost, ComComment, ComReply

class MyMainPost(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='mymainposts')
    mainpost = models.ForeignKey(MainPost, on_delete=models.CASCADE)

    def __str__(self):
        return self.mainpost.title

class MyComPost(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='mycomposts')
    compost = models.ForeignKey(ComPost, on_delete=models.CASCADE)

    def __str__(self):
        return self.compost.title

class MyCom(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='mycommentsreplies')
    maincomments = models.ManyToManyField(MainComment, related_name='mycoms', blank=True)
    mainreplies = models.ManyToManyField(MainReply, related_name='mycoms', blank=True)
    comcomments = models.ManyToManyField(ComComment, related_name='my_oms', blank=True)
    comreplies = models.ManyToManyField(ComReply, related_name='mycoms', blank=True)

    def __str__(self):
        return f'My Comments and Replies for {self.user}'
