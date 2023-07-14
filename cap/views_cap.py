import json

from django.db.models import Q
from django.http import JsonResponse
from django.shortcuts import render
from rest_framework.decorators import api_view

from cap import models
from cap.models import Cap
from djangoProject import result


# Create your views here.

@api_view(['POST'])
def add(request):
    last_cap = models.Cap.objects.last()
    if last_cap is None:
        last_cap = 0
    else:
        last_cap = str(int(last_cap.id)+1)
    data = json.loads(request.body)
    data['id'] = last_cap
    cap = Cap(**data)
    if cap == '':
        return result.Result.data_null('数据不能为空')
    models.Cap.objects.create(**data)
    return result.Result.success(data)


@api_view(['DELETE'])
def delete(request, id):
    cap = models.Cap.objects.get(id=id)
    if cap == '':
        return result.Result.notfound('没有该事件')
    try:
        cap.delete()
        return result.Result.success(id)
    except cap.DoesNotExist:
        return result.Result.error('删除失败')


@api_view(['PUT'])
def update(request):
    data = json.loads(request.body)
    id = data['id']
    if models.Cap.objects.filter(id=id).exists():
        models.Cap.objects.filter(id=id).update(**data)
        response_data = {'msg': '摄像头信息修改成功'}
        return JsonResponse(response_data)
    else:
        return result.Result.notfound("修改的数据不存在")


@api_view(['GET'])
def selectAll(request):
    data_list = []
    try:
        data = models.Cap.objects.filter()
        for item in data:
            data_dict = {key: value for key, value in item.__dict__.items() if key != '_state'}
            data_list.append(data_dict)
        return result.Result.success(data_list)
    except:
        return result.Result.error("获取失败")


@api_view(['GET'])
def select(request, parameter):
    try:
        data = models.Cap.objects.get(Q(id=parameter) | Q(name=parameter))
        data_dict = {key: value for key, value in data.__dict__.items() if key != '_state'}
        return result.Result.success(data_dict)
    except:
        return result.Result.notfound("查询失败")

