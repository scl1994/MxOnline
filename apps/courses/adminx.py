from .models import Course, Lesson, Video, CourseResource
import xadmin


class CourseAdmin:
    list_display = ['name', 'desc', 'detail', 'degree',
                    'learn_times', 'students', 'fav_nums', 'image', 'click_nums', 'add_time']
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
xadmin.site.register(Lesson, LessonAdmin)
xadmin.site.register(Video, VideoAdmin)
xadmin.site.register(CourseResource, CourseResourceAdmin)