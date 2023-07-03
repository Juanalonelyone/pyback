from django.http import JsonResponse


class Result:

    # 请求成功
    def success(self):
        return JsonResponse({'code': 200, 'msg': '请求成功', 'data': self})

    # 未找到数据
    def notfound(self):
        return JsonResponse({'code': 401, 'msg': '查询失败:' + self})

    # 主键已存在
    def is_exist(self):
        return JsonResponse({'code': 402, 'msg': self + '已存在'})

    # 数据为空
    def data_null(self):
        return JsonResponse({'code': 403, 'msg': self + '不能为空'})

    # 发生错误
    def error(self):
        return JsonResponse({'code': 404, 'msg': self + '不能为空'})
