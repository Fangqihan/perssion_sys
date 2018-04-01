# -*- coding: utf-8 -*-   @Time    : 18-1-25 下午6:58
# @Author  : QiHanFang    @Email   : qihanfang@foxmail.com

from ..models import Menu

def init_permission(request, user_obj):
    permission_items = user_obj.values('role__permissions__url', 'role__permissions__title',
                                       'role__permissions__menu_id').distinct()

    # 2, 仅包含当前用户有全访问的url列表
    permission_url_list = []
    # 3， 仅包含当前用户有权限的菜单和权限名称信息
    permission_menu_list = []

    # 4,取出所有菜单, 注意必须转换成列表类型，否则在存入session时无法序列化
    all_menus = list(Menu.objects.values('id', 'caption', 'parent_id'))

    for item in permission_items:
        permission_url_list.append(item['role__permissions__url'])
        if item['role__permissions__menu_id']:
            temp = {'title': item['role__permissions__title'], 'url': item['role__permissions__url'],
                    'menu_id': item['role__permissions__menu_id']}
            permission_menu_list.append(temp)

    from django.conf import settings
    request.session[settings.SESSION_PERMISSION_URL_LIST_KEY] = permission_url_list
    request.session[settings.SESSION_PERMISSION_MENU_LIST_KEY] = permission_menu_list
    request.session[settings.SESSION_ALL_MENU_KEY] = all_menus