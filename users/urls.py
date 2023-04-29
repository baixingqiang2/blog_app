from django.urls import path
from . import views


app_name = 'users'

urlpatterns = [
    # 登录
    path(r'login/', views.UserLogin.as_view(), name='login'),
    # 退出登录
    path(r'logout/', views.UserLogout.as_view(),name='logout'),
    # 注册
    path(r'register/', views.user_register_fist, name='register_email'),
    # path(r'register/(?<email>[a-z]+)/', views.user_register_two,name='register'),
    path(r'register/(?<str:email>[a-z]+)/', views.user_register_two,name='register'),
    path(r'', views.user_register_three,name='register_success'),
    # 删除账号
    path(r'delete/<int:id>/', views.user_delete, name='delete'),
    # 用户信息
    path(r'profile/<int:id>/', views.profile, name='profile'),
    # 修改个人信息
    path(r'profile/<int:id>/edit', views.profile_edit, name='edit'),
    # 修改密码
    path(r'modified/<int:id>/',views.modifiedpwd,name='modified_pwd'),
    # 找回密码
    path(r'restpwd/',views.forgot_password, name='forgot_password'),
    path(r'restpwd/(?<email>[a-z]+)/',views.reset_password, name='reset_password'),
    path(r'',views.reset_success, name='reset_success'),
    # 发送验证码
    path('send-code/<email>/', views.send_code, name='send_code'),

]