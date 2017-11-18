# coding=utf-8

import xadmin

from .models import CityDict, CourseOrg, Teacher


class CityDictAdmin:
    list_display = ['name', 'desc', 'add_time']
    search_fields = ['name', 'desc']
    list_filter = ['name', 'desc', 'add_time']
    model_icon = 'fa fa-map-marker'


class CourseOrgAdmin:
    list_display = ['name', 'desc', 'click_nums', 'fav_nums', 'image', 'address', 'city', 'add_time']
    search_fields = ['name', 'desc', 'click_nums', 'fav_nums', 'image', 'address', 'city__name']
    list_filter = ['name', 'desc', 'click_nums', 'fav_nums', 'image', 'address', 'city__name', 'add_time']
    model_icon = 'fa fa-sitemap'
    # 这里的意思是如果有一个外键指向CourseOrg，比如说Course中有个，在后台管理系统中，CourseOrg的选择列表
    # 变成ajax加载方式，这样就可以在别的地方用名字搜索
    relfield_style = 'fk-ajax'


class TeacherAdmin:
    list_display = ['org', 'name', 'work_years', 'work_company',
                    'work_position', 'points', 'click_nums', 'fav_nums', 'add_time']
    search_fields = ['org__name', 'name', 'work_years', 'work_company',
                     'work_position', 'points', 'click_nums', 'fav_nums']
    list_filter = ['org__name', 'name', 'work_years', 'work_company',
                   'work_position', 'points', 'click_nums', 'fav_nums', 'add_time']
    model_icon = 'fa fa-user-o'


xadmin.site.register(CourseOrg, CourseOrgAdmin)
xadmin.site.register(CityDict, CityDictAdmin)
xadmin.site.register(Teacher, TeacherAdmin)