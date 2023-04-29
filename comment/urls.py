from django.urls import path
from . import views

app_name = 'comment'

urlpatterns = [

    # 增加评论
    path('add_comment/<str:slug>/<int:id>/', views.add_comment, name='add_comment'),
    # 回复评论
    path('reply_comment/<str:slug>/<int:id>/<int:parent_comment_id>/', views.add_comment, name='reply_comment'),
   # 增加留言
    path('post-message/', views.message_form, name='post_message'),
]