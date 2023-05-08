"""blog_app URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path,include
from common import views
from common.views import error_404_view,error_500_view,error_403_view,error_400_view
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index_views),
    path('article/', include('article.urls', namespace='article')),
    path('users/', include('users.urls', namespace='users')),
    path('common/', include('common.urls', namespace='common')),
    path('comment/', include('comment.urls', namespace='comment')),
    path('resource/', include('resource.urls', namespace='resource')),
    path('captcha/', include('captcha.urls')),
    path('ueditor/', include('DjangoUeditor.urls')),
]
#添加这行
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATICFILES_DIRS)

handler404 = error_404_view
handler403 = error_403_view
handler400 = error_400_view
handler500 = error_500_view