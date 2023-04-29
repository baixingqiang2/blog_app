
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User
from .models import Profile, EmailVerifyRecord

@admin.register(EmailVerifyRecord)
class EmailAdmin(admin.ModelAdmin):
    list_display = ['code', 'email', 'send_type', 'send_time']
    search_fields = ['code', 'email', 'send_type']
    list_filter = ['code', 'email', 'send_type', 'send_time']
    list_display_links = ('send_time',)


class ProfileAdmin(admin.ModelAdmin) :
    list_display = ('id','username','another','email','phone','signs','is_superuser')


admin.site.register(Profile, ProfileAdmin)