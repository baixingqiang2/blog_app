from django.contrib import admin
from .models import Notice,Banner,Link


admin.site.site_header = '川塔-管理后台'  # 设置header
admin.site.site_title = '川塔-管理后台'  # 设置title
admin.site.index_title = '川塔-管理后台'

@admin.register(Notice)
class NoticeAdmin(admin.ModelAdmin):
    list_display = ('id', 'notice_name', 'notice_url', 'is_notice','notice_color')
@admin.register(Banner)
class BannerAdmin(admin.ModelAdmin):
    list_display = ('id', 'text_info', 'img', 'link_url', 'is_active')
@admin.register(Link)
class LinkAdmin(admin.ModelAdmin):
    list_display = ('id', 'name','linkurl')