# Generated by Django 4.2.4 on 2023-11-09 09:47

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='BaseApp',
            fields=[
                ('pkgname', models.CharField(max_length=100, primary_key=True, serialize=False, verbose_name='应用包名')),
                ('appname', models.CharField(default='', max_length=100, verbose_name='应用名称')),
                ('areaname', models.CharField(default='', max_length=100, verbose_name='区域名称')),
                ('releasestatus', models.CharField(default='', max_length=50, verbose_name='Ag上架状态')),
                ('downloadlink', models.CharField(default='', max_length=300, verbose_name='下载apk地址')),
                ('arch', models.CharField(default='', max_length=50, verbose_name='apk的位数')),
                ('createTime', models.CharField(default='', max_length=100, verbose_name='创建时间')),
            ],
            options={
                'verbose_name': '基础应用信息',
                'verbose_name_plural': '基础应用信息',
                'db_table': 't_BaseAppInfo',
            },
        ),
        migrations.CreateModel(
            name='FavorBaseApp',
            fields=[
                ('pkgname', models.CharField(max_length=100, primary_key=True, serialize=False, verbose_name='应用包名')),
                ('appname', models.CharField(default='', max_length=100, verbose_name='应用名称')),
                ('areaname', models.CharField(default='', max_length=100, verbose_name='区域名称')),
                ('releasestatus', models.CharField(default='', max_length=50, verbose_name='Ag上架状态')),
                ('downloadlink', models.CharField(default='', max_length=300, verbose_name='下载apk地址')),
                ('arch', models.CharField(default='', max_length=50, verbose_name='apk的位数')),
                ('createTime', models.CharField(default='', max_length=100, verbose_name='创建时间')),
            ],
            options={
                'verbose_name': '重点看护的app',
                'verbose_name_plural': '重点看护的app',
                'db_table': 't_FavorAppInfo',
            },
        ),
    ]
