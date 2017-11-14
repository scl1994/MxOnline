import json

from django.shortcuts import render
from django.views.generic import View
from django.http import HttpResponse
from django.db.models import Q
from pure_pagination import Paginator, EmptyPage, PageNotAnInteger

from .models import Course, CourseResource, Video
from operation.models import UserFavorite, CourseComments, UserCourse
from django.contrib.auth.mixins import LoginRequiredMixin  # 用来为视图函数检测是否登录


# Create your views here.


class CourseListView(View):
    def get(self, request):
        all_courses = Course.objects.all().order_by('-add_time')

        hot_courses = Course.objects.all().order_by('-click_nums')[:3]

        # 实现页面顶部的课程搜索功能
        search_keywords = request.GET.get('keywords', '')
        if search_keywords:
            # 在name或desc或detail（使用Q实现或操作）中不区分大小写（i）搜索包含search_keywords的记录
            all_courses = all_courses.filter(Q(name__icontains=search_keywords) | Q(desc__icontains=search_keywords)
                                             | Q(detail__icontains=search_keywords))

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


class CourseInfoView(LoginRequiredMixin, View):
    """课程章节信息"""

    def get(self, request, course_id):
        course = Course.objects.get(id=int(course_id))

        # 查询用户是否已经关联了该课程
        if_courses = UserCourse.objects.filter(user=request.user, course=course)
        if not if_courses:
            # 没有关联，创建关联,课程的学习人数加一
            course.students += 1
            course.save()
            u = UserCourse(user=request.user, course=course)
            u.save()

        # 取出所有学过该课程的用户，查询他们的id，找到他们还学习了那些课程
        user_courses = UserCourse.objects.filter(course=course)
        user_ids = [user_course.user.id for user_course in user_courses]
        # 这里user_id表示外键的id，后面的__in表示传进来的时个列表
        all_user_courses = UserCourse.objects.filter(user_id__in=user_ids)
        # 取出所有课程的id
        course_ids = [i.course.id for i in all_user_courses]
        relative_courses = Course.objects.filter(id__in=course_ids).order_by('-click_nums')[:5]

        all_resources = CourseResource.objects.filter(course=course)
        return render(request, 'course-video.html', {
            'course': course,
            'course_resources': all_resources,
            'relative_courses': relative_courses
        })


class CommentsView(LoginRequiredMixin, View):
    # 跳转到评论页面
    def get(self, request, course_id):
        course = Course.objects.get(id=int(course_id))
        all_comments = CourseComments.objects.filter(course=course)
        all_resources = CourseResource.objects.filter(course=course)

        user_courses = UserCourse.objects.filter(course=course)
        user_ids = [user_course.user.id for user_course in user_courses]
        # 这里user_id表示外键的id，后面的__in表示传进来的时个列表
        all_user_courses = UserCourse.objects.filter(user_id__in=user_ids)
        # 取出所有课程的id
        course_ids = [i.course.id for i in all_user_courses]
        relative_courses = Course.objects.filter(id__in=course_ids).order_by('-click_nums')[:5]

        return render(request, 'course-comment.html', {
            'course': course,
            'all_comments': all_comments,
            'course_resources': all_resources,
            'relative_courses': relative_courses
        })


class AddCommentsView(View):
    # 用户用ajax添加评论
    def post(self, request):
        if not request.user.is_authenticated():
            return HttpResponse(json.dumps({'status': 'fail', 'msg': '用户未登录'}),
                                content_type='application/json')

        course_id = request.POST.get('course_id', 0)
        comments = request.POST.get('comments', '')
        if int(course_id) > 0 and comments:
            course_comments = CourseComments()
            # 注意在CourseComments中course是个外键，所以在给他传值时要传Course对象
            course = Course.objects.get(id=int(course_id))
            course_comments.course = course
            course_comments.comments = comments
            course_comments.user = request.user
            course_comments.save()
            return HttpResponse(json.dumps({'status': 'success', 'msg': '添加成功'}),
                                content_type='application/json')
        else:
            return HttpResponse(json.dumps({'status': 'fail', 'msg': '添加失败'}),
                                content_type='application/json')


class VideoPlayView(View):
    """视频播放页面"""

    def get(self, request, video_id):
        video = Video.objects.get(id=int(video_id))
        course = video.lesson.course
        # 查询用户是否已经关联了该课程
        if_courses = UserCourse.objects.filter(user=request.user, course=course)
        if not if_courses:
            # 没有关联，创建关联
            course.students += 1
            course.save()
            u = UserCourse(user=request.user, course=course)
            u.save()

        # 取出所有学过该课程的用户，查询他们的id，找到他们还学习了那些课程
        user_courses = UserCourse.objects.filter(course=course)
        user_ids = [user_course.user.id for user_course in user_courses]
        # 这里user_id表示外键的id，后面的__in表示传进来的时个列表
        all_user_courses = UserCourse.objects.filter(user_id__in=user_ids)
        # 取出所有课程的id
        course_ids = [i.course.id for i in all_user_courses]
        relative_courses = Course.objects.filter(id__in=course_ids).order_by('-click_nums')[:5]

        all_resources = CourseResource.objects.filter(course=course)
        return render(request, 'course-play.html', {
            'course': course,
            'course_resources': all_resources,
            'relative_courses': relative_courses,
            'video': video
        })
