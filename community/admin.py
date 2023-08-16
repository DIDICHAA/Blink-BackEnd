from django.contrib import admin
from .models import *
# Register your models here.
admin.site.register(ComPost)
admin.site.register(ComComment)
admin.site.register(CommunityReaction)
admin.site.register(ComReply)
admin.site.register(ComPostMedia)
admin.site.register(ComCommentMedia)
