from django.urls import path,re_path
from . import views

app_name = 'resource'

urlpatterns = [
    path('', views.resource, name='resource'),
]