# coding=utf-8

import xadmin
from xadmin import views as xadmin_views

from .models import EmailVerifyRecord, Banner


# 修改后台可更改主题
class BaseSetting:
    enable_themes = True
    use_bootswatch = True


class GlobalSetting:
    # 修改页头页尾
    site_title = "后台在线管理"
    site_footer = "MxOnline By Scl1994"
    # 将左侧导航设为可折叠
    menu_style = "accordion"


class EmailVerifyRecordAdmin:
    list_display = ['code', 'email', 'send_type', 'send_time']
    search_fields = ['code', 'email', 'send_type']
    list_filter = ['code', 'email', 'send_type', 'send_time']


class BannerAdmin:
    list_display = ['title', 'image', 'url', 'index', 'add_time']
    search_fields = ['title', 'image', 'url', 'index']
    list_filter = ['title', 'image', 'url', 'index', 'add_time']


xadmin.site.register(EmailVerifyRecord, EmailVerifyRecordAdmin)
xadmin.site.register(Banner, BannerAdmin)
xadmin.site.register(xadmin_views.BaseAdminView, BaseSetting)
xadmin.site.register(xadmin_views.CommAdminView, GlobalSetting)