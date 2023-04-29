from django.db import models

#公告栏
class Notice(models.Model):
    STATUS_COLOR = (
        ('r', '#009688'),
        ('n', 'red'),
    )
    notice_name = models.CharField('公告内容',max_length=100)
    notice_url = models.URLField('公告网址', max_length=100,blank=True)
    is_notice = models.CharField('跳转按钮是否存在', max_length=20, blank=True)
    notice_color= models.CharField('字体颜色', max_length=8, blank=True, choices = STATUS_COLOR, default = 'r')
    class Meta:
        verbose_name = "公告"

    def __str__(self):
        #将文章标题返回
        return self.notice_name

#Banner轮播图
class Banner(models.Model):
    text_info = models.CharField('标题', max_length=50, default='')
    img = models.ImageField('轮播图', upload_to='banner/')
    link_url = models.URLField('图片链接', max_length=100)
    is_active = models.BooleanField('是否是active', default=False)

    def __str__(self):
        return self.text_info

    class Meta:
        verbose_name = '轮播图'
        verbose_name_plural = '轮播图'

#友情链接
class Link(models.Model):
    name = models.CharField('链接名称', max_length=20)
    linkurl = models.URLField('网址',max_length=100)

    def __str__(self):
        return self.name
    class Meta:
        verbose_name = '友情链接'
        verbose_name_plural = '友情链接'
