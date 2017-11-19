from .models import Course, Lesson, Video, CourseResource, BannerCourse
from organization.models import CourseOrg
import xadmin


class LessonInline:
    # 课程和章节相关，通过添加这个class，可以在添加新课程的页面同时添加他的章节
    model = Lesson
    extra = 0


class CourseResourceInline:
    # 添加课程时可以顺便添加课程的资源文件
    model = CourseResource
    extra = 0


class CourseAdmin:
    list_display = ['name', 'desc', 'detail', 'degree',
                    'learn_times', 'students', 'fav_nums', 'image', 'click_nums', 'add_time', 'get_zj_nums', 'go_to']
    search_fields = ['name', 'desc', 'detail', 'degree', 'learn_times', 'students', 'fav_nums', 'image', 'click_nums']
    list_filter = ['name', 'desc', 'detail', 'degree',
                   'learn_times', 'students', 'fav_nums', 'image', 'click_nums', 'add_time']
    model_icon = 'fa fa-book'
    # 设置默认排序方式，这里用的时click_nums倒序
    ordering = ['-click_nums']
    # 设置字段在后台管理系统中变成只读，不可以修改
    readonly_fields = ['click_nums', 'fav_nums']
    # 设置字段不显示，隐藏，注意如果字段设置了只读显示，再将他设置为隐藏将不会生效，这里设置为image
    # exclude = ['image']

    # 外键指向这时，通过ajax动态加载数据
    relfield_style = 'fk-ajax'

    # 可以在添加新课程的页面同时添加他的章节， 注意LessonInline要定义在CourseAdmin之前，不然报错
    inlines = [LessonInline, CourseResourceInline]

    # 在xadmin中集成djangoUeditor时用到
    style_fields = {"detail": 'ueditor'}

    # 设置页面刷新间隔时间设置为每30秒或者每60秒
    refresh_times = [30, 60, 90]

    def queryset(self):
        # 只显示非轮播课程
        qs = super(CourseAdmin, self).queryset()
        qs = qs.filter(is_banner=False)
        return qs

    def save_models(self):
        # 在保存课程的时候统计课程机构的课程数
        obj = self.new_obj
        obj.save()
        if obj.course_org is not None:
            course_org = obj.course_org
            course_org.course_nums = Course.objects.filter(course_org=course_org).count()
            course_org.save()


class BannerCourseAdmin:
    #   这个admin只显示轮播课程，要重载queryset方法
    list_display = ['name', 'desc', 'detail', 'degree',
                    'learn_times', 'students', 'fav_nums', 'image', 'click_nums', 'add_time', 'get_zj_nums', 'go_to']
    search_fields = ['name', 'desc', 'detail', 'degree', 'learn_times', 'students', 'fav_nums', 'image', 'click_nums']
    list_filter = ['name', 'desc', 'detail', 'degree',
                   'learn_times', 'students', 'fav_nums', 'image', 'click_nums', 'add_time']
    model_icon = 'fa fa-book'
    # 设置默认排序方式，这里用的时click_nums倒序
    ordering = ['-click_nums']
    # 设置字段在后台管理系统中变成只读，不可以修改
    readonly_fields = ['click_nums', 'fav_nums']
    # 设置字段不显示，隐藏，注意如果字段设置了只读显示，再将他设置为隐藏将不会生效，这里设置为image
    # exclude = ['image']

    # 外键指向这时，通过ajax动态加载数据
    relfield_style = 'fk-ajax'

    # 可以在添加新课程的页面同时添加他的章节， 注意LessonInline要定义在CourseAdmin之前，不然报错
    inlines = [LessonInline, CourseResourceInline]

    def queryset(self):
        # 同筛选的课程在用is_banner筛选一次
        qs = super(BannerCourseAdmin, self).queryset()
        qs = qs.filter(is_banner=True)
        return qs


class LessonAdmin:
    # 一定要注意，search_fields和list_filter中外键要指明外键的那个字段__xx
    list_display = ['course', 'name', 'add_time']
    search_fields = ['course__name', 'name']
    # course为外键，在过滤时要指定要使用的字段，如搜索name字段，就是course__name，即通过课程的名字来区分章节
    list_filter = ['course__name', 'name', 'add_time']
    model_icon = 'fa fa-pencil-square-o'
    relfield_style = 'fk-ajax'


class VideoAdmin:
    list_display = ['lesson', 'name', 'add_time']
    search_fields = ['lesson__name', 'name']
    list_filter = ['lesson__name', 'name', 'add_time']
    model_icon = 'fa fa-file-video-o'


class CourseResourceAdmin:
    list_display = ['course', 'name', 'download', 'add_time']
    search_fields = ['course__name', 'name', 'download']
    list_filter = ['course__name', 'name', 'download', 'add_time']
    model_icon = 'fa fa-file-text-o'


xadmin.site.register(Course, CourseAdmin)
xadmin.site.register(BannerCourse, BannerCourseAdmin)
xadmin.site.register(Lesson, LessonAdmin)
xadmin.site.register(Video, VideoAdmin)
xadmin.site.register(CourseResource, CourseResourceAdmin)