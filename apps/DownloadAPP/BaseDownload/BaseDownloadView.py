import os.path
import shutil
from datetime import datetime
import calendar,time
from django.views.generic import View
import zipfile
from openpyxl import Workbook
import json,random
from appium import webdriver
from pyaxmlparser import APK
from io import BytesIO
from apps.DownloadAPP.models import DownloadApp
from apps.CheckAPP.models import BaseApp
from apps.CreateAPP.models import CheckVersion
import apps.DownloadAPP.BaseDownload.downComm as dwcomm
import apps.CheckAPP.Base.HandleExcel.common as comm
from apps.DownloadAPP.BaseDownload.adbCommand import adbCommmand
from selenium.common.exceptions import NoSuchElementException
from appium.webdriver.common.appiumby import AppiumBy
from django.conf import settings
class ParseApkOnline(View):
    def __init__(self, stream_apk):
        self.stream_apk = stream_apk

    def get_xapk_info(self):
        manifest = zipfile.ZipFile(BytesIO(self.stream_apk.content), 'r').read('manifest.json')
        if manifest:
            load_dict = json.loads(str(manifest, encoding='utf-8'))
            return [load_dict['version_name'], load_dict['version_code']]
        else:
            return None

    def get_apks_info(self):
        meta = zipfile.ZipFile(BytesIO(self.stream_apk.content), 'r').read('meta.sai_v1.json')
        if meta:
            # with open(meta,'r') as load_f:
            load_dict = json.loads(str(meta, encoding='utf-8'))
            return [load_dict['version_name'], load_dict['version_code']]
        else:
            return None

    def get_apk_info(self):
        apk = APK(self.stream_apk.content, raw=True)
        return [apk.version_name, apk.version_code , apk.package]


class ParseApkLocal(View):
    def __init__(self, apk_path):
        self.apk_path = apk_path

    def get_xapk_info(self):
        manifest = zipfile.ZipFile(self.apk_path, 'r').read('manifest.json')
        if manifest:
            load_dict = json.loads(str(manifest, encoding='utf-8'))
            print(load_dict)
            return [load_dict['version_name'], load_dict['version_code'],load_dict['package_name']]
        else:
            return None

    def get_apks_info(self):
        meta = zipfile.ZipFile(BytesIO(self.apk_path), 'r').read('meta.sai_v1.json')
        if meta:
            load_dict = json.loads(str(meta, encoding='utf-8'))
            return [load_dict['version_name'], load_dict['version_code'],load_dict['package_name']]
        else:
            return None

    def get_apk_info(self):
        apk = APK(self.apk_path)
        return [apk.version_name, apk.version_code,apk.package]


