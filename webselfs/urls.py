"""webselfs URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see
    https//docs.djangoproject.com/en/2.0/topics/http/urls/
Examples
Function views
    1. Add an import  from my_app import views
    2. Add a URL to urlpatterns  path('', views.home, name='home')
Class-based views
    1. Add an import  from other_app.views import Home
    2. Add a URL to urlpatterns  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function from django.urls import include, path
    2. Add a URL to urlpatterns  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, re_path
from webc import views
from webc.utils import Ali

urlpatterns = [
    # path('admin/', admin.site.urls),
    path('', views.login),
    path('add_device/', Ali.add_device),# 管理员增加设备
    path('add_user/', views.add_user),# 管理员增加用户/管理员
    path('delete_user/', views.delete_user),# 管理员删除用户/管理员
    path('delete_device/', views.delete_device),# 管理员删除设备
    path('change/', views.change_user_pwd),# 管理员修改用户密码
    path('logout/', views.logout),# 登出
    # path('deviceinfoall/', Ali.device_status_all),# 管理员请求查看所有设备信息
    # path('deviceinfosolo/', Ali.device_status_solo),# 用户请求查看所拥有的设备信息
    path('userinfoall/', Ali.user_info_all), # 管理员请求查看所有用户信息
    path('userinfosolo/', Ali.user_info_solo),# 用户请求查看用户信息

    path('index/', views.index),
    path('page/main/', views.main),
    path('page/machine/newsAdd/', views.newsAdd),
    path('page/machine/machineList/', views.machineList),
    path('page/machine/machineEdit/', views.machineEdit),
    path('page/user/addUser/', views.addUser),
    path('page/user/allUsers/', views.allUsers),
    path('page/user/changePwd/', views.changePwd),
    path('page/user/editUser/', views.editUser),
]
