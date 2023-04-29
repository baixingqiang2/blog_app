from captcha.helpers import captcha_image_url
from captcha.models import CaptchaStore
from django.contrib.auth.hashers import make_password,check_password
from django.core.exceptions import ObjectDoesNotExist
from django.core.validators import validate_email
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login,logout
from django.http import HttpResponse, JsonResponse
# 引入验证登录的装饰器
from django.contrib.auth.decorators import login_required
# 引入表单类
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST

from .forms import ProfileForm,UserRegisterForm,UserLoginForm,EmailRegisterFrom,EmailResetPwdForm,ResetPassForm,ModifiedPwdForm
from .models import Profile,EmailVerifyRecord
from django.views import View
# Create your views here.
from .util import send_code_email, check_email, check_code, random_str


# 用户登录
class UserLogin(View):
    """用户名登录"""

    def get(self, request):
        """
        提供登录界面
        :param request: 请求对象
        :return: 登录界面
        """
        user_login_form = UserLoginForm()
        context = {'form' : user_login_form}
        return render(request, 'users/login.html', context)

    def post(self, request):
        """
        实现登录逻辑
        """
        user_login_form = UserLoginForm(data=request.POST)
        if user_login_form.is_valid() :
            # .cleaned_data 清洗出合法数据
            data = user_login_form.cleaned_data
            # 检验账号、密码是否正确匹配数据库中的某个用户
            # 如果均匹配则返回这个 user 对象
            user = authenticate(username=data['username'], password=data['password'])
            if user:
                # 将用户数据保存在 session 中，即实现了登录动作
                login(request, user)
                return redirect("common:home")
            else :
                username_error = "输入有误~"
                return render(request,'users/login.html',{'username_error':username_error})
        else :
            if len(request.POST.get('username')) < 1:
                username_error = "账号不能为空"
                return render(request, 'users/login.html', {'username_error' : username_error})
            else:
                password_error = "密码不能为空"
                return render(request, 'users/login.html', {'password_error' : password_error})
            # return HttpResponse("账号或密码输入不合法")
# 用户退出
class UserLogout(View):

    def get(self, request):
        # 退出时清理session
        logout(request)
        response = redirect('common:home')
        # 清理cookie中的username信息
        response.delete_cookie('username')
        # 重定向到首页
        return response
# 注册（发送邮箱验证码）
@csrf_exempt
def send_code(request,email):
    if request.method == 'POST':
        verification_code = random_str(6)
        send_code_email(email, verification_code)
        response = {'success': True}
        return JsonResponse(response)


def user_register_fist(request):
    if request.session.get('is_login', None) :
        #     # 登录状态不允许注册，你可以修改这条原则
        return redirect('common:home')
    else:
        if request.method == 'GET':
            hashkey = CaptchaStore.generate_key()
            # 生成验证码地址
            image_url = captcha_image_url(hashkey)
            context = {
                'hashkey':hashkey,
                'image_url':image_url,
            }
            return render(request, 'users/register_again.html', context)
        if request.method == 'POST':
            hashkey = CaptchaStore.generate_key()
            # 生成验证码地址
            image_url = captcha_image_url(hashkey)
            context = {
                'hashkey' : hashkey,
                'image_url' : image_url,
            }
            email_form = EmailRegisterFrom(request.POST)
            # 验证
            if email_form.is_valid():
                email = email_form.cleaned_data['email']
                if Profile.objects.filter(email=email) :  # 邮箱地址唯一
                    email_error = '该邮箱地址已被注册！'
                    context.update({'email_error' : email_error})
                    return render(request, 'users/register_again.html', context)
                elif check_email(email) :  # 邮箱格式正确
                    # # 生成验证码
                    # verification_code = random_str(6)
                    # # 将验证码保存在记录中，并给用户发邮件
                    # send_code_email(email, verification_code)
                    # 返回成功的响应
                    return redirect('users:register', email=email)
                else :
                    email_error = '邮箱格式不正确'
                    context.update({'email_error' : email_error})
                    return render(request, 'users/register_again.html', context)
            else :
                return render(request, 'users/register_again.html', context)

# 用户注册
def user_register_two(request,email):

    if request.method == 'GET':
        # 如果请求不是POST，则渲染的是一个空的表单。
        register_form = UserRegisterForm()
        context = {'form' : register_form,'emails':email,}
        # 如果用户通过表单提交数据，但是数据验证、不合法，则渲染的是一个带有错误信息的表单
        return render(request, 'users/register.html', context)
    if request.method == "POST":
        register_form = UserRegisterForm(data=request.POST)
        message = "请检查填写的内容！"
        if register_form.is_valid():  # 获取数据
            username = register_form.cleaned_data['username']
            password1 = register_form.cleaned_data['password1']
            password2 = register_form.cleaned_data['password2']
            code = register_form.cleaned_data['code']

            if check_code(email,code):#判断邮箱验证码是否正确
                same_name_user = Profile.objects.filter(username=username)
                if same_name_user :  # 用户名唯一
                    username_error = '用户已经存在，请重新选择用户名！'
                    return render(request, 'users/register.html', {'username_error' : username_error})
                else:
                    if password1 != password2 :  # 判断两次密码是否相同
                        password_error = "两次输入的密码不同！"
                        return render(request, 'users/register.html', {'password_error' : password_error})
                    else:# 当一切都OK的情况下，创建新用户
                        new_user = Profile.objects.create()
                        new_user.username = username
                        new_user.set_password(password1)
                        new_user.email = email
                        new_user.save()
                        return redirect('users:register_success')  # 自动跳转到注册成功页面
            else:
                code_error = "请输入正确的验证码"
                return render(request, 'users/register.html', locals())
        else:
            return render(request, 'users/register.html', locals())
