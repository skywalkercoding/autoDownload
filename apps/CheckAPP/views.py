import shutil

from django.urls import reverse
import requests

from celery.worker.state import requests

from datetime import datetime
import apps.CheckAPP.Base.HandleExcel.common as comm
from django.shortcuts import render
from apps.DownloadAPP.BaseDownload.BaseDownloadView import ParseApkLocal
from django.http import HttpResponse,JsonResponse,StreamingHttpResponse
from apps.CheckAPP.Base.HandleExcel.BaseView import BaseView
from apps.CheckAPP.Base.JavaDown.DownloadView import DownloadView
from django.conf import settings
import os,json, calendar,time
from django.shortcuts import redirect
from  apps.CheckAPP.models import BaseApp,FavorBaseApp
from apps.CreateAPP.models import CheckVersion
from apps.DownloadAPP.models import DownloadApp

from celery import Celery
# Create your views here.

app = Celery('CheckAPP')
app.config_from_object('django.conf:settings', namespace='CELERY')
class BaseAppView(BaseView):

    def get(self,request):
        apps = []
        appBaseInfos=BaseApp.objects.all()
        i=1
        for app in appBaseInfos:
            appBaseInfo={
                'num':i,
                'pkgName':app.pkgname,
                'appName':app.appname,
                'place':app.areaname,
                'status':app.releasestatus,
                'link':app.downloadlink,
                'arch':app.arch,
            }

            apps.append(appBaseInfo)
            i=i+1
        self.delJson_file('search1th')
        return render(request,"index.html",{"apps":apps})

class UploadExcelView(BaseView):
    def post(self,request):
        excelFiles = request.FILES.get("excel.file")

        if excelFiles is None:
            print("文件不能为空")
            data = {'success': False, 'message': 'Please upload Excel aaaa'}


        else:

            excel_path=self.uploadCommonFile(request,'excel.file')
            if excelFiles.name.split('.')[-1] not in ['xls', 'xlsx']:
                data = {'success': False, 'message': 'excel type no support '}

            else:
               isUpEDxce,message=self.readExcel(excel_path)
               if isUpEDxce:
                   data = {'success': True, 'message': message}

               else:
                   data = {'success': False, 'message': message}

        return JsonResponse(data)
class UploadControlExcelView(BaseView):
    def post(self,request):
        excelFiles = request.FILES.get("excel.file")

        if excelFiles is None:
            print("文件不能为空")
            data = {'success': False, 'message': 'Please upload Excel aaaa'}


        else:

            excel_path=self.uploadCommonFile(request,'excel.file')
            if excelFiles.name.split('.')[-1] not in ['xls', 'xlsx']:
                data = {'success': False, 'message': 'excel type no support '}

            else:
               isUpEDxce,message=self.readControlExcel(excel_path)
               if isUpEDxce:
                   data = {'success': True, 'message': message}

               else:
                   data = {'success': False, 'message': message}

        return JsonResponse(data)

class AppListView(BaseView):
    def post(self,request):
        self.getPageAndSize(request)
        if request.POST:
           pkgList=[]
           getQuery=self.getStrParam(request,"query")
           getPlace = self.getStrParam(request, "r_place")
           getStatus = self.getStrParam(request, "status")
           appsList=self.searchKey(getQuery,getPlace,getStatus)
           for pkg in appsList:
               link=self.getThreePartLink(pkg['pkgName'])
               pkglink={
                   "pkg":pkg['pkgName'],
                   "link":link[0]
               }
               pkgList.append(pkglink)

           save_json = json.dumps(pkgList)
           self.save_search_as_json("search.json", save_json)

           return render(request,'Index.html',{"apps":appsList})

class CheckStatusView(BaseView):
    def post(self,request):
        if request.POST:
            getCheckStatus=self.getStrParam(request,"check.search")
            taskids,isFindJson=self.getTaskPathName("checkv2th")
            if not isFindJson:
                return redirect('/check/')
            taskid=taskids[0]
            savePathName=taskid+".json"
            appsList,pkgList=self.checkSearchKey(taskid,getCheckStatus)
            appdownload=[]
            for pkg in pkgList:
                   link=self.getThreePartLink(pkg)
                   appslink={
                    'pkg':pkg,
                    'link':link[0]
                }
                   appdownload.append(appslink)
            self.save_downlaod_as_json(savePathName, json.dumps(appdownload))
            return render(request, 'checkv.html',{"apps":appsList})

