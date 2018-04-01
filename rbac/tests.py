
permission_list = [
    {'title': '商品下架', 'url': '/del_goods/', 'menu_id': 14}
]
# 先列出所有的菜单,在将当前登录的用户有权限的url根据其munu_id放入其中;
menu_dict = {
    3: {'id': 3, 'caption': '其他', 'parent_id': None, 'children_contents': [], 'status': False, 'open': False},
    6: {'id': 6, 'caption': '卖家管理', 'parent_id': None, 'children_contents': [], 'status': False, 'open': False},
    8: {'id': 8, 'caption': '消费者管理', 'parent_id': None, 'children_contents': [], 'status': False, 'open': False},
    11: {'id': 11, 'caption': '退货', 'parent_id': 8, 'children_contents': [], 'status': False, 'open': False},
    14: {'id': 14, 'caption': '商品下架', 'parent_id': 6, 'children_contents': [
	    {'title': '商品下架', 'url': '/del_goods/', 'menu_id': 14}], 'status': False, 'open': False},
    15: {'id': 15, 'caption': '后台管理', 'parent_id': 3, 'children_contents': [], 'status': False, 'open': False}}

import re

current_url = '/del_goods/'
for item in permission_list:
    item['status'] = True  # 难点

    # 匹配出当前访问的url对应的的菜单,并展开
    if re.match(item['url'], current_url):
        item['open'] = True
    else:
        item['open'] = False

    # 1, 加授权标签到菜单中
    menu_dict[item['menu_id']]["children_contents"].append(item)
    # 2, 修改菜单的status
    menu_dict[item['menu_id']]['status'] = True
    # 3, 修改所有父菜单的status
    pid = menu_dict[item['menu_id']]['parent_id']  # pid = 6
    while pid:
        menu_dict[pid]['status'] = True
        # 4, (非常关键)因为要不知道有几层菜单标签,  在之前的基础上将父菜单的parent_id作为判断对象,若其不存在,则退出循环
        pid = menu_dict[pid]['parent_id']

    # 方法同上,不断更新pid
    if item['open']:
        pid = item['menu_id']  # pid=14
        while pid:
            menu_dict[pid]['open'] = True
            pid = menu_dict[pid]['parent_id']  # pid = 6
    """
     {3: {'id': 3, 'caption': '其他', 'parent_id': None, 'children_contents': [], 'status': False, 'open': False},
      6: {'id': 6, 'caption': '卖家管理', 'parent_id': None, 'children_contents': [], 'status': True, 'open': True},
      8: {'id': 8, 'caption': '消费者管理', 'parent_id': None, 'children_contents': [], 'status': False, 'open': False}, 
      11: {'id':11, 'caption': '退货', 'parent_id': 8, 'children_contents': [], 'status': False, 'open': False}, 
      14: {'id': 14, 'caption': '商品下架', 'parent_id': 6, 'children_contents': [
            {'title': '商品下架', 'url': '/del_goods/', 'menu_id': 14, 'status': True, 'open': True}], 'status': True, 'open': True}, 
      15: {'id': 15, 'caption': '后台管理', 'parent_id': 3, 'children_contents': [], 'status': False, 'open': False}}
    """

    all_menu_dict = {
      3: {'id': 3, 'caption': '其他', 'parent_id': None, 'children_contents': [], 'status': False, 'open': False},
      6: {'id': 6, 'caption': '卖家管理', 'parent_id': None, 'children_contents': [], 'status': True, 'open': True},
      8: {'id': 8, 'caption': '消费者管理', 'parent_id': None, 'children_contents': [], 'status': False, 'open': False}, 11: {'id':
      11, 'caption': '退货', 'parent_id': 8, 'children_contents': [], 'status': False, 'open': False},
      14: {'id': 14, 'caption': '商品下架', 'parent_id': 6, 'children_contents': [
            {'title': '商品下架', 'url': '/del_goods/', 'menu_id': 14, 'status': True, 'open': True}], 'status': True, 'open': True},
      15: {'id': 15, 'caption': '后台管理', 'parent_id': 3, 'children_contents': [], 'status': False, 'open': False}}

    # 最后一步处理,取出所有的根菜单,并将子菜单放进根菜单中

    for k in all_menu_dict:
        pid = all_menu_dict[k]['parent_id']
        if pid:
            all_menu_dict[pid]['children_contents'].append(all_menu_dict[k])

    ret = []
    for k, v in all_menu_dict.items():
        if not v['parent_id']:
            ret.append(v)


'''
[
{'id': 3, 'caption': '其他', 'parent_id': None, 'children_contents': [
    {'id': 15, 'caption': '后台管理', 'parent_id': 3, 'children_contents': [], 'status': False, 'open': False}], 'status': False, 'open': False}, 

{'id': 6, 'caption': '卖家管理', 'parent_id': None, 'children_contents': [
    {'id': 14, 'caption': '商品下架', 'parent_id': 6, 'children_contents': [
        {'title': '商品下架', 'url': '/del_goods/', 'menu_id': 14, 'status': True, 'open': False}], 'status': True, 'open': False}], 'status': True,'open': False}, 

{'id': 8, 'caption': '消费者管理', 'parent_id': None, 'children_contents': [
    {'id': 11, 'caption': '退货', 'parent_id': 8, 'children_contents': [], 'status': False, 'open': False}], 'status': False, 'open': False}]

'''




