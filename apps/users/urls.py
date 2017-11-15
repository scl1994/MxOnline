from django.conf.urls import url

from .views import UserInfoView, UploadImageView, UpdatePwdView, SendEmailCodeView

urlpatterns = [
    # 用户信息
    url(r"^info/$", UserInfoView.as_view(), name='user_info'),

    # 用户头像上传
    url(r"^image/upload/$", UploadImageView.as_view(), name='image_upload'),

    # 用户个人中心修改密码
    url(r"^update/pwd/$", UpdatePwdView.as_view(), name='update_pwd'),

    # 向邮箱发送验证码
    url(r"^sendemail_code/$", SendEmailCodeView.as_view(), name='sendemail_code'),


]