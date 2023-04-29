from django.db import models
from django.contrib.auth.models import User
# 引入内置信号
from django.db.models.signals import post_save
# 引入信号接收器的装饰器
from django.dispatch import receiver
from django.contrib.auth.models import AbstractUser
from django.utils import timezone

class Profile(AbstractUser):
    #别名字段
    another =models.CharField('昵称',max_length=20,default='', blank=True)
    # 电话号码字段
    phone = models.CharField('电话',max_length=20, default='',blank=True)
    # 头像
    avatar = models.ImageField('头像',upload_to='avatar/%Y%m%d/',default='avatar/Logo_40.png', blank=True)
    # 个人简介
    signs = models.TextField('个性签名',max_length=100,default='暂无签名', blank=True)
    bio = models.TextField('个人简介',max_length=500, default='暂无简介',blank=True)
    # address

    def __str__(self):
        return self.username

    class Meta:
        verbose_name = '用户信息'
        verbose_name_plural=verbose_name


# 信号接收函数，每当新建 User 实例时自动调用
# @receiver(post_save, sender=Profile)
# def create_user_profile(sender, instance, created, **kwargs):
#     if created:
#         Profile.objects.create(Prfile=instance)

# 信号接收函数，每当更新 User 实例时自动调用
# @receiver(post_save, sender=Profile)
# def save_user_profile(sender, instance, **kwargs):
#     instance.profile.save()

# 邮箱验证
class EmailVerifyRecord(models.Model):
    # 验证码
    code = models.CharField(max_length=20, verbose_name="验证码")
    email = models.EmailField(max_length=50, verbose_name="邮箱")
    # 包含注册验证和找回验证
    send_type = models.CharField(verbose_name="验证码类型", max_length=10,choices=(("register", "注册"), ("forget", "找回密码")))
    send_time = models.DateTimeField(verbose_name="发送时间", default=0,)

    def is_valid(self) :#判断是否有效
        return (timezone.now() - self.send_time).seconds < 300

    class Meta:
        verbose_name = "邮箱验证码"
        verbose_name_plural = verbose_name

    def __unicode__(self):
        return '{0}({1})'.format(self.code, self.email)


 #自定义myUser类

