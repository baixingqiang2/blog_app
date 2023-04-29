"""
导航栏主要url配置
"""

from django.urls import re_path
from . import views
from article import views as lss


app_name = 'common'

urlpatterns = [
    re_path(r'home/', views.index_views, name='home'),  # 主页
    re_path(r'resource/', views.resource_views, name='resource'),  # 资源分享
    re_path(r'timeline/', views.timeline_views, name='timeline'),  # 时光树
    re_path(r'about/', views.about_views, name='about'),  # 关于我们
    re_path(r'picurewall', views.picturewall, name='picturewall'),  # 照片墙
    re_path(r'musicland', views.musicland, name='musicland'),  # 音乐天地
]

