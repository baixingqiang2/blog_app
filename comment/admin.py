from django.contrib import admin
from mptt.admin import MPTTModelAdmin

from .models import Message,Comment


# admin.site.register(Comment, MPTTModelAdmin)

# @admin.register(Comment)
# class CommentAdmin(MPTTModelAdmin):
#     list_display = ('id', 'author', 'article','parent','reply_to','content', 'pub_date')
admin.site.register(Comment)
@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ('name', 'email','phone', 'message','suggest')