class NextCheckView(BaseView):
    def get(self,request):
        productIds,isFindJson = self.getTaskPathName("checkv2th")
        if not isFindJson:
            return redirect('/loading/')
        productId=productIds[0]
        appsVerion=CheckVersion.objects.all()

        checkList=[]
        if productId is not None:
            print("获取check任务ID：" + productId)
            num=1
            apps=appsVerion.filter(tasknum__contains=productId)
            for app in apps:
                appCheckinfo = {
                    "num": num,
                    "pkgName": app.appVerObj.pkgname,
                    "fversion": app.fversion,
                    "gversion": app.googleversion,
                    "upstatus": app.upgradestatus,

                }
                num=num+1
                checkList.append(appCheckinfo)
        return render(request, 'checkv.html',{"apps":checkList})

class LoadingVersionView(BaseView):
    def get(self,request):
        self.delJson_file('checkv2th')
        self.delJson_file('download3th')
        # self.delJson_file('search1th')
        getTaskPath = '%s/saveJson/search1th/%s' % (settings.MEDIA_ROOT, "search.json")
        if not os.path.exists(getTaskPath):
            appsList=self.getBaseAppAll()
            self.save_search_as_json("search.json", json.dumps(appsList))
        if not self.checkApiUsage(comm.APKPURE_URL):
            data = {
                'success': False,
                'message': 'Apikey credit usage exceeded'

            }
        else:
             getSearchList = self.readJson(getTaskPath)
             checkList = []
             appList = []
             num = 1
             productId = self.generate_task_id()

             for pkgname in getSearchList:
                  Fv = self.getFVesion(pkgname['pkg'])
                  Gv = self.getGVersion(pkgname['pkg'])
                  Fv=Fv.strip()
                  if comm.Err2 in str(Gv) or Gv is None or comm.Err1 in str(Gv) or comm.Err3 in str(Gv):
                       Gv = self.checkURLSouce(pkgname['link'])
                  if Fv is None:
                       Fv = comm.Err3
                  if Gv is None:
                       Gv = comm.Err3
                  getResult = self.getUpStatus(Fv, Gv)
                  if getResult is None:
                        getResult = comm.Upgrade1
                  print(str(num) + ")" + pkgname['pkg'] + ":" + "F:" + Fv + "-G:" + Gv + "-Status:" + getResult)
                  baseAppObj=BaseApp.objects.get(pkgname=pkgname['pkg'])

                  date = datetime.now()
                  insertdb = CheckVersion(timecheck=date, tasknum=productId,appVerObj=baseAppObj, fversion=Fv,
                                    googleversion=Gv, upgradestatus=getResult)
                  appList.append(insertdb)
                  num = num + 1

             CheckVersion.objects.bulk_create(appList, ignore_conflicts=True)
             print("执行完成获取任务号：" + productId)
             data = {
                 'success': True,
                 'message': 'Success'

             }
             newTaskPath = '%s/saveJson/checkv2th/%s' % (settings.MEDIA_ROOT, productId + ".json")
             shutil.copy2(getTaskPath, newTaskPath)

        return JsonResponse(data)


