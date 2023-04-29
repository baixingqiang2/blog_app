import os
import uuid
from django.db import models
from article.models import Category


def user_directory_path(instance, filename):
    ext = filename.split('.')[-1]
    filename = '{}.{}'.format(uuid.uuid4().hex[:10], ext)
    return os.path.join("files", filename)


class File(models.Model):
    name = models.CharField(max_length=30,verbose_name='文件名')
    file = models.FileField(upload_to=user_directory_path, null=True,verbose_name='文件链接')
    category = models.ForeignKey(Category, on_delete=models.DO_NOTHING, verbose_name='分类', blank=True, null=True)
    slug = models.SlugField('slug', max_length=40, blank=True)
    excerpt = models.CharField(max_length=50, verbose_name='摘要')

    # # 获取文章地址
    # def get_absolute_url(self):
    #     return reverse('resource:resource', args=[self.slug])

    def __str__(self) :
        return self.name

    class Meta :
        ordering = ['name']
        verbose_name = "文件列表"
        verbose_name_plural = verbose_name


class PictureWall(models.Model):
    name = models.CharField(max_length=40,verbose_name='名称')
    picture_url = models.ImageField(upload_to='picture/%Y%m%d/', verbose_name='图片地址')

    class Meta :
        # ordering 指定模型返回的数据排列顺序
        # ‘create_time'表明数据应以倒序排列
        ordering = ('-id',)
        verbose_name = "照片墙"
        verbose_name_plural = verbose_name

    def __str__(self) :
        # 将文章标题返回
        return self.name
