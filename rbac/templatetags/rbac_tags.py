# -*- coding: utf-8 -*-   @Time    : 18-1-25 下午6:58
# @Author  : QiHanFang    @Email   : qihanfang@foxmail.com
from django import template
import re
from django.conf import settings
from django.utils import safestring
register = template.Library()


def process_menu_data(request):
    """数据库取到要展示的菜单的所有信息"""
    all_menu_list = request.session.get(settings.SESSION_ALL_MENU_KEY)
    permission_menu_list = request.session.get(settings.SESSION_PERMISSION_MENU_LIST_KEY)
    print('permission_menu_list', permission_menu_list)

    all_menu_dict = {}
    for item in all_menu_list:
        item['children_contents'] = []
        item['status'] = False  # 是否显示为当前菜单
        item['open'] = False  # 是否展开

        # 先整理成字典格式
        all_menu_dict[item['id']] = item

    for item in permission_menu_list:
        item['status'] = True
        # 匹配出当前访问的url对用的菜单,并展开
        if re.match(item['url'], request.path):
            item['open'] = True
        else:
            item['open'] = False
        # 1, 加授权标签到菜单中
        all_menu_dict[item['menu_id']]["children_contents"].append(item)

        # 2, 修改菜单的status
        all_menu_dict[item['menu_id']]['status'] = True

        # 3, 修改所有父菜单的status
        pid = all_menu_dict[item['menu_id']]['parent_id']  # pid = 6
        while pid:
            all_menu_dict[pid]['status'] = True
            # 4, (非常关键)因为要不知道有几层菜单标签,  在之前的基础上将父菜单的parent_id作为判断对象,若其不存在,则退出循环
            pid = all_menu_dict[pid]['parent_id']

            # 方法同上,不断更新pid

        # 方法同上,不断更新pid
        if item['open']:
            pid = item['menu_id']  # pid=14
            while pid:
                all_menu_dict[pid]['open'] = True
                pid = all_menu_dict[pid]['parent_id']  # pid = 6
        # 最后一步处理,取出所有的根菜单,并将子菜单放进根菜单中

    for k in all_menu_dict:
        pid = all_menu_dict[k]['parent_id']
        if pid:
            all_menu_dict[pid]['children_contents'].append(all_menu_dict[k])

    ret = []
    for k, v in all_menu_dict.items():
        if not v['parent_id']:
            ret.append(v)
    print('ret', ret)
    return ret


def produce_html(all_menu_dict):
    html = ''

    # 菜单
    tpl1 = """
        <div class="rbac-menu-item">
        <div class="rbac-menu-header">{0}</div>
        <div class="rbac-menu-body {2}">{1}</div>
    </div>
    """
    # 权限
    tpl2 = '''<a href="{0}" class="{1}">{2}</a>'''

    # 判断status,只有当其为True的时候才显示, 不好理解
    for item in all_menu_dict:
        # (重要)当前菜单的status为False, 直接跳过,进行下一次循环
        if not item['status']:
            continue
        if item.get('url'):
            # 权限
            html += tpl2.format(item['url'], "rbac-active" if item['open'] else '', item['title'])
        else:
            # 菜单
            # 子菜单放在{1}处, 第二次参数: 将子菜单内容放入(权限或者菜单)
            if item['children_contents']:
                html += tpl1.format(item['caption'], produce_html(item['children_contents']), "" if item['open'] else 'rbac-hide')

            print('html', html)

    return html


@register.simple_tag
def rbac_menu(request):
    # 1. 先去数据库取到菜单相关的数据
    data = process_menu_data(request)

    # 2. 生成html, 注意转换成可以渲染的html
    html = safestring.mark_safe(produce_html(data))
    return html

import os

@register.simple_tag
def rbac_css():
    file_path = os.path.join('rbac', 'theme', 'rbac.css')
    if os.path.exists(file_path):
        return safestring.mark_safe(open(file_path, 'r', encoding='utf-8').read())
    else:
        raise Exception('rbac主题CSS文件不存在')


@register.simple_tag
def rbac_js():
    file_path = os.path.join('rbac', 'theme', 'rbac.js')
    if os.path.exists(file_path):
        return safestring.mark_safe(open(file_path, 'r', encoding='utf-8').read())
    else:
        raise Exception('rbac主题JavaScript文件不存在')