class BaseDwloadView(View):
    def displayDownload(self, taskid):
        num = 1
        dwlist = []
        dwloadAll = DownloadApp.objects.all()
        apps = dwloadAll.filter(tasknum__contains=taskid)
        for dw in apps:
            dwinfo = {
                'num': num,
                'pkgName': dw.pkgname,
                'dversion': dw.dversion,
                'upstatus': dw.uploadStatus,
                'apkpath': dw.apkfilename,
                'instatus':dw.installStatus,
            }
            num = num + 1
            dwlist.append(dwinfo)
        return dwlist

    @property
    def connectAppium(self):
            try:
                caps = {}
                caps['platformName'] = dwcomm.DEVICES_TYPE
                caps["appium:platformVersion"] = dwcomm.DEVICES_VER
                caps["appium:deviceName"] = dwcomm.CONNECT_DEVICES
                caps["appium:newCommandTimeout"] = 3600

                driver = webdriver.Remote(dwcomm.APPIUM_CONNECT_URL, caps)
                driver.implicitly_wait(10)

            except Exception as e:
                print(e)
                driver=dwcomm.DRIVER_FAILE

            return driver


    def installStart(self, taskid):
        dwloadAll = DownloadApp.objects.all()
        apps = dwloadAll.filter(tasknum__contains=taskid)
        versionList = []
        driver=self.connectAppium()
        print(driver)
        if driver==dwcomm.DRIVER_FAILE:
            data={
                "success":False,
                "message":"Connect Appium failed"
            }
            versionList.append(data)
        else:

            for install in apps:
                 if install.apkfilename == comm.APK_FAILED:
                     data = {
                         "pkg":install.pkgname,
                         "success": False,
                         "message": "No Find APK"
                     }
                     versionList.append(data)
                 else:
                     getInstallPkg = install.pkgname
                     adbcomm = adbCommmand(dwcomm.CONNECT_DEVICES, install.apkfilePath, None)
                     getInstallRes=adbcomm.install_apk()
                     driver.implicitly_wait(5)
                     self.onClickButton(driver)
                     driver.implicitly_wait(3)
                     self.onClickButton(driver)
                     data = {
                         "pkg":getInstallPkg,
                         "success": True,
                         "message": "Success"
                          }
                     versionList.append(data)
        return versionList

    def delpkg(self,request,taskid):
        delList=[]

        dwloadAll = DownloadApp.objects.all()
        apps = dwloadAll.filter(tasknum__contains=taskid)
        for app in apps:

            delcmd=adbCommmand(None,None,app.pkgname)
            getRes=delcmd.delpkgcmd()
            if getRes:
                delValue='Del Success'
            else:
                delValue="Del Failed"
            delinfo={
                'pkg':app.pkgname,
                'res':delValue
            }
            delList.append(delinfo)
        return delList
    def updateVersion(self,taskid,pkg,ver):
        dwloadAll = DownloadApp.objects.all()
        versionAll=dwloadAll.filter(tasknum=taskid,pkgname=pkg)
        for ver in versionAll:
            ver.dversion=ver

    def onClickButton(self, driver):
        isClick = False
        if driver!=dwcomm.DRIVER_FAILE:
           try:
               driver.find_element(AppiumBy.ID,dwcomm.INSTALL_BUTTON_ID).click()

               isClick = True
           except NoSuchElementException:
               print("没发现按钮")

        return isClick

    def checkInstallVer(self, filesname, installPath):
        getInstallList = []
        parseApkLocal = ParseApkLocal(installPath)
        if filesname.endswith(".apk"):
            getInstallList = parseApkLocal.get_apk_info()
        if filesname.endswith(".xapk"):
            getInstallList = parseApkLocal.get_xapk_info()
        if filesname.endswith(".apks"):
            getInstallList = parseApkLocal.get_apks_info()
        return getInstallList

    def checkPhoneConnect(self):
        isConnect=False
        usbCheck=adbCommmand()
        getRes=usbCheck.checkConnect()
        if dwcomm.CONNECT_DEVICES in getRes:
            isConnect = True
        return isConnect

    def file_iterator(self,request,file_name, chunk_size=512):

        with open(file_name, "rb") as f:
            while True:
                c = f.read(chunk_size)
                if c:
                    yield c
                else:
                    break


    def readAllPkgData(self,taskid):
        excelList=[]
        basePkgAll=BaseApp.objects.all()
        num=1
        for app in basePkgAll:
            check = CheckVersion.objects.filter(tasknum=taskid, appVerObj=app)
            down = DownloadApp.objects.filter(tasknum=taskid, pkgname=app.pkgname)
            if check.exists():
                fv=check[0].fversion
                gv=check[0].googleversion
                status=check[0].upgradestatus

            else:
                fv=''
                gv=''
                status=''
            if down.exists():
                dv=down[0].dversion
                filename=down[0].apkfilename
            else:
                dv=''
                filename=''

            excelinfo={
                     'num':num,
                    'pkg':app.pkgname,
                    'appname':app.appname,
                    'place':app.areaname,
                    'agstatus':app.releasestatus,
                    'link':app.downloadlink,
                    'fv':fv,
                    'gv':gv,
                    'status':status,
                    'dv':dv,
                    'filename':filename


                }
            excelList.append(excelinfo)
            num=num+1
        return excelList

    def createExcelrep(self,excelName,applist):
        excelRepPath="%s/excel/reportExcel/%s" %(settings.MEDIA_ROOT,excelName)
        wb=Workbook()
        ws=wb.create_sheet("AppFinfo",0)
        ws.append(['pkgName','appNmae','country/area','Ag Status','downloadLink','FVersion','GVersion','UpStatus','DVersion','DownloadName'])
        for app in applist:
            ws.append(
                [app['pkg'],app['appname'],
                 app['place'],app['agstatus'],app['link'],
                 app['fv'],app['gv'],app['status'],app['dv'],
                 app['filename']

                 ]
            )
        wb.save(excelRepPath)
        return  excelRepPath

    def scanPathApp(self,path):
        applist=[]
        if os.path.exists(path):
            appNames=os.listdir(path)
            timepath = calendar.timegm(time.gmtime())
            savepath = '%s/app/%s/' % (settings.MEDIA_ROOT, timepath)
            self.createPath(savepath)
            for apk in appNames:

                srcPath=path+apk
                parselocal = ParseApkLocal(srcPath)

                if apk.endswith(".apk"):
                    print("uploading apk:"+apk)
                    getappList=parselocal.get_apk_info()
                    dstPath=savepath+apk
                    shutil.move(srcPath , dstPath)
                    appinfo = {
                        'pkg': getappList[2],
                        'apkfile': apk,
                        'dv': getappList[0],
                        'path':dstPath
                    }

                    applist.append(appinfo)
                if apk.endswith(".xapk"):
                    print("uploading apk:"+apk)
                    getappList = parselocal.get_xapk_info()
                    dstPath = savepath + apk
                    shutil.move(srcPath, dstPath)
                    appinfo = {
                        'pkg': getappList[2],
                        'apkfile': apk,
                        'dv': getappList[0],
                        'path': dstPath
                    }

                    applist.append(appinfo)
                if apk.endswith(".apks"):
                    print("uploading apk:"+apk)
                    getappList = parselocal.get_apks_info()
                    dstPath = savepath + apk
                    shutil.move(srcPath, dstPath)
                    appinfo = {
                        'pkg': getappList[2],
                        'apkfile': apk,
                        'dv': getappList[0],
                        'path': dstPath

                    }
                    applist.append(appinfo)

            return applist

    def insertApkInfo(self,taskid,getList):
        if getList is None:
            return False
        appdList = []
        for pkg  in getList:
            date = datetime.now()
            userapps=DownloadApp.objects.filter(tasknum=taskid,pkgname=pkg['pkg'])
            if userapps.exists():
                userapps.update(timecheck=date,apkfilename=pkg['apkfile'],apkfilePath=pkg['path'],dversion=pkg['dv'])
            else:
                insertDownload_db = DownloadApp(timecheck=date, tasknum=taskid, pkgname=pkg['pkg'], apkfilename=pkg['apkfile'],
                                        apkfilePath=pkg['path'],dversion=pkg['dv'])
                appdList.append(insertDownload_db)

        DownloadApp.objects.bulk_create(appdList, ignore_conflicts=True)
        return True

    def createPath(self, savePath):
        isExists = os.path.exists(savePath)
        if not isExists:
            os.makedirs(savePath)
            print("创建成功")
        else:
            print("路径已建成存在")