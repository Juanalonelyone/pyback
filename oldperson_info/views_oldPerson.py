import json

from django.db.models import Q

# Create your views here.
from django.http import JsonResponse

from djangoProject import result
from face_Module import FaceDepart
from img import get_image_info_from_path
from oldperson_info import models
from oldperson_info.models import OldpersonInfo
from rest_framework.decorators import api_view

from video_catch import views_video_catch

# 测试时间
import time


# 增加老人信息
@api_view(['POST'])
def add(request):
    if request.method == 'POST' and request.FILES['img']:
        last_old = models.OldpersonInfo.objects.last()
        if last_old is None:
            last_id = 0
        else:
            last_id = int(last_old.id)

        # print(last_id)
        image_file = request.FILES['img']
        data = json.loads(request.POST['old'])  # 获取老人信息的JSON数据
        name = data['name']
        saved_path = './face_Module/face_db/old_' + name + str(last_id + 1) + '.jpg'
        # 创建OldpersonInfo对象并保存到数据库
        data['id'] = str(last_id + 1)
        data['img_url'] = saved_path
        old_person = models.OldpersonInfo.objects.create(**data)

        # 在这里执行保存图像的操作
        # 假设你有一个名为'uploads'的Media文件夹用于保存图像文件
        # 你可以使用Django的默认存储设置来保存图像文件

        with open(saved_path, 'wb') as f:
            for chunk in image_file.chunks():
                f.write(chunk)

        # 返回图像保存路径和新创建的老人信息给前端
        response_data = {'msg': '老人信息和图像保存成功', 'path': saved_path, 'old_person': old_person.id}
        FaceDepart.load_faces(views_video_catch.model, views_video_catch.faces_embedding, views_video_catch.face_db)
        return JsonResponse(response_data)
    else:
        return result.Result.data_null('数据不能为空')


# 删除老人信息
@api_view(['DELETE'])
def delete(request, id):
    old_person = models.OldpersonInfo.objects.get(id=id)
    if old_person == '':
        return result.Result.notfound('没有这位老人')
    try:
        data = models.Event.objects.filter(old_id=old_person.id)
        for item in data:
            item.delete()
        old_person.delete()
        return result.Result.success(id)
    except old_person.DoesNotExist:
        return result.Result.error('删除失败')


# 更新老人信息
@api_view(['PUT'])
def update(request):
    data = json.loads(request.data['old'])  # 获取老人信息的JSON数据
    data_id = data['id']
    if 'img' in request.FILES:
        image_file = request.FILES['img']
        name = data['name']
        saved_path = './face_Module/face_db/old_' + name + data_id + '.jpg'
        # 创建OldpersonInfo对象并保存到数据库
        data['img_url'] = saved_path
        with open(saved_path, 'wb') as f:
            for chunk in image_file.chunks():
                f.write(chunk)
    if models.OldpersonInfo.objects.filter(id=data_id).exists():
        models.OldpersonInfo.objects.filter(id=data_id).update(**data)

        # 在这里执行保存图像的操作
        # 假设你有一个名为'uploads'的Media文件夹用于保存图像文件
        # 你可以使用Django的默认存储设置来保存图像文件
        # 返回图像保存路径和新创建的老人信息给前端
        response_data = {'msg': '老人信息和图像保存成功'}
        FaceDepart.load_faces(views_video_catch.model, views_video_catch.faces_embedding, views_video_catch.face_db)
        return JsonResponse(response_data)
    else:
        return result.Result.notfound("修改的数据不存在")


# 根据条件查询
@api_view(['GET'])
def select_old(request, parameter):
    try:
        data = models.OldpersonInfo.objects.get(Q(id=parameter) | Q(name=parameter) | Q(room=parameter))
        data_dict = {key: value for key, value in data.__dict__.items() if key != '_state'}
        img_url = data_dict.get('img_url')
        image_info = get_image_info_from_path(img_url)
        data_dict['image_info'] = image_info
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
