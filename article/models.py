import markdown
from PIL import Image
from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.urls import reverse
from django.utils.html import strip_tags
from taggit.managers import TaggableManager
from unidecode import unidecode
from django.template.defaultfilters import slugify
# 文章分类
from users.models import Profile
from DjangoUeditor.models import UEditorField

class Category(models.Model):
    name = models.CharField('栏目分类', max_length=100)
    slug = models.SlugField('slug', max_length=40)
    parent_category = models.ForeignKey('self', verbose_name="父级分类", blank=True, null=True, on_delete=models.CASCADE)

    index = models.IntegerField(default=999, verbose_name='分类排序')

    def get_absolute_url(self):
        return reverse('blog:category_detail', args=[self.slug])

    def has_child(self):
        if self.category_set.all().count() > 0:
            return True

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['name']
        verbose_name = "分类"
        verbose_name_plural = verbose_name

# 文章关键词，用来作为 SEO 中 keywords
class Keyword(models.Model):
    name = models.CharField('文章关键词', max_length=20)

    class Meta:
        verbose_name = '关键词'
        verbose_name_plural = verbose_name
        ordering = ['name']

    def __str__(self):
        return self.name

#推荐位
class Tui(models.Model):
    name = models.CharField('推荐位',max_length=100)

    class Meta:
        verbose_name = '推荐位'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name

def default_image():
    # 返回默认图片的路径
    return '../media/article/default.jpg'
# 博客文章数据类型
class ArticlePost(models.Model):
    STATUS_CHOICES = (
        ('d', '草稿'),
        ('p', '发表'),
    )
    #文章作者
    author = models.ForeignKey(Profile,verbose_name='作者',on_delete=models.CASCADE)
    #文章标题
    title=models.CharField(max_length=100,verbose_name='标题')
    excerpt = models.CharField(max_length=100, verbose_name='摘要')
    slug = models.SlugField('slug', max_length=60, blank=True)
    # 文章正文

    body = UEditorField(verbose_name='内容')
    # 标题图
    avatar = models.ImageField(upload_to='article/%Y%m%d/', verbose_name='文章图片',default=default_image, blank=True)
    category = models.ForeignKey(Category, on_delete=models.DO_NOTHING, verbose_name='分类', blank=True, null=True)
    tui = models.ForeignKey(Tui, on_delete=models.DO_NOTHING, verbose_name='推荐位', blank=True, null=True)
    #文章标签
    tags =TaggableManager(blank=True,)

    # 文章创建时间
    create_date=models.DateTimeField('创建时间',auto_now_add=True)
    # 文章更新时间
    update_date= models.DateTimeField('修改时间',auto_now=True)
    #文章发布时间
    pub_date = models.DateTimeField('发布时间',default=timezone.now)
    status = models.CharField('文章状态', max_length=1, choices=STATUS_CHOICES,default='d')
    #统计文章浏览量
    total_views = models.PositiveIntegerField(default=0,verbose_name='浏览量')
    # 新增点赞数统计
    likes = models.PositiveIntegerField(default=0,verbose_name='点赞',blank=True)
    # users_like = models.ManyToManyField(Profile,related_name='articles_liked', blank=True)
    # 文章关键词多对多文章
    keywords = models.ManyToManyField(Keyword, blank=True,verbose_name='文章关键词', help_text='文章关键词，用来作为SEO中keywords，最好使用长尾词，3-4个足够')
    # 保存时出处理图片
    def save(self, *args, **kwargs) :
        if not self.id or not self.slug:
            # Newly created object, so set slug
            self.slug = slugify(unidecode(self.title))
        if not self.excerpt:  #自动生成摘要
            # 首先实例化一个 Markdown 类，用于渲染 body 的文本
            md = markdown.Markdown(extensions=[
                'markdown.extensions.extra',
                'markdown.extensions.codehilite',
            ])
            # 先将 Markdown 文本渲染成 HTML 文本
            # strip_tags 去掉 HTML 文本的全部 HTML 标签
            # 从文本摘取前 54 个字符赋给 excerpt
            self.excerpt = strip_tags(md.convert(self.body))[:54]

            # 调用父类的 save 方法将数据保存到数据库中

        super().save(*args, **kwargs)

        article = super(ArticlePost, self).save(*args, **kwargs)
        if self.avatar and not kwargs.get('update_fields'):  # 上传图片的处理
            image = Image.open(self.avatar)
            (x, y) = image.size
            new_x = 400
            new_y = int(new_x * (y / x))
            resized_image = image.resize((new_x, new_y), Image.ANTIALIAS)
            resized_image.save(self.avatar.path)
        return article
    # 获取文章地址
    def get_absolute_url(self) :
        return reverse('article:article_detail', args=[self.slug,self.id])
    # 内部类
    class Meta:
        #ordering 指定模型返回的数据排列顺序
        #‘create_time'表明数据应以倒序排列

        ordering = ('-create_date',)
        verbose_name = "文章管理"
        verbose_name_plural = verbose_name

    def __str__(self):
        # 将文章标题返回
        return self.title[:20]
    # 点赞+1方法
    def update_loves(self):
        self.likes += 1
        self.save(update_fields=['likes']) #更新字段

    # 浏览+1方法
    def update_views(self):
        self.total_views += 1
        self.save(update_fields=['total_views']) #更新字段

    #前篇方法：当前小于文章并倒序排列的第一个
    def get_pre(self):
        return ArticlePost.objects.filter(id__lt=self.id).order_by('-id').first()
    #后篇方法：当前大于文章并正序排列的第一个
    def get_next(self):
        return ArticlePost.objects.filter(id__gt=self.id).order_by('id').first()

# #点赞
class Like(models.Model):
    like_article = models.ForeignKey(ArticlePost, on_delete=models.CASCADE, verbose_name='所属文章')
    like_user = models.ForeignKey(Profile, on_delete=models.CASCADE, verbose_name='点赞者')
    pub_date = models.DateTimeField(auto_now_add=True, verbose_name='点赞时间')