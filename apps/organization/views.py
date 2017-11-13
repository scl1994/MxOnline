import json

from django.shortcuts import render

# Create your views here.
from django.views.generic import View
from django.http import HttpResponse
from pure_pagination import Paginator, EmptyPage, PageNotAnInteger

from .models import CourseOrg, CityDict, Teacher
from .forms import UserAskForm
from courses.models import Course
from operation.models import UserFavorite


class OrgView(View):
    """
        课程机构列表功能。
    """

    def get(self, request):
        all_orgs = CourseOrg.objects.all()
        # 根据点击数排名，取前三个
        hot_orgs = all_orgs.order_by('click_nums')[:3]
        all_cities = CityDict.objects.all()

        # 类别筛选
        category = request.GET.get('ct', '')
        if category is not '':
            all_orgs = all_orgs.filter(category=category)

        # 取出筛选城市(如果url中带有city参数，说明要根据city进一步筛选)
        city_id = request.GET.get('city', '')
        if city_id is not '':
            all_orgs = all_orgs.filter(city_id=int(city_id))

        sort = request.GET.get('sort', '')
        if sort is not "":
            if sort == 'students':
                all_orgs = all_orgs.order_by('students')
            elif sort == 'courses':
                all_orgs = all_orgs.order_by('course_nums')

        # 数量统计要在筛选之后
        org_nums = all_orgs.count()

        # 对课程机构进行分页
        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1

        # 每页五个
        p = Paginator(all_orgs, 5, request=request)

        orgs = p.page(page)

        return render(request, "org-list.html", {
            "all_orgs": orgs,
            "all_cities": all_cities,
            "org_nums": org_nums,
            "city_id": city_id,
            "category": category,
            'hot_orgs': hot_orgs,
            'sort': sort
        })


class AddUserAskView(View):
    """
        用户添加咨询
    """
    def post(self, request):
        userask_form = UserAskForm(request.POST)
        if userask_form.is_valid():
            # 这里可以直接通过modelform提交到数据库，非常方便，
            user_ask = userask_form.save(commit=True)
            # 注意这里是一个ajax请求，返回json，不用返回页面
            # 注意第一个参数要是json格式，需要将字典转化为json
            return HttpResponse(json.dumps({'status': 'success'}), content_type='application/json')
        else:
            return HttpResponse(json.dumps({'status': 'fail', 'msg': '添加出错'}),
                                content_type='application/json')


class OrgHomeView(View):
    """机构首页"""
    def get(self, request, org_id):
        # 用于前端页面判断当前应该凸显那个标签
        current_page = 'home'
        course_org = CourseOrg.objects.get(id=int(org_id))
        # 用于判断用户是否收藏了机构，在页面上显示
        has_fav = False
        if request.user.is_authenticated():
            if UserFavorite.objects.filter(user=request.user,
                                                    fav_id=int(course_org.id), fav_type=2):
                has_fav = True
        # Course中有个外键指向CourseOrg叫course_org，
        # 在CourseOrg中自动生成一个course_set(类名小写加上_set)反向指向Course
        all_courses = course_org.course_set.all()[:3]
        all_teachers = course_org.teacher_set.all()[:1]
        return render(request, 'org-detail-homepage.html', {
            'all_courses': all_courses,
            'all_teachers': all_teachers,
            'course_org': course_org,
            'current_page': current_page,
            'has_fav': has_fav
        })


class OrgCourseView(View):
    """机构课程列表页"""
    def get(self, request, org_id):
        current_page = 'course'
        course_org = CourseOrg.objects.get(id=int(org_id))
        all_courses = course_org.course_set.all()
        has_fav = False
        if request.user.is_authenticated():
            if UserFavorite.objects.filter(user=request.user,
                                           fav_id=int(course_org.id), fav_type=2):
                has_fav = True
        return render(request, 'org-detail-course.html', {
            'all_courses': all_courses,
            'course_org': course_org,
            'current_page': current_page,
            'has_fav': has_fav
        })


class OrgDescView(View):
    """机构介绍页"""
    def get(self, request, org_id):
        current_page = 'desc'
        course_org = CourseOrg.objects.get(id=int(org_id))
        has_fav = False
        if request.user.is_authenticated():
            if UserFavorite.objects.filter(user=request.user,
                                           fav_id=int(course_org.id), fav_type=2):
                has_fav = True
        return render(request, 'org-detail-desc.html', {
            'course_org': course_org,
            'current_page': current_page,
            'has_fav': has_fav
        })


class OrgTeacherView(View):
    """机构教师列表页"""
    def get(self, request, org_id):
        current_page = 'teacher'
        course_org = CourseOrg.objects.get(id=int(org_id))
        all_teachers = course_org.teacher_set.all()
        has_fav = False
        if request.user.is_authenticated():
            if UserFavorite.objects.filter(user=request.user,
                                           fav_id=int(course_org.id), fav_type=2):
                has_fav = True
        return render(request, 'org-detail-teachers.html', {
            'all_teachers': all_teachers,
            'course_org': course_org,
            'current_page': current_page,
            'has_fav': has_fav
        })


class AddFavView(View):
    """用户收藏"""
    def post(self, request):
        fav_id = request.POST.get('fav_id', 0)   # 为防止int转换时异常，将默认值设为0
        fav_type = request.POST.get('fav_type', '')

        # 这个视图函数不仅可以添加收藏，还要能取消收藏（如果你已经收藏，再次提交表示取消）
        # 所以在此之前必须要验证用户是否登录（不然不知道谁收藏了）
        # 没登录，返回json，同时ajax应该跳转到登录页面
        if not request.user.is_authenticated():
            return HttpResponse(json.dumps({'status': 'fail', 'msg': '用户未登录'}),
                                content_type='application/json')
        # 在数据库中某user中，用fav_id、fav_type作联合查询，确定是否已经收藏
        exist_records = UserFavorite.objects.filter(user=request.user,
                                                    fav_id=int(fav_id), fav_type=int(fav_type))
        if exist_records:
            # 如果已经存在记录，表示要取消收藏，删除记录
            exist_records.delete()
            return HttpResponse(json.dumps({'status': 'success', 'msg': '收藏'}),
                                content_type='application/json')
        else:
            user_fav = UserFavorite()
            if int(fav_id) > 0 and int(fav_type) > 0:
                user_fav.user = request.user
                user_fav.fav_id = int(fav_id)
                user_fav.fav_type = int(fav_type)
                user_fav.save()
                return HttpResponse(json.dumps({'status': 'success', 'msg': '已收藏'}),
                                    content_type='application/json')
            else:
                return HttpResponse(json.dumps({'status': 'fail', 'msg': '收藏失败'}),
                                    content_type='application/json')


class TeacherListView(View):
    """课程讲师列表页"""
    def get(self, request):
        all_teachers = Teacher.objects.all()

        # 排序功能
        sort = request.GET.get('sort', '')
        if sort is not "":
            if sort == 'hot':
                all_teachers = all_teachers.order_by('-click_nums')

        # 讲师排行榜
        sorted_teacher = Teacher.objects.all().order_by('-click_nums')[:3]

        # 对讲师进行分页
        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1

        # 每页五个
        p = Paginator(all_teachers, 1, request=request)

        teachers = p.page(page)

        return render(request, 'teachers-list.html', {
            'all_teachers': teachers,
            'sorted_teacher': sorted_teacher,
            "sort": sort,
        })