# 用户注册成功
def user_register_three(request):
    return render(request, 'users/register_success.html', locals())

# 删除用户
@login_required(login_url='/users/login/')
def user_delete(request, id):
    user = Profile.objects.get(id=id)
    # 验证登录用户、待删除用户是否相同
    if request.user == user:
        #退出登录，删除数据并返回博客列表
        logout(request)
        user.delete()
        return redirect("common:home")
    else:
        return HttpResponse("你没有删除操作的权限。")

# 用户信息
@login_required(login_url='/users/login/')
def profile(request, id):
    users= Profile.objects.filter(id=id).all()
    profiles = Profile.objects.filter(id=id).all()
    context = {
        'profiles': profiles,
        'users': users
    }
    return render(request,'users/profile.html',context)

# 编辑用户信息
@login_required(login_url='/users/login/')
def profile_edit(request, id):
    # user_id 是 OneToOneField 自动生成的字段
    profile = Profile.objects.get(id=id)
    if request.method == 'POST':
        # 验证修改数据者，是否为用户本人
        if request.user != profile:
            return HttpResponse("你没有权限修改此用户信息。")

        profile_form = ProfileForm(data=request.POST)
        if profile_form.is_valid():
            # 取得清洗后的合法数据
            profile_cd = profile_form.cleaned_data
            profile.another = profile_cd['another']
            profile.phone = profile_cd['phone']
            sings =request.POST.get('sings')
            if 'sings':
                profile.signs = sings
            profile.bio = profile_cd['bio']
            avatar = request.FILES.get('avatar')
            if 'avatar':
                profile.avatar = avatar
            profile.save()
            # 带参数的 redirect()
            return redirect("users:profile", id=id)
        else:
            return HttpResponse("注册表单输入有误。请重新输入~")

    elif request.method == 'GET':
        profile_form = ProfileForm()
        context = { 'profile_form': profile_form, 'profile': profile, 'user': profile}
        return render(request, 'users/edit.html', context)
    else:
        return HttpResponse("请使用GET或POST请求数据")


# 修改密码
@login_required(login_url='/users/login/')
def modifiedpwd(request,id):
    if request.method == 'GET':
        users = Profile.objects.filter(id=id)
        return render(request, 'users/modified_password.html', {'users':users})
    if request.method == 'POST':
        user_password = Profile.objects.get(id=id)
        modefied_form = ModifiedPwdForm(data=request.POST)
        if modefied_form.is_valid():
            old_password = modefied_form.cleaned_data['old_pwd']
            new_password = modefied_form.cleaned_data['new_pwd']
            new_password1 = modefied_form.cleaned_data['new_pwd1']
            if check_password(old_password,user_password.password):#判断旧密码是否正确
                if new_password != new_password1:#判断两次输入的密码
                    password_error = '两次输入密码不一致'
                    return render(request, 'users/modified_password.html',{'password_error':password_error})
                elif old_password == new_password:
                    password_error = '新密码不能和旧密码相同'
                    return render(request, 'users/modified_password.html', {'password_error' : password_error})
                else:
                    user_password.set_password(new_password)
                    user_password.save()
                    UserLogout()
                    return redirect('users:login')
            else:
                old_password_error = '登录密码输入错误'
                return render(request, 'users/modified_password.html', {'old_password_error' : old_password_error})

        else:
            password_error = '请检查输入内容'
            return render(request, 'users/modified_password.html', {'old_password_error' : password_error})


# 忘记密码
def forgot_password(request):
    if request.method == 'GET' :
        forgot_form = EmailResetPwdForm()
        return render(request, 'users/forgot_password.html',{'forgot_form':forgot_form})

    if request.method == 'POST' :
        forgot_form = EmailResetPwdForm(request.POST)
        if forgot_form.is_valid():
            email = forgot_form.cleaned_data['email']
            email_check = Profile.objects.filter(email=email)
            if email_check:
                return redirect( 'users:reset_password', email)
            else:
                email_error = '该邮箱未被注册'
                return render(request, 'users/forgot_password.html', {'email_error' : email_error})
        else:
            email_error = '邮箱格式不正确'
            return render(request, 'users/forgot_password.html', {'email_error' : email_error})

# 重置密码
def reset_password(request,email):
    if request.method == 'GET':
        emails=email
        reset_form = ResetPassForm()
        return render(request, 'users/reset_password.html',{'reset_form':reset_form,'emails':emails})

    if request.method == 'POST':
        user_profile = Profile.objects.get(email=email)
        reset_form = ResetPassForm(data=request.POST)
        if reset_form.is_valid():
            code = reset_form.cleaned_data['code']
            newpwd1 = reset_form.cleaned_data['newpwd1']
            newpwd2 = reset_form.cleaned_data['newpwd2']
            code_check = EmailVerifyRecord.objects.values('code').filter(email=email).order_by('-send_time')[0].get('code')
            if newpwd1 != newpwd2:
                password_error = '两次输入的密码不一致'
                return render(request, 'users/reset_password.html',{'password_error':password_error})
            elif code != code_check:
                code_error = '邮箱验证码错误'
                return render(request, 'users/reset_password.html', {'code_error' : code_error})
            else:  # 保存修改密码
                user_profile.set_password(newpwd1)
                user_profile.save()
                return render(request, 'users/reset_password_success.html', )
        else:
            return render(request, 'users/reset_password.html')


def reset_success(request):  # 重置密码成功

    return render(request, 'users/reset_password_success.html')