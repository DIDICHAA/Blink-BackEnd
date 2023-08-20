from django.db import models
from accounts.models import User

# Create your models here.
class MainPost(models.Model):
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=50)
    writer = models.ForeignKey(User, on_delete=models.CASCADE, blank=False, null=False)
    content = models.CharField(max_length=1000)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    category_choices = [
        ('교통사고', '교통사고'), 
        ('도난,절도', '도난,절도'), 
        ('실종신고', '실종신고'), 
        ('기타', '기타')
    ]
    category = models.CharField(default='', max_length = 10, choices=category_choices, blank=False, null=False)
    jebo_bool = models.BooleanField(default=False)
    lat = models.FloatField(blank=True, null=True)
    lng = models.FloatField(blank=True, null=True)
    location = models.CharField(max_length=300, blank=True, null=True)
    filmed_at = models.IntegerField(blank=True, null=True)
    media = models.CharField(max_length=5000, blank=True, null=True) #, blank=True, null=True 필요하면 집어넣기

class MainComment(models.Model):
    id = models.AutoField(primary_key=True)
    writer = models.ForeignKey(User, on_delete=models.CASCADE, blank=False, null=False)
    content = models.TextField(max_length=200)
    created_at = models.DateTimeField(auto_now_add=True)
    mainpost = models.ForeignKey(MainPost, blank=False, null=False, on_delete=models.CASCADE, related_name='comments')
    media = models.CharField(max_length=5000, blank=True, null=True) #, blank=True, null=True 필요하면 집어넣기

class MainReply(models.Model):
    id = models.AutoField(primary_key=True)
    writer = models.ForeignKey(User, on_delete=models.CASCADE, blank=False, null=False)
    content = models.TextField(max_length=200)
    created_at = models.DateTimeField(auto_now_add=True)
    maincomment = models.ForeignKey(MainComment, blank=False, null=False, on_delete=models.CASCADE, related_name='replies')
