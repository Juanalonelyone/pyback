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
from django.urls import path
from first_app import views
from oldperson_info import views_oldPerson
from event import views_event

urlpatterns = [
    # 管理员登陆
    path('login/', views.login),
    # 对老人表进行操作
    path('add_oldPerson/', views_oldPerson.add),
    path('delete_oldPerson/<id>', views_oldPerson.delete),
    path('update_oldPerson/', views_oldPerson.update),
    path('select_old/<parameter>', views_oldPerson.select_old),
    path('select_allOld/', views_oldPerson.select),
    # 对事件表进行操作
    path('add_event/', views_event.add),
    path('select_event/<parameter>', views_event.select_event),
    path('select_allEvent/', views_event.select_all),
    path('select_EventId/<id>', views_event.select_id)
]
