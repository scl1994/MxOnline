# coding=utf-8

from django.shortcuts import render
from django.contrib.auth import authenticate, login
from django.contrib.auth.backends import ModelBackend
from django.db.models import Q  # django的查询多参数为与关系，用Q可改成或关系
from django.views.generic.base import View
from django.contrib.auth.hashers import make_password
from django.contrib.auth.mixins import LoginRequiredMixin

from .models import UserProfile, EmailVerifyRecord
from .forms import LoginForm, RegisterForm, ForgetPwdForm, ModifyPwdForm, UploagImageForm
from utils.email_send import send_register_mail


# Create your views here.

class CustomBackend(ModelBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        try:
            # 无论时用户名还是邮箱都通过username传入
            # 这里使用Q的语法将用户名的查询改为了查询用户名或邮箱，满足一个即可登录，
            # |表示或关系。都好表示与关系
            user = UserProfile.objects.get(Q(username=username) | Q(email=username))
            # 注意django在存储密码时加密了，所以不能将密码直接传进去查询验证，要用默认函数
            if user.check_password(password):
                return user
        except Exception as e:
            return None


# 注册
class RegisterView(View):
    def get(self, request):
        register_form = RegisterForm()
        return render(request, "register.html", {'register_form': register_form})

    def post(self, request):
        register_form = RegisterForm(request.POST)
        if register_form.is_valid():
            user_name = request.POST.get("email", "")
            if UserProfile.objects.filter(email=user_name):
                return render(request, 'register.html', {"msg": '用户已经存在', "register_form": register_form})
            pass_word = request.POST.get("password", "")
            user_profile = UserProfile()
            user_profile.username = user_name
            user_profile.email = user_name
            user_profile.is_active = False
            # 密码传过来的时明文密码，存储时要变成加密的文本
            user_profile.password = make_password(pass_word)
            # 记住保存user信息
            user_profile.save()

            send_register_mail(user_name, "register")
            # 注册成功，返回登录页面
            return render(request, "login.html")
        else:
            # 输入的帐号密码未能通过验证，返回注册页面
            return render(request, 'register.html', {"register_form": register_form})


# 用户通过邮箱链接激活账户
class ActiveUserView(View):
    def get(self, request, active_code):
        # 用户点击激活链接，查询验证邮件记录
        all_records = EmailVerifyRecord.objects.filter(code=active_code)
        if all_records:
            for record in all_records:
                # 从记录中取出邮件，找到对应用户，将UserProfile的is_active改为true，激活用户
                if record.is_active:
                    email = record.email
                    user = UserProfile.objects.get(email=email)
                    #  将激活链接无效化
                    record.is_active = False
                    record.save()
                    user.is_active = True
                    # 激活用户后要保存
                    user.save()
                else:
                    return render(request, 'login.html', {'msg': '帐号激活链接已失效，可尝试登录'})
        else:
            # 验证失败
            return render(request, 'active_fail.html')
        # 验证成功，返回登录页面
        return render(request, 'login.html')


# 基于类实现登录功能
class LoginView(View):
    # 重写get方法，当遇到get请求时，会自定调用get函数
    def get(self, request):
        return render(request, "login.html", {})

    def post(self, request):
        # 使用forms验证用户输入的用户名和密码是否正确，要求forms中定义的名字要与POST中的字段名字相同，
        # 也就是和前端的input标签的name属性对应起来，这样才会取验证对应字段是否正确。
        login_form = LoginForm(request.POST)
        if login_form.is_valid():
            user_name = request.POST.get("username", "")
            pass_word = request.POST.get("password", "")
            # authenticate默认使用用户名认证，如果要定义邮箱，需要自定义
            user = authenticate(username=user_name, password=pass_word)
            if user is not None:
                if user.is_active:
                    # 使用django自带的login函数实现登录
                    login(request, user)
                    return render(request, 'index.html')
                else:
                    return render(request, 'login.html', {'msg': '用户未激活!'})
            # 验证失败，返回到登录页面
            else:
                return render(request, "login.html", {'msg': '用户名或密码错误！'})
        else:
            return render(request, "login.html", {'login_form': login_form})


class ForgetPwdView(View):
    def get(self, request):
        forget_form = ForgetPwdForm()
        return render(request, 'forgetpwd.html', {'forget_form': forget_form})

    def post(self, request):
        forget_form = ForgetPwdForm(request.POST)
        if forget_form.is_valid():
            email = request.POST.get('email', '')
            send_register_mail(email, "forget")
            return render(request, "send_success.html")
        else:
            return render(request, 'forgetpwd.html', {'forget_form': forget_form})


# 重置密码（发送邮件）
class ResetView(View):
    def get(self, request, reset_code):
        # 用户点击激活链接，查询验证邮件记录
        all_records = EmailVerifyRecord.objects.filter(code=reset_code)
        if all_records:
            for record in all_records:
                # 从记录中取出邮件，找到对应用户，将UserProfile的is_active改为true，激活用户
                if record.is_active:
                    email = record.email
                    record.is_active = False
                    record.save()
                    return render(request, "password_reset.html", {"email": email})
                else:
                    return render(request, 'login.html', {'msg': '密码重置链接已失效，可尝试登录'})
        else:
            # 验证失败
            return render(request, 'active_fail.html')
        # 验证成功，返回登录页面
        return render(request, 'login.html')


# 修改密码
class ModifyPwdView(View):
    def post(self, request):
        modify_form = ModifyPwdForm(request.POST)
        if modify_form.is_valid():
            pwd1 = request.POST.get("password1", '')
            pwd2 = request.POST.get("password2", '')
            email = request.POST.get("email", '')
            if pwd1 != pwd2:
                return render(request, "password_reset.html", {"email": email, 'msg': '密码不一致！'})
            user = UserProfile.objects.get(email=email)
            user.password = make_password(pwd1)
            user.save()

            return render(request, 'login.html')
        else:
            email = request.POST.get("email", '')
            return render(request, "password_reset.html", {"email": email, "modify_form": modify_form})


class UserInfoView(LoginRequiredMixin, View):
    """ 用户个人信息"""
    def get(self, request):
        return render(request, 'usercenter-info.html', {

        })


class UploadImageView(LoginRequiredMixin, View):
    """用户修改头像"""
    def post(self, request):
        # 这里的upform是一个modelform，通过给intance传入model对象，可直接对image_form进行数据库保存操作，他即是form又是model
        image_form = UploagImageForm(request.POST, request.FILES, instance=request.user)
        if image_form.is_valid():
            image_form.save()
            pass