class DownloadingView(BaseView , DownloadView,ParseApkLocal):
    def get(self,request):
        print("Starting Download")
        path=calendar.timegm(time.gmtime())
        savepath = '%s/app/%s/' % (settings.MEDIA_ROOT, path)
        self.createPath(savePath=savepath)
        taskid,isFindJson=self.getTaskPathName("download3th")
        apps_download_List = []
        value1=1
        if not isFindJson:
            taskid, isFindJson = self.getTaskPathName("checkv2th")
            getDownloadList= self.getJsonFilePath('checkv2th')
            if getDownloadList is None:
                print("Failed")
            getSearchList = self.readJson(getDownloadList[0])
            for pkgname in getSearchList:
                print(str(value1) + "/Start download:" +pkgname['pkg'])
                app=self.runStepNext(pkgname['pkg'],pkgname['link'],savepath)
                dw_list=self.getDownloadAll(taskid[0], app['pkg'], app['filename'], app['path'], app['ver'])
                apps_download_List.append(dw_list)
                value1 = value1 + 1
        else:
            appfilesJson = self.getJsonFilePath("download3th")
            downloadJsonList = self.readJson(appfilesJson[0])

            for pkgname in downloadJsonList:
                print(str(value1) + "/Start download:" +pkgname['pkg'])
                app = self.runStepNext(pkgname['pkg'],pkgname['link'], savepath)

                dw_list=self.getDownloadAll(taskid[0], pkgname['pkg'], app['filename'], app['path'], app['ver'])
                apps_download_List.append(dw_list)
                value1=value1+1

        try:

            DownloadApp.objects.bulk_create(apps_download_List, ignore_conflicts=True)
            data = {
                'success': True,
                'message': 'Insert data success'
            }
        except Exception:
            data = {
                'success': False,
                'message': 'Insert data Failed'
            }
        return JsonResponse(data)


class DownloadExcelTem(BaseView):
    def get(self,request):
        response = StreamingHttpResponse(self.file_iterator(request))
        response['Content-Type'] = 'application/vnd.ms-excel'
        response['Content-Disposition'] = 'attachment;filename=' + "template.xlsx"

        return response

class ClearDataView(BaseView):
    def get(self, request):

        return self.handle(request)

    def post(self, request):
        return self.handle(request)
    def handle(self, request):
        pkgnames = self.getStrParam(request, 'id')
        print("获取当前包名："+str(len(pkgnames)))
        if len(pkgnames) ==0:
            success = False
            print("至少选择一条")
            message="至少选择一条"
            return JsonResponse({"success": success, "message": message})
        pkgnames = pkgnames.split(',')
        count = 0

        try:
            for pkgname in pkgnames:

                print("当前要删除：" + str(pkgname))
                # BaseApp.objects.all().delete()
                if self.primaryKeyExist(pkgname):

                     BaseApp.objects.filter(pkgname=pkgname.strip()).delete()

                count = count + 1
            message = '%s条记录删除成功！' % count
            success = True
        except Exception as e:
            message = str(e)
            print(e)
            success = False
        return JsonResponse({"success": success, "message": message})

class DelControlDataView(BaseView):
    def get(self, request):
        return self.handle(request)

    def post(self, request):
        return self.handle(request)
    def handle(self, request):
        pkgnames = self.getStrParam(request, 'id')

        if len(pkgnames) ==0:
            success = False
            print("至少选择一条")
            message="至少选择一条"
            return JsonResponse({"success": success, "message": message})
        pkgnames = pkgnames.split(',')
        count = 0

        try:
            for pkgname in pkgnames:

                print("已经删除成功：" +str(count+1)+":" +str(pkgname))
                # BaseApp.objects.all().delete()
                if self.primaryKeyControlExist(pkgname):

                     FavorBaseApp.objects.filter(pkgname=pkgname.strip()).delete()

                count = count + 1
            message = '%s条记录删除成功！' % count
            success = True
        except Exception as e:
            message = str(e)
            print(e)
            success = False
        return JsonResponse({"success": success, "message": message})
class ModifyAppView(BaseView):
    def get(self, request):
        return self.handle(request)

    def post(self, request):
        return self.handle(request)
    def handle(self, request):
        pkgnames = self.getStrParam(request, 'id')
        if len(pkgnames) ==0:
            success = False
            print("至少选择一条")
            message="至少选择一条"
            return JsonResponse({"success": success, "message": message})
        pkgnames = pkgnames.split(',')
        print("获取当前包名：" + str(pkgnames))
        print("当前长度："+str(len(pkgnames)))

        if len(pkgnames)>=2:
            success = False
            print("只能选择一条")
            message = "只能选择一条"
            return JsonResponse({"success": success, "message": message})
        else:
            if len(pkgnames) == 1:
                # 获取第一个包名（因为已经确保只有一个包名）
                pkgname = pkgnames[0]
            #     # 构建修改页面的 URL，将 pkgname 作为参数传递
            #     modify_url = f'/modify/{pkgname}/'
            #     return redirect(modify_url)
            success = True
            message = pkgname
            return JsonResponse({"success": success, "message": message})



