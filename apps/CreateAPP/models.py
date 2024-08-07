from django.db import models
from apps.CheckAPP.models import BaseApp,FavorBaseApp
# Create your models here.

class CreateApp(models.Model):
    pkgname = models.CharField(max_length=100, primary_key=True, verbose_name="应用包名")
    appname = models.CharField(max_length=100, default='', verbose_name='应用名称')
    appcategory = models.CharField(max_length=100, default='', verbose_name='app类型')
    Appicon =models.ImageField(upload_to="img", max_length='500', verbose_name="图标的路径")
    saveiconpath=models.CharField(max_length=200, default='', verbose_name='图片保存绝对路径')
    CreateStatus=models.CharField(max_length=50, default='', verbose_name='创建app状态')
    createTime = models.CharField(max_length=100, default='', verbose_name='创建时间')

    class Meta:
        db_table = 't_CreateApp'
        verbose_name = '创建应用'
        verbose_name_plural = verbose_name

    def getJsonObj(self):
        apps={
            "pkgname":self.pkgname,
             "appname":self.appname,
             "appcategory":self.appcategory,
             "Appicon":self.Appicon.url,
             'savepath':self.saveiconpath,
             "createTime":self.createTime,
        }
        return apps




class CheckVersion(models.Model):
    favorId=models.AutoField(primary_key=True,verbose_name="版本ID")
    tasknum = models.CharField( max_length=50,default='', verbose_name="Task编号")
    fversion = models.CharField(max_length=100, default='', verbose_name='f版本')
    googleversion = models.CharField(max_length=100, default='', verbose_name='谷歌版本')
    upgradestatus=models.CharField(max_length=100, default='', verbose_name='升级状态')
    timecheck = models.CharField(max_length=100, default='', verbose_name='创建时间')
    appVerObj = models.ForeignKey(BaseApp, on_delete=models.CASCADE,
                                  verbose_name='检查版本信息')
    class Meta:
        db_table = 't_check_version'
        verbose_name = '检查版本表'
        verbose_name_plural = verbose_name
class FavorVersion(models.Model):
    favorId=models.AutoField(primary_key=True,verbose_name="版本ID")
    tasknum = models.CharField(max_length=50, default='', verbose_name="Task编号")
    fversion = models.CharField(max_length=100, default='', verbose_name='f版本')
    googleversion = models.CharField(max_length=100, default='', verbose_name='谷歌版本')
    upgradestatus = models.CharField(max_length=100, default='', verbose_name='升级状态')
    timecheck = models.CharField(max_length=100, default='', verbose_name='创建时间')
    appVerObj = models.ForeignKey(FavorBaseApp, on_delete=models.CASCADE,
                                  verbose_name='检查版本信息')
    class Meta:
        db_table = 't_Favor_version'
        verbose_name = '重点看护的app'
        verbose_name_plural = verbose_name