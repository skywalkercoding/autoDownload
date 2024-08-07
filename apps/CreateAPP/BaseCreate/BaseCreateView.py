from django.views.generic import View
from django.conf import settings
from apps.CreateAPP.models import CreateApp
import xlrd3 as xlrd
from datetime import datetime
import calendar,time,requests
from google_play_scraper import app
import json
from openpyxl import Workbook
from requests.packages import urllib3
import apps.CheckAPP.Base.HandleExcel.common as  comm
from apps.UploadAPP.BaseUpView.BaseUploadView import BaseUploadView
import apps.CreateAPP.BaseCreate.commont as crcomm
class ImageFormatException(Exception):
    def __init__(self, code, error, data):
        self.code = code
        self.error = error
        self.data = data
class BaseCreateView(View):
    def primaryKeyExist(self, pkgname):  # 判断主键是否存在
        try:
            CreateApp.objects.get(pkgname=pkgname.strip())

            return True
        except CreateApp.DoesNotExist:
            return False

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

    def displayCreateApp(self):
        num = 1
        ctlist = []
        ctAppAll = CreateApp.objects.all()

        for ct in ctAppAll:
            if ct.Appicon=='':
                icon=''
            else:
                icon=ct.Appicon
            ctinfo = {
                'num': num,
                'pkgName': ct.pkgname,
                'appName': ct.appname,
                'Category': ct.appcategory,
                'Appicon': icon,
                "CreateStatus":ct.CreateStatus,
            }
            num = num + 1
            ctlist.append(ctinfo)
        return ctlist

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
                save_path = '%s/excel/createtmp/%s' % (settings.MEDIA_ROOT, commonFile.name)

                with open(save_path, 'wb') as f:
                    for content in commonFile.chunks():
                        f.write(content)
                fileName = '%s/excel/createtmp/%s' % (settings.MEDIA_ROOT, commonFile.name)
        except Exception as e:
            fileName = '%/excel/createtmp/NoFile.xlsx' % (settings.MEDIA_ROOT)
        return fileName

    def readExcel(self, excel_Path):
        # 打开上传 excel 表格
        try:
            isresult = False
            readboot = xlrd.open_workbook(excel_Path)
            sheet = readboot.sheet_by_index(0)
            nrows = sheet.nrows
            ncols = sheet.ncols
            print(ncols, nrows)
            message = ''
            # sql = "insert into working_hours (jobnum,name,workingtime,category,project,date,createtime) VALUES"
            appList = []
            if ncols < 1:
                isresult = False
                message = "Exel template error"
            else:
                for i in range(1, nrows):

                    row = sheet.row_values(i)
                    packageName = row[0]
                    appName = row[1]
                    appcategory = row[2]
                    Appicon=''



                    date = datetime.now()
                    if self.primaryKeyExist(packageName.strip()):
                        CreateApp.objects.filter(pkgname=packageName.strip()).update(appname=appName, appcategory=appcategory,
                                                                                   Appicon=Appicon, createTime=date)
                        print(str(i) + ":" + packageName + "  modify success")
                    else:
                        appinfo = CreateApp(pkgname=packageName.strip(), appname=appName, appcategory=appcategory,
                                          Appicon=Appicon,createTime=date)
                        appList.append(appinfo)
                        print(str(i) + ":" + packageName + "  upload success")
                    isresult = True
                    message = "upload success"
                CreateApp.objects.bulk_create(appList, ignore_conflicts=True)

        except Exception as e:
            isresult = False
            print(e)
            message = str(e)

        return isresult, message

    def downloadIcon(self,pkgnames):
        basedw = BaseUploadView()
        path = calendar.timegm(time.gmtime())
        imgPath = '%s/img/download/%s/' % (settings.MEDIA_ROOT, path)
        showPath='img/download/%s/' %  path
        basedw.createPath(imgPath)
        if len(pkgnames)!=0:
            num=1
            for pkg in pkgnames:
                if self.primaryKeyExist(pkg):
                   # googleInfoList=self.getGVersion(pkg)
                   googleInfoList=crcomm.getGVersion(pkg)
                   img_path,save_path=basedw.save_image_path(imgPath,showPath,googleInfoList[1],pkg)
                   print(str(num)+":"+googleInfoList[0])
                   print("Img 路径："+img_path)
                   if img_path=='':
                       category = ''

                   else:
                       try:
                          category = googleInfoList[2][0]['name']
                       except Exception as e:
                           category=''


                   print("获取到当前URL:"+img_path)
                   num=num+1
                   date = datetime.now()
                   try:

                       CreateApp.objects.filter(pkgname=pkg).update(
                           appname=googleInfoList[0],appcategory=category, Appicon=img_path,saveiconpath=save_path, createTime=date)
                       status=True
                       message = "download success"
                   except Exception as e:
                       status=False
                       message=str(e)

        else:
            status=False
            message="no choose"

        return status,message






           # basedw.getAllImage(driver,search_url)

    def createExcelrep(self,excelName,applist):
        excelRepPath="%s/excel/reportExcel/%s" %(settings.MEDIA_ROOT,excelName)

        wb=Workbook()
        ws=wb.create_sheet("AppFinfo",0)
        ws.append(['pkgName','appName','category','icon'])
        for app in applist:

            if app['appName']=='':
                icon='No'
            else:
                icon="Yes"
            ws.append(
                [app['pkgName'],app['appName'],
                 app['Category'],icon
                 ]
            )
        wb.save(excelRepPath)
        return  excelRepPath


    def file_iterator(self, request, fExcel_name,chunk_size=1024):
        # fExcel_name = "%s/excel/model/%s" % (settings.MEDIA_ROOT,"template.xlsx")
        print(fExcel_name)
        with open(fExcel_name, "rb") as f:
            while True:
                c = f.read(chunk_size)
                if c:
                    yield c
                else:
                    break
    def checkAppExists(self,pkg):
        apkUrl=comm.MALAYSIA_F_URL_PKG+pkg
        ispkgExists=False
        urllib3.disable_warnings()
        try:
            r = requests.get(apkUrl, verify=False, timeout=5)
            if r.status_code == 200:
                ispkgExists=True
            else:
                ispkgExists=False

        except Exception as e:
            ispkgExists = False
        return ispkgExists

    def uploadIcon(self,uploadList):
        num=1
        getUploadList=[]
        bsupLoad = BaseUploadView()
        browser, isSetChorme = bsupLoad.setChrome("")
        if isSetChorme:
            getList=bsupLoad.loginFproject(browser, comm.CREATE)
            newUploadList=self.getUploadIconInfo(uploadList)

            for pkginfo in newUploadList:
                if self.checkAppExists(pkginfo['pkg']):
                    print(str(num) + "、" + pkginfo['pkg'] + ":已经存在,不需要添加")
                    status="noCreate"
                else:
                    print(str(num) + "、" + pkginfo['pkg'] + ":不存在,开始添加")
                    isCreateStatus=bsupLoad.createAppinputInfo(browser,pkginfo['pkg'],pkginfo['appname'],pkginfo['category'],pkginfo['icon'])
                    if isCreateStatus:
                      bsupLoad.clickAddButton(browser)
                      status = "Created"
                    else:
                        status = "noCreate"
                getUploadinfo={
                    'pkg':pkginfo['pkg'],
                    'status':status
                }
                getUploadList.append(getUploadinfo)
                num=num+1
        else:
            getUploadList=[]
        # browser.quit()
        return getUploadList

    def getUploadIconInfo(self,uploadList):
        if len(uploadList)!=0:
            ctlist = []
            for pkg in uploadList:
                try:
                   ceateList=CreateApp.objects.filter(pkgname=pkg).first()
                   uploadinfo={
                     'pkg':pkg,
                     'appname':ceateList.appname,
                     'category':ceateList.appcategory,
                     'icon':ceateList.saveiconpath
                   }
                   ctlist.append(uploadinfo)
                except CreateApp.DoesNotExist:
                    pass
            return ctlist
    def updateCreateStatus(self,crList):
        if len(crList)!=0:
            for app in crList:
                try:

                    CreateApp.objects.filter(pkgname=app['pkg']).update(CreateStatus=app['status'])
                    status = True
                    message = "insert data success"
                except Exception as e:
                    status = False
                    message = str(e)
            return status,message

    def getGVersion(self,pkg):
        print("Starting  donwload")
        try:
            result = app(
                pkg.strip(),
                lang='en',  # defaults to 'en'
                country='my'  # defaults to 'us'
            )
            json_str = json.dumps(result)
            data2 = json.loads(json_str)
            appName = data2['title']
            icon = data2['icon']
            categories=data2['categories']
            print(icon)
        except Exception as e:
            print(e)
            appName=''
            icon=''
            categories=''
            print(icon)
        return [appName,icon,categories]

#
if __name__=="__main__":
#     url='https://play.google.com/store/apps/details?id=com.astro.sott'
    baseicon=BaseCreateView()
    baseicon.getGVersion('com.airbnb.android')
