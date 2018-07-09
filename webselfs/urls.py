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
from django.urls import path
from django.conf.urls import url
from webc import views
from django.contrib.auth.views import login, logout


urlpatterns = [
    path('admin/', admin.site.urls),
    # url(r'^$', views.hello),
    # path(r'', views.hello),
    # url(r'^1$', views.recv_data),
    # url(r'^admin/login/$', login),
    # url(r'^admin/logout/$', logout),
    path('',views.login),
    path('add_user/',views.add_user),
    path('add_device/',views.add_device),
    path('delete_user/',views.delete_user),
    path('delete_device/',views.delete_device),
    path('change/',views.change_user_pwd),
    path('logout/',views.logout),
]
