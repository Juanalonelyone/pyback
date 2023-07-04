import json

from django.db.models import Q
from django.shortcuts import render
from rest_framework.decorators import api_view


from djangoProject import result
from worker import models
from worker.models import Worker


# Create your views here.
# 增加工作人员信息
@api_view(['POST'])
def add(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        new_worker = Worker(**data)
        if new_worker.id == '':
            return result.Result.data_null('数据不能为空')
        if models.Worker.objects.filter(id=new_worker.id).exists():
            return result.Result.is_exist('用户id已存在')
        models.Worker.objects.create(**data)
        return result.Result.success(data)


# 删除工作人员信息
@api_view(['DELETE'])
def delete(request, id):
    delete_worker = models.Worker.objects.get(id=id)
    if delete_worker == '':
        return result.Result.notfound('工作人员不存在')
    try:
        delete_worker.delete()
        return result.Result.success(id)
    except delete_worker.DoesNotExist:
        return result.Result.error('删除失败')


# 更新工作人员信息
@api_view(['PUT'])
def update(request):
    data = json.loads(request.body)
    update_worker = Worker(**data)
    if models.Worker.objects.filter(id=update_worker.id).exists():
        try:
            models.Worker.objects.filter(id=update_worker.id).update(**data)
            return result.Result.success(update_worker.id)
        except update_worker.DoesNotExist:
            return result.Result.error('更新失败')
    return result.Result.notfound('未找到更新对象')


# 查询所有工作人员
@api_view(['GET'])
def select(request):
    data_list = []
    try:
        data = models.Worker.objects.filter()
        for item in data:
            data_dict = {key: value for key, value in item.__dict__.items() if key != '_state'}
            data_list.append(data_dict)
        return result.Result.success(data_list)
    except:
        return result.Result.error('获取失败')


# 根据条件查询
@api_view(['GET'])
def select_worker(request, parameter):
    try:
        data = models.Worker.objects.get(Q(id=parameter) | Q(workername=parameter))
        data_dict = {key: value for key, value in data.__dict__.items() if key != '_state'}
        return result.Result.success(data_dict)
    except:
        return result.Result.notfound('查询失败')
