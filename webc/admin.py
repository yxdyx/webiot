from django.contrib import admin
# Register your models here.
from webc.models import *

admin.site.site_header = '物联网系统管理系统'
admin.site.site_title = '物联网系统管理系统'


# Blog模型的管理器
# @admin.register(UserInfo)
# class UserAdmin(admin.ModelAdmin):
#     list_display = ('id', 'username', 'password', 'name', 'if_admin')


@admin.register(DeviceInfo)
class DeviceAdmin(admin.ModelAdmin):
    list_display = ('id', 'devicename', 'devicesecret')


@admin.register(UandD)
class UandDAdmin(admin.ModelAdmin):
    list_display = ('id', 'userid', 'username', 'name', 'deviceid', 'devicename')
