from django.contrib import admin
from .models import File,PictureWall
# Register your models here.

@admin.register(File)
class FileAdmin(admin.ModelAdmin):
    list_display = ('id','name', 'file', 'category', 'slug', 'excerpt')
@admin.register(PictureWall)
class PicturAdmin(admin.ModelAdmin):
    list_display = ('id','name', 'picture_url')

# admin.site.register(File)