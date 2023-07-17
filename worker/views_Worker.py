import json

from django.db.models import Q
from django.http import JsonResponse
from django.shortcuts import render
from rest_framework.decorators import api_view


from djangoProject import result
from face_Module import FaceDepart
from img import get_image_info_from_path
from worker import models
from worker.models import Worker

from video_catch import views_video_catch


# Create your views here.
# 增加工作人员信息
@api_view(['POST'])
def add(request):
    if request.method == 'POST' and request.FILES['img']:
        last_worker = models.Worker.objects.last()
        if last_worker is None:
            last_id = 0
        else:
            last_id = int(last_worker.id)
        # print(last_id)
        image_file = request.FILES['img']
        data = json.loads(request.POST['worker'])  # 获取工作人员信息的JSON数据
        name = data['name']
        saved_path = './face_Module/face_db/worker_' + name + '_' + str(last_id + 1) + '.jpg'
        # 创建OldpersonInfo对象并保存到数据库
        data['id'] = str(last_id + 1)
        data['img_url'] = saved_path
        worker = models.Worker.objects.create(**data)

        # 在这里执行保存图像的操作
        # 假设你有一个名为'uploads'的Media文件夹用于保存图像文件
        # 你可以使用Django的默认存储设置来保存图像文件

        with open(saved_path, 'wb') as f:
            for chunk in image_file.chunks():
                f.write(chunk)

        # 返回图像保存路径和新创建的老人信息给前端
        response_data = {'msg': '员工信息和图像保存成功', 'path': saved_path, 'worker': worker.id}
        FaceDepart.load_faces(views_video_catch.model, views_video_catch.faces_embedding, views_video_catch.face_db)
        return JsonResponse(response_data)
    else:
        return result.Result.data_null('数据不能为空')


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
    data = json.loads(request.data['worker'])   # 获取老人信息的JSON数据
    data_id = data['id']
    if 'img' in request.FILES:
        image_file = request.FILES['img']
        name = data['name']
        saved_path = './face_Module/face_db/worker_' + name + '_' + data_id + '.jpg'
        # 创建OldpersonInfo对象并保存到数据库
        data['img_url'] = saved_path
        with open(saved_path, 'wb') as f:
            for chunk in image_file.chunks():
                f.write(chunk)
    if models.Worker.objects.filter(id=data_id).exists():
        models.Worker.objects.filter(id=data_id).update(**data)

        # 在这里执行保存图像的操作
        # 假设你有一个名为'uploads'的Media文件夹用于保存图像文件
        # 你可以使用Django的默认存储设置来保存图像文件
        # 返回图像保存路径和新创建的老人信息给前端
        response_data = {'msg': '员工信息和图像保存成功'}
        FaceDepart.load_faces(views_video_catch.model, views_video_catch.faces_embedding, views_video_catch.face_db)
        return JsonResponse(response_data)
    else:
        return result.Result.notfound("修改的数据不存在")




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
        img_url = data_dict.get('img_url')
        image_info = get_image_info_from_path(img_url)
        data_dict['image_info'] = image_info
        return result.Result.success(data_dict)
    except:
        return result.Result.notfound("查询失败")
