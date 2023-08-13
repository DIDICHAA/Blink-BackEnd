from django.db import models
from accounts.models import User
from main.models import MainComment, MainReply, MainPost
from community.models import ComComment, ComReply, ComPost

class MyRequest(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='myrequests')
    mainposts = models.ManyToManyField(MainPost, related_name='myrequests', blank=True)

    def __str__(self):
        return f'My Request for {self.user} - {", ".join(mainpost.title for mainpost in self.mainposts.all())}'

class MyReport(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='myreports')
    mainposts = models.ManyToManyField(MainPost, related_name='myreports', blank=True)

    def __str__(self):
        return f'My Report for {self.user} - {", ".join(mainpost.title for mainpost in self.mainposts.all())}'

class MyComPost(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='mycomposts')
    composts = models.ManyToManyField(ComPost, related_name='mycomposts', blank=True)

    def __str__(self):
        return f'My Community Posts {self.user} - {", ".join(compost.title for compost in self.composts.all())}'

class MyCom(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='mycoms')
    maincomments = models.ManyToManyField(MainComment, related_name='mycoms', blank=True)
    mainreplies = models.ManyToManyField(MainReply, related_name='mycoms', blank=True)
    comcomments = models.ManyToManyField(ComComment, related_name='mycoms', blank=True)
    comreplies = models.ManyToManyField(ComReply, related_name='mycoms', blank=True)

    def __str__(self):
        return f'My Comments and Replies for {self.user}'
