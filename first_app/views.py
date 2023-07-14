import json

from rest_framework.decorators import api_view

from first_app import models
from djangoProject import result


# Create your views here.


@api_view(['POST'])
def login(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        admin_name = data.get('admin_name', '')
        admin_password = data.get('admin_password', '')
        if admin_name == '' or admin_password == '':
            return result.Result.data_null('账户或密码不能为空')
        if models.Admin.objects.filter(admin_name=admin_name, admin_password=admin_password).exists():
            # print("success")
            return result.Result.success(data)
        return result.Result.notfound('用户不存在或密码错误，请重新输入')


