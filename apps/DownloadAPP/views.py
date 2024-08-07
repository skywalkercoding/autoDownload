import json,random
import apps.DownloadAPP.BaseDownload.downComm as dComm
from django.shortcuts import render
from django.http import StreamingHttpResponse
from apps.CheckAPP.Base.HandleExcel.BaseView import BaseView
from django.http import HttpResponse,JsonResponse
from apps.DownloadAPP.BaseDownload.BaseDownloadView import BaseDwloadView
# Create your views here.
class DownloadView(BaseDwloadView,BaseView):
    def get(self,request):
        taskid=self.check2place_file()
        dwlist=self.displayDownload(taskid)
        return render(request,"download.html",{"apps":dwlist})




class ConnectAppiumView(BaseDwloadView,BaseView):
    def get(self,request):
        print("Starting Connect Appium")
        conRes=self.checkPhoneConnect()
        taksId = self.check2place_file()
        if  conRes:
           data={'success':True,'message:':"connected"}
           print(" Connected ")

           getInstalledList=self.installStart(taksId)

           data = {'success': True, 'message': "Install Success"}
        else:
            data = {'success': False, 'message': "connect failed"}

            print(" Connect Appium Failed ")
        return JsonResponse(data)

class DelAppView(BaseDwloadView,BaseView):
    def get(self,request):
        print("Del install ")

        taksId=self.check2place_file()
        if self.checkPhoneConnect():
              getDelList=self.delpkg(request,taksId)
              data = {'success': True, 'message': json.dumps(getDelList)}
        else:
            data = {'success': False, 'message': "Please check connect Phone "}
        return JsonResponse(data)
class DownloadExcelView(BaseDwloadView,BaseView):
    def get(self,request):
        taskid = self.check2place_file()
        getNewList=self.readAllPkgData(taskid)
        print(json.dumps(getNewList))
        num=random.randint(1,9999)
        filename='%s_%s.xlsx' % (taskid,num)
        path = self.createExcelrep(filename,getNewList)

        response=StreamingHttpResponse(self.file_iterator(request,path))
        response['Content-Type']='application/vnd.ms-excel'
        response['Content-Disposition']='attachment;filename='+filename
        return response


class TestingInfoView(BaseView,BaseDwloadView):
    def get(self,request):
        taskid = self.check2place_file()
        getNewList = self.readAllPkgData(taskid)
        return render(request,"testing.html",{"apps":getNewList})
class UploadAppView(BaseDwloadView,BaseView):
    def get(self,request):
        print("start upload")
        taskid = self.check2place_file()
        path=dComm.Update_Apk
        getappList=self.scanPathApp(path)
        getres=self.insertApkInfo(taskid,getappList)
        if getres:
             data = {'success': True, 'message': "Insert apk Success"}
        else:
            data = {'success': False, 'message': "Insert apk Failed"}
        return JsonResponse(data)