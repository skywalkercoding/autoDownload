from audioop import reverse

from django.urls import reverse
import requests
from django.shortcuts import render, redirect
from django.http import JsonResponse
from apps.DownloadAPP.BaseDownload.BaseDownloadView import BaseDwloadView
from apps.CheckAPP.Base.HandleExcel.BaseView import BaseView
from apps.DownloadAPP.models import DownloadApp
from apps.UploadAPP.BaseUpView.BaseUploadView import BaseUploadView
import apps.CheckAPP.Base.HandleExcel.common as comm
# Create your views here.
class UploadFView(BaseView,BaseDwloadView):
    def get(self,request):
        taskid = self.check2place_file()
        dwlist = self.displayDownload(taskid)
        return render(request,'upload.html',{"apps":dwlist})



class DelUploadAppView(BaseDwloadView,BaseView):
    def get(self, request):
        return self.handle(request)

    def post(self, request):
        return self.handle(request)
    def handle(self, request):
        pkgnames = self.getStrParam(request, 'id')
        taskid = self.check2place_file()
        print("获取当前包名："+str(len(pkgnames)))
        if len(pkgnames) ==0:
            success = False
            print("至少选择一条")
            message="至少选择一条"
            return JsonResponse({"success": success, "message": message})
        pkgnames = pkgnames.split(',')
        count = 0


        for pkgname in pkgnames:

                print("当前要删除：" + str(pkgname))
                # BaseApp.objects.all().delete()
                appsDown=DownloadApp.objects.filter(tasknum=taskid, pkgname=pkgname.strip())
                if appsDown.exists():
                    appsDown.delete()
                    count = count + 1
                    message = "删除成功"
                    success = True

                else:
                    message = "数据库内部错误"
                    success = False

        return JsonResponse({"success": success, "message": message})


class LoginFproView(BaseUploadView,BaseView,BaseDwloadView):
    def get(self,request):
        print("start login")
        upsuccessList=[]
        brower,isSetChrome=self.setChrome("D:/")
        if not isSetChrome:
            success = False
            message = '打开失败'
        if self.loginFproject(brower,comm.ADD)[0]:
            taskid = self.check2place_file()
            getDwList=self.getDownloadInfo(taskid)
            if len(getDwList)==0:
                success = False
                message = "Upload Failed"
            else:
                for apk in getDwList:
                    choose = comm.ChooseValue
                    message, isSearch = self.searchApp(brower, apk['pkgName'], apk['arh'], apk['dversion'], choose,
                                                       apk['apkpath'])
                    if isSearch:
                        upStatus = "Uploaded"
                        apkupload = {
                            'id': taskid,
                            'pkg': apk['pkgName'],
                            'upstatus': upStatus
                        }
                        success = True
                        message = "upload success"
                    else:
                        upStatus = "NoUpload"
                        apkupload = {
                            'id': taskid,
                            'pkg': apk['pkgName'],
                            'upstatus': upStatus
                        }
                        success = True
                        message = "upload success"
                upsuccessList.append(apkupload)
                self.updateSuccessStatus(upsuccessList)

        else:
            success=False
            message=self.loginFproject(brower,comm.ADD)[1]



        return JsonResponse({"success": success, "message": message})

