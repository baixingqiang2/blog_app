from django.urls import path,re_path
from . import views

app_name = 'article'

urlpatterns = [
    path('', views.article_list, name='article_list'),
    path(r'<str:slug>/<int:id>/', views.article_detail, name='article_detail'),
    path(r'create/', views.article_create, name='article_create'),
    path(r'delete/<str:slug>/<int:id>/', views.article_safe_delete, name='article_safe_delete'),
    path(r'update/<str:slug>/<int:id>/', views.article_update, name='article_update'),
    path(r'article-admin/', views.article_admin, name='article_admin'),
    path(r'like-article/', views.article_like, name='article_like'),
    path(r'update-status/<str:slug>/<int:id>/', views.update_status, name='update_status'),

]