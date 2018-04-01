# -*- coding: utf-8 -*-   @Time    : 18-1-25 下午6:58
# @Author  : QiHanFang    @Email   : qihanfang@foxmail.com
import re

from django.utils.deprecation import MiddlewareMixin
from django.shortcuts import HttpResponse, redirect

from django.conf import settings


class Md1(MiddlewareMixin):
    def process_request(self, request):

        # 排除无需授权的url
        for url in settings.AUTHORIZED_URLS:
            match_url =  re.match(url, request.path)
            if match_url:
                return None

        # 取出当前用户的所有有权限访问的url
        permission_url_list = request.session.get(settings.SESSION_PERMISSION_URL_LIST_KEY, '')
        print('permission_url_list', permission_url_list)

        # 此处易发生循环重定向，因为下一次发送请求还要经过这里，此时这里还是没有任何信息，会定向到登录的url;
        if not permission_url_list:
            return redirect(settings.LOGIN_URL)

        #  有权限
        flag = False
        # permission_urls = ['/return_goods/', '/admin/']
        for db_url in permission_url_list:
            # 注意必须完全匹配,因为权限的url是正则表达式的形式;
            # match_ulr = re.match(settings.URL_PATTERN.format(db_url), request.path)
            match_ulr = re.match(settings.URL_PATTERN.format(db_url), request.path)
            if match_ulr:
                flag = True
                break

        if not flag:
            if settings.DEBUG:
                url_html = '</br>'.join(permission_url_list)
                return HttpResponse('无权访问: %s' % url_html)
            else:
                return HttpResponse('<h1>无权访问</h1>')
