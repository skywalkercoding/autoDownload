import time

from django.views.decorators.csrf import csrf_exempt
from django.views.generic import View
from django.conf import settings
from django.db.models import Q
import xlrd3 as xlrd
from datetime import datetime

from openpyxl.workbook import Workbook

from apps.CheckAPP.models import BaseApp,FavorBaseApp
from apps.CreateAPP.models import CheckVersion,FavorVersion
from apps.DownloadAPP.models import DownloadApp
import json
from google_play_scraper import app
import requests
from requests.packages import urllib3
import re,os
from bs4 import BeautifulSoup
import apps.CheckAPP.Base.HandleExcel.common as comm
import random
from datetime import date
from django.core.mail import send_mail, EmailMessage
from email.mime.base import MIMEBase
from email import encoders
import logging
from django.http import JsonResponse, HttpResponse
from google.cloud import firestore
# firestore_client = firestore.Client()
# user_refresh_tokens_ref = firestore_client.collection('userRefreshTokens')
# logger = logging.getLogger(__name__)
class ImageFormatException(Exception):
    def __init__(self, code, error, data):
        self.code = code
        self.error = error
        self.data = data


class BaseView(View):
    def __init__(self,code=None,error=None, state=None,callback_url=None):
        self.currentPage = 1
        self.totalPage = 0
        self.pageSize = 8
        self.recordNumber = 0
        self.startIndex = 0
        self.startPage = 1
        self.endPage = 1
        self.pageList = []
        self.paginator = None
        self.code = code
        self.error = error
        self.state = state
        self.callback_url = callback_url

    def checkCodeStatus(self):
        # 检查是否有错误
        if self.error:
            return JsonResponse({"error": f"Authorization failed: {self.error}"}, status=400)

        # 检查是否有授权码
        if not self.code:
            return JsonResponse({"error": "No authorization code provided."}, status=400)

        # 检查是否有状态
        if not self.state:
            return JsonResponse({"error": "No state parameter provided."}, status=400)

        return None  #

    def getToken_from_huawei(self):
        token_data = {
            'grant_type': 'authorization_code',
            'code': self.code,
            'client_id': comm.client_id,  # 在 comm.py 中定义
            'client_secret': comm.client_secret,  # 在 comm.py 中定义
            'redirect_uri': self.callback_url,  # 确保与华为开发者平台配置的一致
        }

        response = requests.post(comm.token_url, data=token_data)
        token_response_data = response.json()
        if 'access_token' in token_response_data:
            # 获取成功，处理 token
            access_token = token_response_data['access_token']
            refresh_token = token_response_data.get('refresh_token')

            # 根据业务逻辑保存或使用 token
            # 这里我们仅返回 token 作为示例
            return JsonResponse({
                "message": "Authorization successful",
                "access_token": access_token,
                "refresh_token": refresh_token,
                "expires_in": token_response_data['expires_in'],
                "scope": token_response_data['scope'],
                "token_type": token_response_data['token_type'],
                "id_token": token_response_data.get('id_token')
            })
        else:
            # 获取 token 失败，返回错误信息
            return JsonResponse({
                "error": "Failed to retrieve access token.",
                "details": token_response_data
            }, status=400)

    def refreshToken(self, refresh_token):
        refresh_data = {
            'grant_type': 'refresh_token',
            'refresh_token': refresh_token,
            'client_id': comm.client_id,
            'client_secret': comm.client_secret,
        }

        # 向华为服务器请求新的访问令牌
        response = requests.post(comm.token_url, data=refresh_data)
        refresh_response_data = response.json()

        if 'access_token' in refresh_response_data:
            # 刷新成功，返回新的 access_token
            return JsonResponse({
                "message": "Token refreshed successfully",
                "access_token": refresh_response_data['access_token'],
                "refresh_token": refresh_response_data.get('refresh_token'),
                "expires_in": refresh_response_data['expires_in'],
                "scope": refresh_response_data['scope'],
                "token_type": refresh_response_data['token_type']
            })
        else:
            # 刷新失败，返回错误信息
            return JsonResponse({
                "error": "Failed to refresh access token.",
                "details": refresh_response_data
            }, status=400)

    def getCurrentPage(self, request):  # 前台要显示第几页的参数获取
        if request.method == 'GET':
            self.currentPage = request.GET.get('currentPage', 1)
            self.currentPage = int(self.currentPage)
        elif request.method == 'POST':
            self.currentPage = request.POST.get('currentPage', 1)
            self.currentPage = int(self.currentPage)

    def getPageAndSize(self, request):  # 后台要显示第几页和每页多少条数据的参数获取
        if request.method == 'GET':
            self.currentPage = request.GET.get('page', 1)
            self.currentPage = int(self.currentPage)
            self.pageSize = request.GET.get('rows', 5)
            self.pageSize = int(self.pageSize)
        elif request.method == 'POST':
            self.currentPage = request.POST.get('page', 1)
            self.currentPage = int(self.currentPage)
            self.pageSize = request.GET.get('rows', 5)
            self.pageSize = int(self.pageSize)

    def getStrParam(self, request, paramName):
        if request.method == 'GET':

            value = request.GET.get(paramName)
            if value is None:
                value = ''
            return value
        elif request.method == 'POST':

            value = request.POST.get(paramName)

            if value is None:
                value = ''
            return value

    def getIntParam(self, request, paramName):
        if request.method == 'GET':
            value = request.GET.get(paramName)
            if value is None or value == '':
                value = '0'
            return value
        elif request.method == 'POST':
            value = request.POST.get(paramName)
            if value is None or value == '':
                value = '0'
            return value

    def calculatePages(self):
        self.totalPage = self.paginator.num_pages
        self.recordNumber = self.paginator.count
        if self.currentPage > self.totalPage:
            self.currentPage = self.totalPage
        self.startIndex = (self.currentPage - 1) * self.pageSize  # 计算起始序号
        self.startPage = self.currentPage - 5
        self.endPage = self.currentPage + 5
        if self.startPage < 1:
            self.startPage = 1
        if self.endPage > self.totalPage:
            self.endPage = self.totalPage;
        self.pageList = list(range(self.startPage, self.endPage + 1))

    def uploadImageFile(self, request, param):
        try:
            imageFile = request.FILES[param]
            if imageFile.size > 0:
                contentTypes = ['image/jpeg', 'image/png', 'image/gif', 'image/webp']
                if imageFile.content_type not in contentTypes:
                    raise ImageFormatException(1001, '图书格式错误', '请上传图片格式')
                save_path = '%s/img/%s' % (settings.MEDIA_ROOT, imageFile.name)
                with open(save_path, 'wb') as f:
                    for content in imageFile.chunks():
                        f.write(content)
                fileName = 'img/%s' % imageFile.name
        except KeyError as e:  # 如果不传文件就这个异常
            fileName = 'img/NoImage.jpg'
        return fileName

    def uploadCommonFile(self, request, param):
        try:
            commonFile = request.FILES[param]

            if commonFile.size > 0:
                save_path = '%s/excel/tmp/%s' % (settings.MEDIA_ROOT, commonFile.name)

                with open(save_path, 'wb') as f:
                    for content in commonFile.chunks():
                        f.write(content)
                fileName = '%s/excel/tmp/%s' % (settings.MEDIA_ROOT, commonFile.name)
        except Exception as e:
            fileName = '%/excel/tmp/NoFile.xlsx' % (settings.MEDIA_ROOT)
        return fileName

    def checkUrlCorrect(self, pkg, url):
        newUrl = url
        # if pkg not in url:
        #     newUrl = ''
        if url == '':
            newUrl=''
        if not url.endswith('/'):
            newUrl = url + '/'



        return newUrl
    def checkArh(self,arh):
        newArh=arh
        if arh=='':
            newArh=64
        if isinstance(arh, (int, float)):
            newArh=int(float(arh))
            if newArh!=32 and newArh!=64:
                newArh=64
        if not isinstance(arh, (int, float)):
            newArh=64

        return newArh

    def readExcel(self,excel_Path):
        # 打开上传 excel 表格
        try:
           isresult=False
           readboot = xlrd.open_workbook(excel_Path)
           sheet = readboot.sheet_by_index(0)
           nrows = sheet.nrows
           ncols = sheet.ncols
           print(ncols, nrows)
           message=''
        # sql = "insert into working_hours (jobnum,name,workingtime,category,project,date,createtime) VALUES"
           appList=[]
           if ncols<6:
               isresult=False
               message="Exel template error"
           else:
               baseId=1
               for i in range(1, nrows):

                  row = sheet.row_values(i)
                  packageName = row[0]
                  appName = row[1]
                  place = row[2]
                  status = row[3]
                  link = self.checkUrlCorrect(packageName.strip(),row[4])
                  arch = self.checkArh(row[5])

                  date = datetime.now()
                  if self.primaryKeyExist(packageName.strip()):
                      BaseApp.objects.filter(pkgname=packageName.strip()).update(appname=appName, areaname=place,
                                                                               releasestatus=status, downloadlink=link,
                                                                               arch=arch, createTime=date)
                      print(str(i) + ":" + packageName + "  modify success")
                  else:
                      appinfo = BaseApp(pkgname=packageName.strip(), appname=appName, areaname=place,
                                      releasestatus=status, downloadlink=link, arch=arch, createTime=date)
                      appList.append(appinfo)
                      print(str(i)+":"+packageName+"  upload success")
                  baseId=baseId+1
                  isresult = True
                  message="upload success"
               BaseApp.objects.bulk_create(appList, ignore_conflicts=True)

        except Exception as e:
            isresult=False
            print(e)
            message=str(e)

        return isresult,message
    def readControlExcel(self,excel_Path):
        # 打开上传 excel 表格
        try:
           isresult=False
           readboot = xlrd.open_workbook(excel_Path)
           sheet = readboot.sheet_by_index(0)
           nrows = sheet.nrows
           ncols = sheet.ncols
           print(ncols, nrows)
           message=''
        # sql = "insert into working_hours (jobnum,name,workingtime,category,project,date,createtime) VALUES"
           appList=[]
           if ncols<6:
               isresult=False
               message="Exel template error"
           else:
               for i in range(1, nrows):

                  row = sheet.row_values(i)
                  packageName = row[0]
                  appName = row[1]
                  place = row[2]
                  status = row[3]
                  link = self.checkUrlCorrect(packageName.strip(),row[4])
                  arch = self.checkArh(row[5])

                  date = datetime.now()
                  if self.primaryKeyControlExist(packageName.strip()):
                      FavorBaseApp.objects.filter(pkgname=packageName.strip()).update(appname=appName, areaname=place,
                                                                               releasestatus=status, downloadlink=link,
                                                                               arch=arch, createTime=date)
                      print(str(i) + ":" + packageName + "  modify success")
                  else:
                      appinfo = FavorBaseApp(pkgname=packageName.strip(), appname=appName, areaname=place,
                                      releasestatus=status, downloadlink=link, arch=arch, createTime=date)
                      appList.append(appinfo)
                      print(str(i)+":"+packageName+"  upload success")
                  isresult = True
                  message="upload success"
               FavorBaseApp.objects.bulk_create(appList, ignore_conflicts=True)

        except Exception as e:
            isresult=False
            print(e)
            message=str(e)

        return isresult,message
    def checkSearchKey(self,taskid,q):
        appsCheck=CheckVersion.objects.all()
        appCheckList=[]
        pkgList=[]
        if q!='':
            apps = appsCheck.filter(tasknum=taskid,upgradestatus__contains=q.strip())
            appCheckList,pkgList=getCheckShowList(apps)
        else:
            apps = appsCheck.filter(tasknum=taskid)
            appCheckList, pkgList = getCheckShowList(apps)
        return appCheckList,pkgList

    def searchKey(self,q,place,status):
        appsAll=BaseApp.objects.all()
        appsList=[]
        num=1
        if q!='':
            apps=appsAll.filter(Q(pkgname__contains=q.strip())
                                | Q(appname__contains=q.strip()))
            appsList=getShowList(apps)

        if place!='':
            apps=appsAll.filter(areaname__contains=place.strip())
            appsList=getShowList(apps)
        if status!='':
            apps = appsAll.filter(releasestatus__contains=status.strip())
            appsList=getShowList(apps)

        if  place.strip()!='' and status.strip()!='':
            apps = appsAll.filter(
                releasestatus=status,
                areaname=place
            )
            appsList = getShowList(apps)
        if q=='' and place=='' and status=='':
              i=1
              for app in appsAll:
                  appBaseInfo = {
                      'num': i,
                      'pkgName': app.pkgname,
                      'appName': app.appname,
                      'place': app.areaname,
                      'status': app.releasestatus,
                      'link': app.downloadlink,
                  }

                  appsList.append(appBaseInfo)
                  i=i+1
        return appsList
    def getFVesion(self,pkg):
            urllib3.disable_warnings()
            apkUrl=comm.MALAYSIA_F_URL_PKG+pkg.strip()
            try:
                r = requests.get(apkUrl, verify=False, timeout=5)
                if r.status_code == 200:
                    soup = BeautifulSoup(r.text, 'html.parser')
                    packsoup = soup.find_all('p', class_='display-4 sub-app-show d-inline')
                    packinfo = packsoup[0].get_text()
                    infoList = re.split(':|\n', packinfo)
                    return infoList[10]
            except Exception as e:

                return comm.Err3

    def getGVersion(self,pkg):

        try:
            result = app(
                pkg.strip(),
                lang='en',  # defaults to 'en'
                country='my'  # defaults to 'us'
            )
            json_str = json.dumps(result)
            data2 = json.loads(json_str)
            releaseTime = data2['updated']
            getVersion = data2['version']

            dt_object = datetime.fromtimestamp(releaseTime)


            print("谷歌版本：" + str(getVersion)+"--更新时间："+str(dt_object))
            return getVersion
        except Exception as e:
            print("谷歌版本Exception："+str(e))
            return comm.Err3
    def getUpStatus(self,Fv,Gv):
        if comm.Err1 in Fv or  comm.Err3 in Gv:
            return comm.Upgrade1

        else:
            baseview=BaseView()
            result=baseview.compared_version(Fv, Gv)
            return result
    def checkApiUsage(self,url):
        apikey = comm.API_KEY
        isableUsage=False
        params = {
            'url': url,
            'apikey': apikey,
            'autoparse': 'true',
        }
        try:
            response = requests.get(comm.API_URL, params=params)
            if response.status_code == 200:
                isableUsage = True
            if response.status_code == 402:
                isableUsage = False
        except Exception as e:
            print(e)
        return  isableUsage

    def checkApkCombo(self,URL):
        apikey = comm.API_KEY


        params = {
            'url': URL,
            'apikey': apikey,
            'autoparse': 'true',
        }
        try:
            response = requests.get(comm.API_URL, params=params)

            if response.status_code == 200:
                data = json.loads(response.text)
                combV = data[3]["softwareVersion"]

                return combV
            if response.status_code==402:
                data = json.loads(response.text)
                combV=data[3]['title']

                return combV
        except Exception as e:
            print(e)

            return comm.Err4

    def checkApkpureVer(self,URL):
        apikey = comm.API_KEY
        print("run apkpureURL")
        params = {
            'url': URL,
            'apikey': apikey,
            'autoparse': 'true',
        }
        try:
            response = requests.get(comm.API_URL, params=params)

            if response.status_code == 200:
                data = json.loads(response.text)
                apkpureVer = data[0][4]['version']

                return apkpureVer
            if response.status_code==402:
                data = json.loads(response.text)
                combV=data[3]['title']

                return combV
        except Exception as e:
            print(e)

            return comm.Err4
    def checkURLSouce(self,link):
        if link.startswith(comm.APKCOMBO_URL):
            ver=self.checkApkCombo(link)
            return ver
        if link.startswith(comm.APKPURE_URL):
            ver=self.checkApkpureVer(link)
            return ver
    def save_search_as_json(self, jsonfile, json_data):
        try:
            save_path = '%s/savejson/search1th/%s' % (settings.MEDIA_ROOT, jsonfile)
            with open(save_path, 'w') as f:
                f.write(json_data)
            fileName = '%s/savejson/search1th/%s' % (settings.MEDIA_ROOT, jsonfile)
            return fileName
        except Exception as e:
            fileName = '%s/savejson/search1th/%s' % (settings.MEDIA_ROOT, "NoFile.json")
            return fileName
    def save_downlaod_as_json(self, jsonfile, json_data):
        try:
            save_path = '%s/savejson/download3th/%s' % (settings.MEDIA_ROOT, jsonfile)
            with open(save_path, 'w') as f:
                f.write(json_data)
            fileName = '%s/savejson/download3th/%s' % (settings.MEDIA_ROOT, jsonfile)
            return fileName
        except Exception as e:
            fileName = '%s/savejson/download3th/%s' % (settings.MEDIA_ROOT, "NoFile.json")
            return fileName
    def readJson(self, jsonPath):

        with open(jsonPath, 'r') as json_f:
            readJson = json.load(json_f)
        return readJson
    def readTaskJson(self,jsonPath):
        with open(jsonPath, 'r') as json_f:
            readJson = json.load(json_f)

        return readJson
    def generate_task_id(self):
        today = date.today().strftime('%Y%m%d')
        random_num = random.randint(1000, 9999)
        task_id = f"{today}_{random_num}"
        return task_id

    def getTaskPathName(self,path):
        taskpath = '%s/saveJson/%s/' % (settings.MEDIA_ROOT,path)
        print("getTaskPath:"+taskpath)
        findFile = os.listdir(taskpath)
        getNamelist = []
        isFindJson=False
        for i in range(0, len(findFile)):
            if findFile[i].endswith('.json'):
                getName = findFile[i].split('.')[0]
                getNamelist.append(getName)
                isFindJson=True
            else:
                isFindJson=False
        return getNamelist,isFindJson
    def getJsonFilePath(self,path):
        taskpath = '%s/saveJson/%s/' % (settings.MEDIA_ROOT, path)
        findFile = os.listdir(taskpath)
        getNamelist = []
        for i in range(0, len(findFile)):
            if findFile[i].endswith('.json'):
                newPath=taskpath+findFile[i]
                getNamelist.append(newPath)
        return getNamelist

    def getThreePartLink(self,pkg):
        appsAll=BaseApp.objects.all()
        apklinkList=[]
        if pkg is not None:
            apps = appsAll.filter(pkgname__contains=pkg)
            for app in apps:
                apklinkList.append(app.downloadlink)
        return apklinkList

    def delJson_file(self,delpath):
        try:
           nextPath='%s/saveJson/%s/' % (settings.MEDIA_ROOT,delpath)
           for files in os.listdir(nextPath):
              if files.endswith(".json"):
                   os.remove(os.path.join(nextPath,files))
        except Exception as e:
            print(e)

    def getBaseAppAll(self):
        appsList=[]
        appsAll=BaseApp.objects.all()
        for app in appsAll:
            appsinfo={
                'pkg':app.pkgname,
                'link':app.downloadlink
            }
            appsList.append(appsinfo)
        return appsList

    def getDownloadAll(self,taskid,pkgNmae,fileName,path,dv):
        date=datetime.now()
        insertDownload_db = DownloadApp(timecheck=date, tasknum=taskid, pkgname=pkgNmae, apkfilename=fileName,
                                apkfilePath=path,dversion=dv)
        return insertDownload_db

    def check2place_file(self):
        isJsonEx=False
        baseView=BaseView()
        getNamelist,isFindJson=baseView.getTaskPathName("download3th")
        if not isFindJson:
            getNamelist,isFindJson=baseView.getTaskPathName("checkv2th")
            if not isFindJson:
                return comm.Err3
        return getNamelist[0]

    def compared_version(self,Fv, Gv):
        baseview=BaseView()
        listF = str(Fv).split(".")
        listG = str(Gv).split(".")

        if len(listF) > len(listG):
            for i in range(len(listF) - len(listG)):
                listG.append("0")
        elif len(listF) < len(listG):
            for i in range(len(listG) - len(listF)):
                listF.append("0")
        else:
            pass



        for i in range(len(listF)):
                Gn = baseview.check_int(listG[i])
                Fn = baseview.check_int(listF[i])
                if listF[i] == listG[i]:
                    return comm.Upgrade2
                elif Gn == True and Fn == True:
                    if int(listF[i]) < int(listG[i]):
                        return comm.Upgrade1
                        break
                    elif int(listF[i]) > int(listG[i]):
                        return comm.Upgrade2
                        break
                elif listF[i].strip() < listG[i].strip():
                    return comm.Upgrade1
                    break
                elif listF[i].strip() > listG[i].strip():
                    return comm.Upgrade2

                    break
                else:
                    return comm.Upgrade2

    def check_int(self,num):
        if num.strip().isdigit() == True:
            return True

    def file_iterator(self, request, chunk_size=512):
        fExcel_name = "%s/excel/model/%s" % (settings.MEDIA_ROOT,"template.xlsx")
        print(fExcel_name)
        with open(fExcel_name, "rb") as f:
            while True:
                c = f.read(chunk_size)
                if c:
                    yield c
                else:
                    break

    def primaryKeyExist(self, pkgname):  # 判断主键是否存在
        try:
            BaseApp.objects.get(pkgname=pkgname.strip())
            print("正确")
            return True
        except BaseApp.DoesNotExist:
            print("失败" + str(BaseApp.DoesNotExist))
            return False


    def primaryKeyControlExist(self, pkgname):  # 判断主键是否存在
        try:
            FavorBaseApp.objects.get(pkgname=pkgname.strip())
            print("正确")
            return True
        except FavorBaseApp.DoesNotExist:
            print("失败" + str(FavorBaseApp.DoesNotExist))
            return False

    def judgmentStatus(self,pkgname,link):
        Fv = self.getFVesion(pkgname)
        Gv = self.getGVersion(pkgname)
        if comm.Err2 in str(Gv) or Gv is None or comm.Err1 in str(Gv) or comm.Err3 in str(Gv):
            Gv = self.checkURLSouce(link)
        if Fv is None:
            Fv = comm.Err3
        if Gv is None:
            Gv = comm.Err3
        getResult = self.getUpStatus(Fv, Gv)
        if getResult is None:
            getResult = comm.Upgrade1

        return [Fv,Gv,getResult]
    def daily_task_run(self):
        appList = []
        excelList=[]
        num=1
        appsF=FavorBaseApp.objects.all()
        taskid=self.generate_task_id()
        for app in appsF:

            verList=self.judgmentStatus(app.pkgname,app.downloadlink)
            date = datetime.now()
            favorObj=FavorBaseApp.objects.get(pkgname=app.pkgname)
            insertdb = FavorVersion(timecheck=date, tasknum=taskid, appVerObj=favorObj, fversion=verList[0],
                                    googleversion=verList[1], upgradestatus=verList[2])
            controlApp={
                'pkg':app.pkgname,
                'appname':app.appname,
                'place':app.areaname,
                'agstatus':app.releasestatus,
                'link': app.downloadlink,
                'fv':verList[0],
                'gv':verList[1],
                'status':verList[2]


            }
            excelList.append(controlApp)
            appList.append(insertdb)
            print(str(num) + "-" + app.pkgname + ":" + "F:" + verList[0] + "-G:" + verList[1] + "-Status:" + verList[2])
            num=num+1

        try:
            current_time = datetime.now()
            formatted_time = current_time.strftime("%Y%m%d%H%M")
            filename=str(formatted_time)+"_control.xlsx"
            FavorVersion.objects.bulk_create(appList, ignore_conflicts=True)
            execl_path=self.createExcelrepCon(filename,excelList)
            self.send_email_with_attachment(execl_path,filename)
            print("数据插入成功")
        except Exception as e:
            print("数据插入失败："+str(e))


    def send_email_with_attachment(self,excelPath,filename):
        current_time = datetime.now()

        # 格式化输出为"2023-11-14"
        current_data = current_time.strftime("%Y-%m-%d")
        subject = str(current_data)+'F谷歌版本对比'
        message = '执行时间为：'+str(current_data)
        from_email = settings.EMAIL_HOST_USER
        recipient_list = ['zhuwei33@huawei.com','soh.wei.jian@huawei-partners.com','chenpeng285@huawei-partners.com','denis.yu@huawei.com','linzizhong@huawei.com']
        email_message = EmailMessage(subject, message, from_email, recipient_list)
        with open(excelPath, 'rb') as file:
            attachment = MIMEBase('application', 'octet-stream')
            attachment.set_payload(file.read())
            encoders.encode_base64(attachment)
            attachment.add_header('Content-Disposition', f'attachment; filename="{filename}"')
            email_message.attach(attachment)

        # 发送邮件
        email_message.send()
        print("邮件发送成功")

    def createExcelrepCon(self,excelName,applist):
        excelRepPath="%s/excel/reportControl/%s" %(settings.MEDIA_ROOT,excelName)
        wb=Workbook()
        ws=wb.create_sheet("AppFinfo",0)
        ws.append(['pkgName','appNmae','country/area','Ag Status','downloadLink','FVersion','GVersion','UpStatus','DVersion','DownloadName'])
        for app in applist:
            ws.append(
                [app['pkg'],app['appname'],
                 app['place'],app['agstatus'],app['link'],
                 app['fv'],app['gv'],app['status']

                 ]
            )
        wb.save(excelRepPath)
        return  excelRepPath

    # def redirect_view(request):
    #     try:
    #         auth_code = request.GET.get('code')
    #         user_id = request.GET.get('user_id')
    #
    #         logger.info(f'AuthCode {auth_code if auth_code else "not provided"}')
    #         logger.info(f'User id {user_id if user_id else "not provided"}')
    #
    #         if not auth_code:
    #             return JsonResponse(
    #                 {'error_message': 'Invalid authorization code, please reauthorize the Huawei Health again'},
    #                 status=400)
    #
    #         if not user_id:
    #             logger.error('No user query parameter found')
    #             return JsonResponse({'error_message': 'InvalidQueryParamError'}, status=400)
    #
    #         # Fetch access token
    #         token_response = requests.post(
    #             comm.HUAWEI_OAUTH_TOKEN_URL,
    #             data={
    #                 'grant_type': comm.AUTH_TOKEN,
    #                 'code': auth_code,
    #                 'client_id': comm.CLIENT_ID,
    #                 'client_secret': comm.CLIENT_SECRET,
    #                 'redirect_uri': f'{comm.HUAWEI_APP_REDIRECT_URL}?user_id={user_id}'
    #             },
    #             headers={'Content-Type': 'application/x-www-form-urlencoded'}
    #         )
    #         token_response.raise_for_status()
    #         token_data = token_response.json()
    #
    #         # Store tokens in Firestore
    #         user_refresh_tokens_ref.document(user_id).set({
    #             'userId': user_id,
    #             'accessToken': token_data['access_token'],
    #             'refreshToken': token_data['refresh_token']
    #         })
    #
    #         logger.info('Access token response', token_data)
    #
    #         response = HttpResponse("Huawei Health Authorized. Redirecting...")
    #         response.set_cookie('access_token', token_data['access_token'], max_age=3600, httponly=True)
    #         return response
    #     except Exception as e:
    #         logger.error('Error during access token request', exc_info=e)
    #         return JsonResponse({'error_message': 'Unauthorized'}, status=401)
    #
    # @csrf_exempt
    # def refresh_huawei_health_token(request):
    #     if request.method == 'POST':
    #         try:
    #             user_id = request.POST.get('user_id')
    #             access_token = request.headers.get('Authorization')
    #
    #             logger.info(f'Access Token: {access_token if access_token else "not provided"}')
    #             logger.info(f'User id: {user_id if user_id else "not provided"}')
    #
    #             if not user_id:
    #                 logger.error('user_id is not found in request body')
    #                 return JsonResponse({'error_message': 'Invalid user_id in request body'}, status=400)
    #
    #             if not access_token:
    #                 logger.error('Unauthorized user')
    #                 return JsonResponse({'error_message': 'Unauthorized'}, status=401)
    #
    #             snapshot = user_refresh_tokens_ref.document(user_id).get()
    #
    #             if snapshot.exists:
    #                 refresh_token = snapshot.to_dict().get('refreshToken')
    #                 refresh_token_response = requests.post(
    #                     comm.HUAWEI_OAUTH_TOKEN_URL,
    #                     data={
    #                         'grant_type': comm.REFRESH_TOKEN,
    #                         'refresh_token': refresh_token,
    #                         'client_id': comm.CLIENT_ID,
    #                         'client_secret': comm.CLIENT_SECRET,
    #                         'redirect_uri': f'{comm.HUAWEI_APP_REDIRECT_URL}?user_id={user_id}'
    #                     },
    #                     headers={'Content-Type': 'application/x-www-form-urlencoded'}
    #                 )
    #                 refresh_token_response.raise_for_status()
    #                 return JsonResponse(refresh_token_response.json(), status=200)
    #             else:
    #                 return JsonResponse({'error_message': 'Unauthorized'}, status=401)
    #         except Exception as e:
    #             logger.error('Error during refresh token request', exc_info=e)
    #             return JsonResponse({'error_message': 'Unauthorized'}, status=401)
    #     else:
    #         return JsonResponse({'error_message': 'Method not allowed'}, status=405)

def getShowList(apps):
    i=1
    listAll = []
    for app in apps:

       appBaseInfo = {
        'num': i,
        'pkgName': app.pkgname,
        'appName': app.appname,
        'place': app.areaname,
        'status': app.releasestatus,
        'link': app.downloadlink,
    }
       listAll.append(appBaseInfo)
       i=i+1

    return listAll
def getCheckShowList(apps):
    i=1
    listAll = []
    pkgList=[]
    for app in apps:
        appCheckinfo = {
            "num": i,
            "pkgName": app.appVerObj.pkgname,
            "fversion": app.fversion,
            "gversion": app.googleversion,
            "upstatus": app.upgradestatus,

        }

        listAll.append(appCheckinfo)
        pkgList.append(app.appVerObj.pkgname)
        i=i+1

    return listAll,pkgList






