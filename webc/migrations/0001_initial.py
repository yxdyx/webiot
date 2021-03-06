# Generated by Django 2.0.5 on 2018-07-13 00:26

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='DeviceInfo',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('devicename', models.CharField(max_length=32)),
                ('devicesecret', models.CharField(max_length=32)),
                ('type', models.CharField(max_length=32)),
                ('value', models.CharField(blank=True, max_length=32, null=True)),
            ],
            options={
                'db_table': 'Device',
            },
        ),
        migrations.CreateModel(
            name='UandD',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('username', models.CharField(max_length=32)),
                ('name', models.CharField(max_length=32)),
                ('devicename', models.CharField(max_length=32)),
                ('device_type', models.CharField(max_length=32)),
                ('deviceid', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='webc.DeviceInfo')),
                ('userid', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'UandD',
            },
        ),
    ]
