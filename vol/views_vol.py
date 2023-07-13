import json

from django.db.models import Q
from django.http import JsonResponse

from djangoProject import result
from img import get_image_info_from_path
from vol import models
from vol.models import Vol
from rest_framework.decorators import api_view

#对护工的增删改查


#添加护工信息
@api_view(['POST'])
def add(request):
    if request.method == 'POST' and request.FILES['img']:
        last_vol = models.Vol.objects.last()
        if last_vol is None:
            last_id = 0
        else:
            last_id = int(last_vol.id)
        image_file = request.FILES['img']
        data = json.loads(request.POST['vol'])  # 获取老人信息的JSON数据
        saved_path = 'C:/img/vol/' + str(last_id + 1) + '.jpg'
        # 创建OldpersonInfo对象并保存到数据库
        data['id'] = str(last_id + 1)
        data['img_url'] = saved_path
        vol = models.Vol.objects.create(**data)

        # 在这里执行保存图像的操作
        # 假设你有一个名为'uploads'的Media文件夹用于保存图像文件
        # 你可以使用Django的默认存储设置来保存图像文件

        with open(saved_path, 'wb') as f:
            for chunk in image_file.chunks():
                f.write(chunk)

        # 返回图像保存路径和新创建的老人信息给前端
        response_data = {'msg': '义工信息和图像保存成功', 'path': saved_path, 'vol': vol.id}
        return JsonResponse(response_data)
    else:
        return result.Result.data_null('数据不能为空')


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
    data = json.loads(request.data['vol'])  # 获取老人信息的JSON数据
    data_id = data['id']
    if 'img' in request.FILES:
        image_file = request.FILES['img']
        saved_path = 'C:/img/vol/' + data_id + '.jpg'
        # 创建OldpersonInfo对象并保存到数据库
        data['img_url'] = saved_path
        with open(saved_path, 'wb') as f:
            for chunk in image_file.chunks():
                f.write(chunk)
    if models.Vol.objects.filter(id=data_id).exists():
        models.Vol.objects.filter(id=data_id).update(**data)

        # 在这里执行保存图像的操作
        # 假设你有一个名为'uploads'的Media文件夹用于保存图像文件
        # 你可以使用Django的默认存储设置来保存图像文件
        # 返回图像保存路径和新创建的老人信息给前端
        response_data = {'msg': '义工信息和图像保存成功'}
        return JsonResponse(response_data)
    else:
        return result.Result.notfound("修改的数据不存在")



# 根据条件查询
@api_view(['GET'])
def select_vol(request, parameter):
    try:
        data = models.Vol.objects.get(Q(id=parameter) | Q(name=parameter))
        data_dict = {key: value for key, value in data.__dict__.items() if key != '_state'}
        img_url = data_dict.get('img_url')
        image_info = get_image_info_from_path(img_url)
        data_dict['image_info'] = image_info
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
