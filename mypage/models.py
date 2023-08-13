from django.db import models
from accounts.models import User
from main.models import MainPost, MainComment, MainReply
from community.models import ComPost, ComComment, ComReply

class MyAct(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='acts')
    mainposts = models.ManyToManyField(MainPost, related_name='myacts', blank=True)
    maincomments = models.ManyToManyField(MainComment, related_name='myacts', blank=True)
    mainreplies = models.ManyToManyField(MainReply, related_name='myacts', blank=True)
    comcomments = models.ManyToManyField(ComComment, related_name='myacts', blank=True)
    comreplies = models.ManyToManyField(ComReply, related_name='myacts', blank=True)
    
    class Meta:
        ordering = ['-id']
