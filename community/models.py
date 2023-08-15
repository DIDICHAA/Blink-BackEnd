from django.db import models
from django.conf import settings
from accounts.models import User

def image_upload_path(instance, filename):
    return f'{instance.pk}/{filename}'

class ComPost(models.Model):
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=30, blank=False)
    content = models.TextField(max_length=3000, blank=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    media = models.FileField(upload_to='compost_media/', blank=True, null=True)
    writer = models.ForeignKey(User, on_delete=models.CASCADE, blank=False, null=True)
    comcomments_cnt = models.PositiveIntegerField(default=0)

class ComComment(models.Model):
    id = models.AutoField(primary_key=True)
    compost= models.ForeignKey(ComPost, blank=True, null=True, on_delete=models.CASCADE, related_name='comcomments')
    # writer = models.ForeignKey(User, on_delete=models.CASCADE, )
    content = models.TextField(max_length=500, blank=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    like = models.PositiveIntegerField(default=0)
    writer = models.ForeignKey(User, on_delete=models.CASCADE, blank=False, null=True)

    def save(self, *args, **kwargs):
        # 댓글이 생성되거나 삭제될 때 'comcomments_cnt' 필드 갱신
        self.compost.comcomments_cnt = self.compost.comcomments.count()
        self.compost.save()
        super(ComComment, self).save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        # 댓글이 삭제될 때 'comcomments_cnt' 필드 갱신
        self.compost.comcomments_cnt = self.compost.comcomments.count()
        self.compost.save()
        super(ComComment, self).delete(*args, **kwargs)

class CommunityReaction(models.Model):
    REACTION_CHOICES = (("like", "Like"), ("heart", "Heart"))
    reaction = models.CharField(choices=REACTION_CHOICES, max_length=10)
    compost = models.ForeignKey(ComPost, on_delete=models.CASCADE, related_name="reactions")
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

class ComReply(models.Model):
    id = models.AutoField(primary_key=True)
    writer = models.ForeignKey(User, on_delete=models.CASCADE, blank=False, null=True)
    content = models.TextField(max_length=200)
    created_at = models.DateTimeField(auto_now_add=True)
    comcomment = models.ForeignKey(ComComment, blank=False, null=False, on_delete=models.CASCADE, related_name='replies')

class ComPostMedia(models.Model):
    compost = models.ForeignKey(ComPost, on_delete=models.CASCADE, related_name='medias')
    media = models.FileField(upload_to='compost_media/', blank=True, null=True)

class ComCommentMedia(models.Model):
    ComComment = models.ForeignKey(ComComment, on_delete=models.CASCADE, related_name = 'medias')
    media = models.FileField(upload_to='comcomment_media/', blank=True, null=True) #, blank=True, null=True 필요하면 집어넣기
