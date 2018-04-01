from django.shortcuts import render
from .models import *


def login(request):
    if request.method == 'GET':
        return render(request, 'login.html')

    else:
        username = request.POST.get('username', '')
        password = request.POST.get('password', '')
        user_obj = UserInfo.objects.filter(username=username, password=password)
        if user_obj:
            user_obj = user_obj.first()
            # 取出改用的所有权限




        else:
            return render(request, 'login.html', {'msg': '用户名或密码有误'})