from django.db import models

# Create your models here.
class BaseApp(models.Model):
    pkgname = models.CharField(max_length=100, primary_key=True, verbose_name="应用包名")
    appname = models.CharField(max_length=100, default='', verbose_name='应用名称')
    areaname = models.CharField(max_length=100, default='', verbose_name='区域名称')
    releasestatus = models.CharField(max_length=50, default='', verbose_name='Ag上架状态')
    downloadlink = models.CharField(max_length=300, default='', verbose_name='下载apk地址')
    arch=models.CharField(max_length=50,default='',verbose_name="apk的位数")

    createTime = models.CharField(max_length=100, default='', verbose_name='创建时间')

    class Meta:
        db_table = 't_BaseAppInfo'
        verbose_name = '基础应用信息'
        verbose_name_plural = verbose_name

    def getJsonObj(self):
            appsfiles={
              "pkgname":self.pkgname,
              "appname":self.appname,
              "areaname":self.areaname,
              "releasestatus":self.releasestatus,
              "downloadlink":self.downloadlink,
              "arch":self.arch,
              "createTime":self.createTime

        }
            return appsfiles



class FavorBaseApp(models.Model):
    pkgname = models.CharField(max_length=100, primary_key=True, verbose_name="应用包名")
    appname = models.CharField(max_length=100, default='', verbose_name='应用名称')
    areaname = models.CharField(max_length=100, default='', verbose_name='区域名称')
    releasestatus = models.CharField(max_length=50, default='', verbose_name='Ag上架状态')
    downloadlink = models.CharField(max_length=300, default='', verbose_name='下载apk地址')
    arch=models.CharField(max_length=50,default='',verbose_name="apk的位数")
    createTime = models.CharField(max_length=100, default='', verbose_name='创建时间')
    class Meta:
        db_table = 't_FavorAppInfo'
        verbose_name = '重点看护的app'
        verbose_name_plural = verbose_name

