from django.db import models
from django.contrib.auth.models import User


# Create your models here.
# class UserInfo(models.Model):
#     id = models.AutoField(primary_key=True)
#     username = models.CharField(max_length=32)
#     password = models.CharField(max_length=32)
#     name = models.CharField(max_length=32)
#     if_admin = models.BooleanField()


class DeviceInfo(models.Model):
    id = models.AutoField(primary_key=True)
    devicename = models.CharField(max_length=32)
    devicesecret = models.CharField(max_length=32)
    type = models.CharField(max_length=32)

    class Meta:
        db_table = 'Device'


class UandD(models.Model):
    id = models.AutoField(primary_key=True)
    userid = models.ForeignKey(User, on_delete=models.CASCADE)
    username = models.CharField(max_length=32)
    name = models.CharField(max_length=32)
    deviceid = models.ForeignKey(DeviceInfo, on_delete=models.CASCADE)
    devicename = models.CharField(max_length=32)
    device_type=models.CharField(max_length=32)

    class Meta:
        db_table = 'UandD'