class CurrentModifyView(BaseView):
    def get(self,request,pkgname):
        try:
            app=BaseApp.objects.filter(pkgname=pkgname).first()
            context={
                'pkg':pkgname,
                'appName':app.appname,
                'place':app.areaname,
                'status':app.releasestatus,
                'link':app.downloadlink,
                'arch':app.arch
            }
        except Exception as e:
            print(e)
        return render(request,'modify.html',context)
    def post(self,request,pkgname):
        getAppName = self.getStrParam(request, "appname")
        getPlace = self.getStrParam(request, "place")
        getStatus = self.getStrParam(request, "status")
        getLink = self.getStrParam(request, "link")
        getarch = self.getStrParam(request, "arch")
        getNewArch=self.checkArh(getarch)
        getNewLink=self.checkUrlCorrect(pkgname,getLink)
        print(getNewLink)
        try:
           BaseApp.objects.filter(pkgname=pkgname).update(
               appname=getAppName,areaname=getPlace,releasestatus=getStatus,
               downloadlink=getNewLink,arch=getNewArch
                                                          )
        except Exception as e:
            print(e)
        return redirect('/')


class AddControlView(BaseView):
    def get(self,request):
        apps = []
        appBaseInfos = FavorBaseApp.objects.all()
        i = 1
        for app in appBaseInfos:
            appBaseInfo = {
                'num': i,
                'pkgName': app.pkgname,
                'appName': app.appname,
                'place': app.areaname,
                'status': app.releasestatus,
                'link': app.downloadlink,
                'arch': app.arch,
            }

            apps.append(appBaseInfo)
            i = i + 1
        return render(request, "addcontrol.html", {"apps": apps})


class RunTaskView(BaseView):
    isRunValue=False

    def get(self, request):
        try:


            success = True
            message = "启动任务"
            self.isRunValue=True
        except Exception as e:
            print(e)
            # stop_scheduler()  # 如果启动失败，停止任务
            success = False
            message = "启动任务失败"
        return JsonResponse({"success": success, "message": message})
class StopTaskView(BaseView):
    isRunValue=False

    def get(self, request):

        return self.handle(request)

    def post(self, request):
        return self.handle(request)

    def handle(self, request):
        try:


            success=True
            message="停止成功"
            self.isRunValue=True
        except Exception as e:
            success=False
            message="停止失败"
        return JsonResponse({"success": success, "message": message})
class RedirectView(BaseView):
    def get(self, request):
        client_id = '102726023'
        redirect_uri = request.build_absolute_uri('/oauth/callback/')
        authorization_url = (
            f"https://oauth-login.cloud.huawei.com/oauth2/v3/authorize"
            f"?response_type=code"
            f"&client_id={client_id}"
            f"&redirect_uri={redirect_uri}"
        )

        return redirect(authorization_url)
class  OAuthCallbackView(BaseView):
    def get(self, request):
        code = request.GET.get('code')
        if  code:
            client_id = '102726023'
            client_secret = '5e87b5eb0683627914fbd82a65a32f722ff9fec104484ae2f173bba4c809dbb6'
            redirect_uri = request.build_absolute_uri(reverse('oauth_callback'))
            token_url = "https://127.0.0.1:8000/oauth/token"
            data = {
                'grant_type': 'authorization_code',
                'code': code,
                'redirect_uri': redirect_uri,
                'client_id': client_id,
                'client_secret': client_secret,
            }
            response = requests.post(token_url, data=data)
            token_data = response.json()
            # Handle token_data, such as saving to the database or session
            return render(request, 'callback.html', {'token_data': token_data})
        else:
            return render(request, 'error.html', {'error': 'No code provided'})
class TestOAuthCallbackView(BaseView):
    def get(self, request):
        # 模拟一个授权码
        test_code = 'test_authorization_code'
        callback_url = f"{request.build_absolute_uri(reverse('oauth_callback'))}?code={test_code}"
        return redirect(callback_url)