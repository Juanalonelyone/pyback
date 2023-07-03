from django.http import JsonResponse


class Result:

    def success(self, data):
        return JsonResponse({'code': 200, 'msg': self, 'data': data})

    def notfound(self, data):
        return JsonResponse({'code': 404, 'msg': self, 'data': data})

    def data_null(self):
        return JsonResponse({'code': 401, 'msg': self})
