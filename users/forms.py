from django import forms
from captcha.fields import CaptchaField
# 引入 Profile 模型
from .models import Profile


class ProfileForm(forms.ModelForm):  # 用户信息表单
    class Meta:
        model = Profile
        fields = ('phone', 'avatar', 'another', 'bio','signs')


class UserLoginForm(forms.Form):  # 登录表单

    username = forms.CharField(label="用户名", max_length=128, widget=forms.TextInput(attrs={'class' : 'form-control'}))
    password = forms.CharField(label="密码", max_length=256, widget=forms.PasswordInput(attrs={'class' : 'form-control'}))


class EmailRegisterFrom(forms.Form):  # 注册验证邮箱表单

    email = forms.EmailField(required=True, error_messages={'required' : '邮箱不能为空.'})
    captcha = CaptchaField(error_messages={'invalid' : '验证码错误'})


class UserRegisterForm(forms.ModelForm):  # 注册用户表单

    username = forms.CharField(required=True, error_messages={'required': '用户名不能为空.'})
    # 复写 User 的密码
    password1 = forms.CharField(required=True, min_length=6, error_messages={'required': '密码不能为空.', 'min_length': "至少6位"})
    password2 = forms.CharField(required=True, min_length=6, error_messages={'required': '密码不能为空.', 'min_length': "至少6位"})
    # captcha = CaptchaField(error_messages={'invalid' : '验证码错误'})
    code = forms.CharField(required=True, error_messages={'required': '输入正确的验证码'})

    class Meta:
        model = Profile
        fields = ('username', 'email')

    def clean_username(self):
        username = self.cleaned_data.get('username')
        user_obj = Profile.objects.filter(username='username')
        if user_obj:
            self.add_error('username', '用户名已存在')
        return username


class ResetPassForm(forms.Form):  # 重置密码表单

    code = forms.CharField(required=True,min_length=6)
    newpwd1 = forms.CharField(required=True,min_length=6,error_messages={'required': '密码不能为空.', 'min_length': "至少6位"})
    newpwd2 = forms.CharField(required=True, min_length=6, error_messages={'required': '密码不能为空.', 'min_length': "至少6位"})


class EmailResetPwdForm(forms.Form):  # 重置密码验证邮箱表单

    email = forms.EmailField(required=True, error_messages={'required' : '邮箱不能为空.'})

    def clean_email(self):
        email = self.cleaned_data.get('email')
        user_obj = Profile.objects.filter(email='email')
        if user_obj :
            self.add_error('email', '用户名已存在')
        return email


class ModifiedPwdForm(forms.Form):  # 修改密码表单

    old_pwd = forms.CharField(required=True, min_length=6,error_messages={'required' : '密码不能为空.', 'min_length' : "至少6位"})
    new_pwd = forms.CharField(required=True, min_length=6,error_messages={'required' : '密码不能为空.', 'min_length' : "至少6位"})
    new_pwd1 = forms.CharField(required=True, min_length=6,error_messages={'required' : '密码不能为空.', 'min_length' : "至少6位"})
