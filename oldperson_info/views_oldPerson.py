import json

from django.db.models import Q

# Create your views here.
from djangoProject import result
from oldperson_info import models
from oldperson_info.models import OldpersonInfo
from rest_framework.decorators import api_view


# 增加老人信息
@api_view(['POST'])
def add(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        old_person = OldpersonInfo(**data)
        print(old_person)
        if old_person.id == '':
            return result.Result.data_null('数据不能为空')
        if models.OldpersonInfo.objects.filter(id=old_person.id).exists():
            return result.Result.is_exist('用户id已存在')
        models.OldpersonInfo.objects.create(**data)
        return result.Result.success(data)


# 删除老人信息
@api_view(['DELETE'])
def delete(request, id):
    old_person = models.OldpersonInfo.objects.get(id=id)
    if old_person == '':
        return result.Result.notfound('没有这位老人')
    try:
        old_person.delete()
        return result.Result.success(id)
    except old_person.DoesNotExist:
        return result.Result.error('删除失败')


# 更新老人信息
@api_view(['PUT'])
def update(request):
    data = json.loads(request.body)
    old_person = OldpersonInfo(**data)
    if models.OldpersonInfo.objects.filter(id=old_person.id).exists():
        try:
            models.OldpersonInfo.objects.filter(id=old_person.id).update(**data)
            return result.Result.success(old_person.id)
        except:
            return result.Result.error('更新失败')
    return result.Result.notfound("未找到更新对象")


# 根据条件查询
@api_view(['GET'])
def select_old(request, parameter):
    try:
        data = models.OldpersonInfo.objects.get(Q(id=parameter) | Q(name=parameter) | Q(room=parameter))
        data_dict = {key: value for key, value in data.__dict__.items() if key != '_state'}
        return result.Result.success(data_dict)
    except:
        return result.Result.notfound("查询失败")


# 获取所有老人列表
@api_view(['GET'])
def select(request):
    data_list = []
    try:
        data = models.OldpersonInfo.objects.filter()
        for item in data:
            data_dict = {key: value for key, value in item.__dict__.items() if key != '_state'}
            data_list.append(data_dict)
        return result.Result.success(data_list)

    except:
        return result.Result.error("获取失败")
