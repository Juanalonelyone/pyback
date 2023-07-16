"""
URL configuration for djangoProject project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import path, re_path
from rest_framework.documentation import include_docs_urls

from cap import views_cap
from first_app import views
from oldperson_info import views_oldPerson
from event import views_event
from worker import views_Worker
from vol import views_vol
from video_catch import views_video_catch
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

schema_view = get_schema_view(
    openapi.Info(
        title="Lemon API接口文档平台",    # 必传
        default_version='v1',   # 必传
        description="这是一个美轮美奂的接口文档",
        terms_of_service="http://api.keyou.site",
        contact=openapi.Contact(email="keyou100@qq.com"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    # permission_classes=(permissions.AllowAny,),   # 权限类
)


urlpatterns = [
    # 管理员登陆
    path('login/', views.login),
    # 对老人表进行操作
    path('add_oldPerson/', views_oldPerson.add),
    path('delete_oldPerson/<id>', views_oldPerson.delete),
    path('update_oldPerson/', views_oldPerson.update),
    path('select_old/<parameter>', views_oldPerson.select_old),
    path('select_allOld/', views_oldPerson.select),


    path('add_vol/', views_vol.add),
    path('delete_vol/<id>', views_vol.delete),
    path('update_vol/', views_vol.update),
    path('select_vol/<parameter>', views_vol.select_vol),
    path('select_allVol/', views_vol.select),

    # 对事件表进行操作
    path('add_event/', views_event.add),
    path('select_event/<parameter>', views_event.select_event),
    path('select_allEvent/', views_event.select_all),
    path('select_EventId/<id>', views_event.select_id),
    path('delete_Event/<id>', views_event.delete),
    # 对工作人员表进行操作
    path('add_Worker/', views_Worker.add),
    path('delete_Worker/<id>', views_Worker.delete),
    path('update_Worker/', views_Worker.update),
    path('select_Worker/<parameter>', views_Worker.select_worker),
    path('select_allWorker/', views_Worker.select),

    path('video/<id>', views_video_catch.video_stream),
    path('stop_video_stream/', views_video_catch.stop_video_stream),
    path('enable_video_stream/', views_video_catch.enable_video_stream),
    # path('video1/<id>', views_video_catch.video_stream),
    # path('video2/<id>', views_video_catch.video_stream),
    # 对摄像头进行操作
    path('add_Cap/',views_cap.add),
    path('delete_Cap/<id>',views_cap.delete),
    path('update_Cap/',views_cap.update),
    path('select_Cap/<id>',views_cap.select),
    path('select_allCap/',views_cap.selectAll),

    # swegger
    path('docs/', include_docs_urls(title='API接口文档', description='xxx描述')),
    re_path(r'^swagger(?P<format>\.json|\.yaml)$', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),

]
