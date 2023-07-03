import json

from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from first_app import models
from djangoProject import result


# Create your views here.

def hello(request):
    return HttpResponse("Hello World")


def login(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        admin_name = data.get('admin_name', '')
        admin_password = data.get('admin_password', '')
        if admin_name == '' or admin_password == '':
            return result.Result.data_null('数据不能为空')
        if models.Admin.objects.filter(admin_name=admin_name, admin_password=admin_password).exists():
            return result.Result.success('登陆成功', data)
        return result.Result.success('用户不存在或密码错误，请重新输入', data)
