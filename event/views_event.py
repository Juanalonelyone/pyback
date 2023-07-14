import json

from django.db.models import Q

from event import models
from djangoProject import result
from rest_framework.decorators import api_view
from event.models import Event


# Create your views here.


# 新增事件
from img import get_image_info_from_path


@api_view(['POST'])
def add(request):

    if request.method == 'POST':
        data = json.loads(request.body)
        if models.OldpersonInfo.objects.filter(id=data['old_id']):
            print(data)
            event = Event(**data)
            if event == '':
                return result.Result.data_null('数据不能为空')
            models.Event.objects.create(**data)
            return result.Result.success(data)
        return result.Result.error("存在外键，操作失败")


# 删除事件信息
@api_view(['DELETE'])
def delete(request, id):
    event = models.Event.objects.get(id=id)
    if event == '':
        return result.Result.notfound('没有该事件')
    try:
        event.delete()
        return result.Result.success(id)
    except event.DoesNotExist:
        return result.Result.error('删除失败')


# 查询信息(老头id，时间，地点)
@api_view(['GET'])
def select_event(request, parameter):
    print(parameter)
    data_list = []
    data = models.Event.objects.filter(Q(old_id=parameter) | Q(location=parameter) | Q(time=parameter))
    print(data)
    for item in data:
        data_dict = {key: value for key, value in item.__dict__.items() if key != '_state'}
        data_list.append(data_dict)
    return result.Result.success(data_list)


# 查询信息(所有)
@api_view(['GET'])
def select_all(request):
    data_list = []
    try:
        data = models.Event.objects.all()
        for item in data:
            data_dict = {key: value for key, value in item.__dict__.items() if key != '_state'}
            oldperson_info = models.OldpersonInfo.objects.filter(id=data_dict.get('old_id')).values('name')
            if oldperson_info:
                data_dict['name'] = oldperson_info[0]['name']
            else:
                data_dict['name'] = None
            data_list.append(data_dict)
        return result.Result.success(data_list)
    except:
        return result.Result.error("获取失败")


# 查询信息(id)
@api_view(['GET'])
def select_id(request, id):
    try:
        data = models.Event.objects.get(id=id)
        data_dict = {key: value for key, value in data.__dict__.items() if key != '_state'}
        img_url = data_dict.get('img_url')
        img_info = get_image_info_from_path(img_url)
        data_dict['image_info'] = img_info
        return result.Result.success(data_dict)
    except:
        return result.Result.notfound("查询失败")