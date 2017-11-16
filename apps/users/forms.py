# 定义forms验证用户输入

from django import forms
from captcha.fields import CaptchaField

from .models import UserProfile


class LoginForm(forms.Form):
    username = forms.CharField(required=True)
    password = forms.CharField(required=True, min_length=5)


class RegisterForm(forms.Form):
    email = forms.EmailField(required=True)
    password = forms.CharField(required=True, min_length=5)
    # 验证码字段
    captcha = CaptchaField(error_messages={'invalid': '验证码错误'})


class ForgetPwdForm(forms.Form):
    email = forms.EmailField(required=True)
    # 验证码字段
    captcha = CaptchaField(error_messages={'invalid': '验证码错误'})


class ModifyPwdForm(forms.Form):
    password1 = forms.CharField(required=True, min_length=5)
    password2 = forms.CharField(required=True, min_length=5)


class UploagImageForm(forms.ModelForm):
    # 管理头像文件上传
    class Meta:
        model = UserProfile
        fields = ['image']


class UserInfoForm(forms.ModelForm):
    # 管理头像文件上传
    class Meta:
        model = UserProfile
        fields = ['nick_name', 'gender', 'birthday', 'address', 'mobile']
