from django.contrib.auth.models import User
from django.contrib.auth.models import User
from django.db import models
from mptt.models import MPTTModel, TreeForeignKey
from DjangoUeditor.models import UEditorField

from article.models import ArticlePost
from article.models import ArticlePost
# 博文的评论
from users.models import Profile


# # 博文的评论
class Comment(MPTTModel):
    content = UEditorField(max_length=500,verbose_name='评论内容')
    pub_date = models.DateTimeField(auto_now_add=True,verbose_name='评论时间')
    author = models.ForeignKey(Profile, on_delete=models.CASCADE,related_name='comments',verbose_name='评论人')
    article =models.ForeignKey(ArticlePost,on_delete=models.CASCADE,related_name='comments',verbose_name='评论的文章')
    # 新增，mptt树形结构
    parent = TreeForeignKey('self',on_delete=models.CASCADE,null=True,blank=True,related_name='children',verbose_name='回复的评论')
    # 新增，记录二级评论回复给谁, str
    reply_to = models.ForeignKey(Profile,null=True,blank=True,on_delete=models.CASCADE,related_name='replyers',verbose_name='回复谁')

    def __str__(self) :
        return self.content[:20]

    class MPTTMeta:
        ordering = ('pub_date',)
        verbose_name = "评论列表"
        verbose_name_plural = verbose_name



# 网站留言
class Message(models.Model):#
    # 定义字段
    # max_length为必填字段，对应数据库中的varchar类型，verbose_name可理解为注释，并设置为主键
    name = models.CharField(max_length=20, verbose_name="姓名",primary_key=True)
    # EmailField是在CharField上的封装，会检测是否为邮箱，按住CTRL+左键点入可看到，已经默认设置了max_length,为254
    email = models.EmailField(verbose_name="邮箱")
    phone = models.CharField(max_length=30, verbose_name="联系电话",blank= True)
    # TextField不限字段长度
    message = models.TextField(verbose_name="留言信息")
    suggest = models.TextField(verbose_name="建议信息",blank=True)

    # 表中的meta信息
    class Meta:
        verbose_name = "留言列表"
        verbose_name_plural = verbose_name
        # 可以自己指定表名
        # 可以自己指定表名
        db_table = "message"



