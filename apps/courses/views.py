from django.shortcuts import render
from django.views.generic import View
from pure_pagination import Paginator, EmptyPage, PageNotAnInteger

from .models import Course
from operation.models import UserFavorite


# Create your views here.


class CourseListView(View):
    def get(self, request):
        all_courses = Course.objects.all().order_by('-add_time')

        hot_courses = Course.objects.all().order_by('-click_nums')[:3]

        # 课程排序
        sort = request.GET.get('sort', '')
        if sort is not "":
            if sort == 'students':
                all_courses = all_courses.order_by('-students')
            elif sort == 'hot':
                all_courses = all_courses.order_by('-click_nums')

        # 对课程进行分页
        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1

        # 每页五个
        p = Paginator(all_courses, 6, request=request)

        courses = p.page(page)

        return render(request, 'course-list.html', {
            'all_courses': courses,
            'hot_courses': hot_courses,
            'sort': sort
        })


class CourseDetailView(View):
    """课程详情页"""
    def get(self, request, course_id):
        course = Course.objects.get(id=int(course_id))

        # 每请求一次（点击一次），点击数加一
        course.click_nums += 1
        course.save()

        # 判断用户是否收藏了机构或课程
        has_fav_course = False
        has_fav_org = False

        if request.user.is_authenticated():
            if UserFavorite.objects.filter(user=request.user, fav_id=course.id, fav_type=1):
                has_fav_course = True
            if UserFavorite.objects.filter(user=request.user, fav_id=course.course_org.id, fav_type=2):
                has_fav_org = True

        # 根据课程标签推荐相同类型课程
        tag = course.tag
        if tag:
            relative_courses = Course.objects.filter(tag=tag)[:1]
        else:
            # tag为空时，返回一个数组，应为要在html中for循环，防止出错
            relative_courses = []
        return render(request, 'course-detail.html', {
            'course': course,
            'relative_courses': relative_courses,
            'has_fav_course': has_fav_course,
            'has_fav_org': has_fav_org
        })
