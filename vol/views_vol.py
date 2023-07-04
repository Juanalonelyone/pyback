import json

from django.db.models import Q

from djangoProject import result
from vol import models
from vol.models import Vol
from rest_framework.decorators import api_view

#对护工的增删改查


#添加护工信息
@api_view(['POST'])
def add(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        vol = Vol(**data)
        print(vol)
        if vol.id == '':
            return result.Result.data_null('数据不能为空')
        if models.Vol.objects.filter(id=vol.id).exists():
            return result.Result.is_exist('护工id已存在')
        models.Vol.objects.create(**data)
        return result.Result.success(data)
@api_view(['DELETE'])
def delete(request, id):
    vol = models.Vol.objects.get(id=id)
    if vol == '':
        return result.Result.notfound('没有这位护工')
    try:
        vol.delete()
        return result.Result.success(id)
    except vol.DoesNotExist:
        return result.Result.error('删除失败')


@api_view(['PUT'])
def update(request):
    data = json.loads(request.body)
    vol = Vol(**data)
    if models.Vol.objects.filter(id=vol.id).exists():
        try:
            models.Vol.objects.filter(id=vol.id).update(**data)
            return result.Result.success(vol.id)
        except:
            return result.Result.error('更新失败')
    return result.Result.notfound("未找到更新对象")


@api_view(['GET'])
def select_vol(request, parameter):
    try:
        data = models.Vol.objects.get(Q(id=parameter) | Q(name=parameter))
        data_dict = {key: value for key, value in data.__dict__.items() if key != '_state'}
        return result.Result.success(data_dict)
    except:
        return result.Result.notfound("查询失败")


@api_view(['GET'])
def select(request):
    data_list = []
    try:
        data = models.Vol.objects.filter()
        for item in data:
            data_dict = {key: value for key, value in item.__dict__.items() if key != '_state'}
            data_list.append(data_dict)
        return result.Result.success(data_list)
    except:
        return result.Result.error("获取失败")
