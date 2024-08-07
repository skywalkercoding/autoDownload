# Generated by Django 4.2.4 on 2023-11-09 09:47

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('CheckAPP', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='CreateApp',
            fields=[
                ('pkgname', models.CharField(max_length=100, primary_key=True, serialize=False, verbose_name='应用包名')),
                ('appname', models.CharField(default='', max_length=100, verbose_name='应用名称')),
                ('appcategory', models.CharField(default='', max_length=100, verbose_name='app类型')),
                ('Appicon', models.ImageField(max_length='500', upload_to='img', verbose_name='图标的路径')),
                ('saveiconpath', models.CharField(default='', max_length=200, verbose_name='图片保存绝对路径')),
                ('CreateStatus', models.CharField(default='', max_length=50, verbose_name='创建app状态')),
                ('createTime', models.CharField(default='', max_length=100, verbose_name='创建时间')),
            ],
            options={
                'verbose_name': '创建应用',
                'verbose_name_plural': '创建应用',
                'db_table': 't_CreateApp',
            },
        ),
        migrations.CreateModel(
            name='FavorVersion',
            fields=[
                ('favorId', models.AutoField(primary_key=True, serialize=False, verbose_name='版本ID')),
                ('tasknum', models.CharField(default='', max_length=50, verbose_name='Task编号')),
                ('fversion', models.CharField(default='', max_length=100, verbose_name='f版本')),
                ('googleversion', models.CharField(default='', max_length=100, verbose_name='谷歌版本')),
                ('upgradestatus', models.CharField(default='', max_length=100, verbose_name='升级状态')),
                ('timecheck', models.CharField(default='', max_length=100, verbose_name='创建时间')),
                ('appVerObj', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='CheckAPP.baseapp', verbose_name='检查版本信息')),
            ],
            options={
                'verbose_name': '重点看护的app',
                'verbose_name_plural': '重点看护的app',
                'db_table': 't_Favor_version',
            },
        ),
        migrations.CreateModel(
            name='CheckVersion',
            fields=[
                ('favorId', models.AutoField(primary_key=True, serialize=False, verbose_name='版本ID')),
                ('tasknum', models.CharField(default='', max_length=50, verbose_name='Task编号')),
                ('fversion', models.CharField(default='', max_length=100, verbose_name='f版本')),
                ('googleversion', models.CharField(default='', max_length=100, verbose_name='谷歌版本')),
                ('upgradestatus', models.CharField(default='', max_length=100, verbose_name='升级状态')),
                ('timecheck', models.CharField(default='', max_length=100, verbose_name='创建时间')),
                ('appVerObj', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='CheckAPP.favorbaseapp', verbose_name='检查版本信息')),
            ],
            options={
                'verbose_name': '检查版本表',
                'verbose_name_plural': '检查版本表',
                'db_table': 't_check_version',
            },
        ),
    ]