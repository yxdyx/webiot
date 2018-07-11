"""webselfs URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
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
from django.contrib import admin
from django.urls import path, re_path
from webc import views
from webc.utils import Ali

urlpatterns = [
    # path('admin/', admin.site.urls),
    path('', views.login),
    path('index/', views.index),
    path('page/main/', views.main),
    path('add_device/', views.add_device),
    path('add_user/', views.add_user),
    path('delete_user/', views.delete_user),
    path('delete_device/', views.delete_device),
    path('change/', views.change_user_pwd),
    path('logout/', views.logout),
    path('deviceinfoall/', Ali.device_status_all),
    path('deviceinfosolo/', Ali.device_status_solo),
    path('userinfoall/', Ali.user_info_all),
    path('userinfosolo/', Ali.user_info_solo),
]
