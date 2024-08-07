from django.db import models

# Create your models here.
class DownloadApp(models.Model):
    timecheck = models.CharField(max_length=100, primary_key=True, verbose_name='创建时间')
    tasknum = models.CharField(max_length=50, default='', verbose_name="Task编号")
    pkgname = models.CharField(max_length=100, default='', verbose_name="应用包名")
    dversion=models.CharField(max_length=100, default='', verbose_name="下载的apk版本")
    apkfilename=models.CharField(max_length=100, default='', verbose_name="apk的文件名字")
    apkfilePath=models.CharField(max_length=200, default='', verbose_name="APK报错的路径")
    installStatus=models.CharField(max_length=50, default='', verbose_name="安装状态")
    uploadStatus=models.CharField(max_length=50, default='', verbose_name="upload的状态")

    class Meta:
        db_table = 't_download_app'
        verbose_name = '下载apk地方'
        verbose_name_plural = verbose_name
