# coding=utf-8
from datetime import datetime

from django.db import models

from organization.models import CourseOrg, Teacher

# Create your models here.


# 课程
class Course(models.Model):
    course_org = models.ForeignKey(CourseOrg, verbose_name="课程机构", null=True, blank=True)
    name = models.CharField(max_length=50, verbose_name=u"课程名")
    desc = models.CharField(max_length=300, verbose_name=u"课程描述")
    detail = models.TextField(verbose_name="课程详情")
    is_banner = models.BooleanField(default=False, verbose_name='是否轮播')
    teacher = models.ForeignKey(Teacher, verbose_name='讲师', null=True, blank=True)
    degree = models.CharField(verbose_name=u'难度', choices=(('cj', u'初级'), ('zj', u'中级'), ('gj', u"高级")), max_length=2)
    learn_times = models.IntegerField(default=0, verbose_name=u'学习时长（分钟数）')
    students = models.IntegerField(default=0, verbose_name=u"学习人数")
    fav_nums = models.IntegerField(default=0, verbose_name=u"收藏人数")
    image = models.ImageField(upload_to="courses/%Y/%m", verbose_name=u"封面", max_length=100)
    click_nums = models.IntegerField(default=0, verbose_name=u"点击数")
    category = models.CharField(default='后端开发', max_length=20, verbose_name=u"课程类别")
    tag = models.CharField(default='', verbose_name='课程标签', max_length=10)
    need_know = models.CharField(default='', verbose_name='课程须知', max_length=300)
    you_get = models.CharField(default='', verbose_name='课程收获', max_length=300)
    add_time = models.DateTimeField(default=datetime.now, verbose_name=u"添加时间")

    class Meta:
        verbose_name = u"课程"
        verbose_name_plural = verbose_name

    def get_zj_nums(self):
        # 通过外键查询课程有多少个章节
        return self.lesson_set.all().count()
    # 这样将章节数统计也可以加入xadmin后台显示
    get_zj_nums.short_description = "章节数"

    # 点击课程后跳转的页面
    def go_to(self):
        from django.utils.safestring import mark_safe
        return mark_safe("<a href='http://www.baidu.com'>跳转</a>")

    go_to.short_description = "跳转"

    def get_learn_users(self):
        # 获取学习用户
        return self.usercourse_set.all()[:5]

    def get_course_lesson(self):
        # 获取课程章节
        return self.lesson_set.all()

    def __str__(self):
        return self.name


class BannerCourse(Course):
    class Meta:
        verbose_name = '轮播课程'
        verbose_name_plural = verbose_name

        # 设这了这个参数，就不会生成一张新表， 这里设置这个bannercourse的目地只
        # 是为了在xadmin中注册一个新的表，在数据库中不必生成一个新表，用Course的就行
        proxy = True


# 课程章节信息，位于课程下
class Lesson(models.Model):
    course = models.ForeignKey(Course, verbose_name=u'课程')
    name = models.CharField(max_length=100, verbose_name=u"章节名")
    add_time = models.DateTimeField(default=datetime.now, verbose_name=u"添加时间")

    class Meta:
        verbose_name = u"章节"
        verbose_name_plural = verbose_name

    def __str__(self):
        #  名字要带上课程的名字
        return str(self.name) + '--' + str(self.course)

    def get_lesson_video(self):
        # 获取章节所有视频
        return self.video_set.all()


# 课程每个章节的视频，位于章节下
class Video(models.Model):
    lesson = models.ForeignKey(Lesson, verbose_name=u'章节')
    name = models.CharField(max_length=100, verbose_name=u"视频名")
    url = models.CharField(max_length=200, default='', verbose_name='访问地址')
    learn_times = models.IntegerField(default=0, verbose_name=u'学习时长（分钟数）')
    add_time = models.DateTimeField(default=datetime.now, verbose_name=u"添加时间")

    class Meta:
        verbose_name = u"视频"
        verbose_name_plural = verbose_name

    def __str__(self):
        return str(self.name) + '--' + str(self.lesson)


# 课程的文件资源，位于课程下
class CourseResource(models.Model):
    course = models.ForeignKey(Course, verbose_name=u'课程')
    name = models.CharField(max_length=100, verbose_name=u"名称")
    download = models.FileField(upload_to="course/resource/%Y/%m", verbose_name=u'资源文件', max_length=100)
    add_time = models.DateTimeField(default=datetime.now, verbose_name=u"添加时间")

    class Meta:
        verbose_name = u"课程资源"
        verbose_name_plural = verbose_name

    def __str__(self):
        return str(self.name) + '--' + str(self.course)
