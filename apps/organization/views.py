import json

from django.shortcuts import render

# Create your views here.
from django.views.generic import View
from django.http import HttpResponse
from pure_pagination import Paginator, EmptyPage, PageNotAnInteger

from .models import CourseOrg, CityDict
from .forms import UserAskForm


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
