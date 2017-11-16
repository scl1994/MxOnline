"""MxOnline URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from django.contrib import admin
from django.views.generic import TemplateView
from django.views.static import serve
import xadmin

from users.views import LoginView, RegisterView, ActiveUserView, ForgetPwdView, ResetView, ModifyPwdView
from MxOnline.settings import MEDIA_ROOT


urlpatterns = [
    url(r'^xadmin/', xadmin.site.urls),

    url(r"^$", TemplateView.as_view(template_name='index.html'), name='index'),
    # 注意这里的as_view要交括号，这样就将LoginView类变成了一个试图函数

    url(r"^login/$", LoginView.as_view(), name='login'),

    url(r"^register/$", RegisterView.as_view(), name='register'),

    # 下面时请求验证码图片的请求，是django-simple-captcha模块配置的
    # 这里有点像flask的蓝本，在每个app下可以定义自己的路由，相同前缀的直接路由到对应app下的url定义中
    url(r'^captcha/', include('captcha.urls')),

    # 使用了动态变化的url语法，(?P<变量名>正则表达式)，用于激活用户帐号
    url(r'^active/(?P<active_code>.*)/$', ActiveUserView.as_view(), name='user_active'),

    url(r"^forget/$", ForgetPwdView.as_view(), name='forget_pwd'),

    url(r'^reset/(?P<reset_code>.*)/$', ResetView.as_view(), name='reset_pwd'),

    url(r"^modify_pwd/$", ModifyPwdView.as_view(), name='modify_pwd'),

    # 课程机构url配置
    url(r'^org/', include('organization.urls', namespace='org')),

    # 配置上传文件的访问处理函数
    url(r'^media/(?P<path>.*)$', serve, {"document_root": MEDIA_ROOT}),

    # 课程url配置
    url(r'^course/', include('courses.urls', namespace='course')),

    # 用户配置
    url(r'^users/', include('users.urls', namespace='users')),


]
