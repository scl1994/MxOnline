from django.conf.urls import url

from .views import UserInfoView, UploadImageView

urlpatterns = [
    # 用户信息
    url(r"^info/$", UserInfoView.as_view(), name='user_info'),

    # 用户头像上传
    url(r"^image/upload/$", UploadImageView.as_view(), name='image_upload'),
]