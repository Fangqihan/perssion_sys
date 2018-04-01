from django.shortcuts import render, redirect, HttpResponse
from rbac.models import UserInfo

import re

from rbac.session_service.init_permission import init_permission
# from rbac.templatetags.rbac import


def login(request):
    if request.method == 'GET':
        return render(request, 'login.html')

    else:
        username = request.POST.get('username', '')
        password = request.POST.get('password', '')
        user_obj = UserInfo.objects.filter(name=username, password=password)

        if not user_obj:
            return render(request, 'login.html', {'msg': '用户名或密码有误'})
        else:
            init_permission(request, user_obj)
            return redirect('/index/')


def index(request):


    return render(request, 'index.html')


def exchange(request):
    return HttpResponse('更换商品')


def return_goods(request):
    return render(request, 'index.html')


def add_goods(request):
    return HttpResponse('商品上架')


def del_goods(request):
    # from django.conf import settings
    # all_menu_list = request.session.get(settings.SESSION_ALL_MENU_KEY)
    # permission_menu_list = request.session.get(settings.SESSION_PERMISSION_MENU_LIST_KEY)
    # print('permission_menu_list', permission_menu_list)
    # # [{'title': '商品下架', 'url': '/del_goods/', 'menu_id': 14}]
    # # permission_url_list ['/del_goods/']
    #
    # # 对其结果进行处理,整合成特殊结构
    # all_menu_dict = {}
    # for item in all_menu_list:
    #     item['children_contents'] = []
    #     item['status'] = False  # 是否显示为当前菜单
    #     item['open'] = False  # 是否展开
    #
    #     # 先整理成字典格式
    #     all_menu_dict[item['id']] = item
    #
    # for item in permission_menu_list:
    #     item['status'] = True
    #     # 匹配出当前访问的url对用的菜单,并展开
    #     if re.match(item['url'], request.path):
    #         item['open'] = True
    #     else:
    #         item['open'] = False
    #     # 1, 加授权标签到菜单中
    #     all_menu_dict[item['menu_id']]["children_contents"].append(item)
    #     # 2, 修改菜单的status
    #     all_menu_dict[item['menu_id']]['status'] = True
    #     # 3, 修改所有父菜单的status
    #     pid = all_menu_dict[item['menu_id']]['parent_id']  # pid = 6
    #     while pid:
    #         all_menu_dict[pid]['status'] = True
    #         # 4, (非常关键)因为要不知道有几层菜单标签,  在之前的基础上将父菜单的parent_id作为判断对象,若其不存在,则退出循环
    #         pid = all_menu_dict[pid]['parent_id']
    #
    #         # 方法同上,不断更新pid
    #
    #     # 方法同上,不断更新pid
    #     if item['open']:
    #         pid = item['menu_id']  # pid=14
    #         while pid:
    #             all_menu_dict[pid]['open'] = True
    #             pid = all_menu_dict[pid]['parent_id']  # pid = 6
    #
    # print('all_menu_dict', all_menu_dict)

    return render(request, 'index.html')

