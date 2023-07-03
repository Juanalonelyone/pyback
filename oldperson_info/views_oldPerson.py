import json

from django.core.serializers import serialize
from django.shortcuts import render

# Create your views here.
from djangoProject import result
from oldperson_info import models
from oldperson_info.models import OldpersonInfo
from rest_framework.decorators import api_view


def add(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        old_person = OldpersonInfo(**data)
        print(old_person)
        if old_person.id == '':
            return result.Result.data_null('数据不能为空')
        if models.OldpersonInfo.objects.filter(id=old_person.id).exists():
            return result.Result.is_exist('用户id')
        models.OldpersonInfo.objects.create(**data)
        return result.Result.success(data)


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

