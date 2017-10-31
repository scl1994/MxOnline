# coding=utf-8

from django.shortcuts import render
from django.contrib.auth import authenticate, login
from django.contrib.auth.backends import ModelBackend
from django.db.models import Q    # django的查询多参数为与关系，用Q可改成或关系
from django.views.generic.base import View

from .models import UserProfile
from .forms import LoginForm


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


# 基于函数实现登录功能
# def user_login(request):
#     if request.method == "POST":
#         user_name = request.POST.get("username", "")
#         pass_word = request.POST.get("password", "")
#         # authenticate默认使用用户名认证，如果要定义邮箱，需要自定义
#         user = authenticate(username=user_name, password=pass_word)
#         if user is not None:
#             login(request, user)
#             return render(request, 'index.html')
#         else:
#             return render(request, "login.html", {'msg': '用户名或密码错误！'})
#     elif request.method == "GET":
#         return render(request, "login.html", {})


# 基于类实现登录功能
class LoginView(View):
    # 重写get方法，当遇到get请求时，会自定调用get函数
    def get(self, request):
        return render(request, "login.html", {})

    def post(self, request):
        # 使用forms验证用户输入的用户名和密码是否正确，要求forms中定义的名字要与POST中的字段名字相同，
        # 也就是和前端的input标签的名字对应起来，这样才会取验证对应字段是否正确。
        login_form = LoginForm(request.POST)
        if login_form.is_valid():
            user_name = request.POST.get("username", "")
            pass_word = request.POST.get("password", "")
            # authenticate默认使用用户名认证，如果要定义邮箱，需要自定义
            user = authenticate(username=user_name, password=pass_word)
            if user is not None:
                # 使用django自带的login函数实现登录
                login(request, user)
                return render(request, 'index.html')
            # 验证失败，返回到登录页面
            else:
                return render(request, "login.html", {'msg': '用户名或密码错误！'})
        else:
            return render(request, "login.html", {'login_form': login_form})
