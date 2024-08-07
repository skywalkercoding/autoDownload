import subprocess
import time

import apps.CheckAPP.Base.HandleExcel.common as comm
from django.views.generic import View
from bs4 import BeautifulSoup
from urllib.parse import urlparse
from urllib.parse import parse_qs
from selenium import webdriver
from django.conf import settings
import re,os,requests
from urllib.parse import unquote
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from clint.textui import progress
from apps.DownloadAPP.BaseDownload.BaseDownloadView import ParseApkLocal
from apps.UploadAPP.BaseUpView.BaseUploadView import BaseUploadView
class DownloadView(View):
    def __init__(self):
        self.currentPage = 1
        self.totalPage = 0
        self.pageSize = 8
        self.recordNumber = 0
        self.startIndex = 0
        self.startPage = 1
        self.endPage = 1
        self.pageList = []
        self.paginator = None


    def connectWithCaptcha(self,link):
        print("获取当前下载地址："+link)
        # 运行Java程序并设置类路径
        isFindDownloading=False
        jarPath=settings.JAVA_PATH+'/CheckAPP/Base/JavaDown/StartDownload.jar'
        libPath=settings.JAVA_PATH+'/CheckAPP/Base/JavaDown/lib/*'
        print(jarPath)
        # java_classpath = "StartDownload.jar;.;lib/*"
        java_classpath = jarPath+";.;"+ libPath
        java_command = f"java -cp {java_classpath} com.StartDownload {comm.API_KEY} {link}"
        try:
             # 调用Java程序
             result = subprocess.run(java_command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)

             if result.returncode == 0:
        # Java 程序正常运行，获取结果
                 java_output = result.stdout.strip()
                 isFindDownloading=True
                 # print("Java程序输出：", java_output)
                 return java_output,isFindDownloading
             else:
                # Java 程序运行出错，获取错误信息
                 java_error = result.stderr.strip()
                 isFindDownloading = False
                 print("Java程序错误：", java_error)
                 return java_error,isFindDownloading
        except subprocess.CalledProcessError as e:
                 print("调用Java程序时出错：", e)
                 return e,isFindDownloading

    def connectWithCaptchaApkpure(self,url):
        try:
            params = {
                'url': url,
                'apikey': comm.API_KEY,

            }
            response = requests.get(comm.API_URL, params=params)
        except  Exception:
            response=''
        return response

    def getApkpureDownLink(self, reslut):
        linkList = []
        if isinstance(reslut, tuple):
            # Assuming that the first element of the tuple is the HTML content
            html_content = reslut[0]
            if isinstance(html_content, bytes):
                html_content = html_content.decode('utf-8')
        else:
            # If reslut is not a tuple, assume it is already a string
            html_content = reslut
        soup = BeautifulSoup(html_content, 'html.parser')
        ul_tag = soup.find('a', class_='download-start-btn')
        if ul_tag:
            href_value = ul_tag.get('href')
            linkList.append(href_value)
        else:
            print("Anchor tag not found.")
            linkList.append(comm.Err3)

        return linkList
    def getApkComboDownLink(self,reslut):

        linkList=[]
        if isinstance(reslut, tuple):
            # Assuming that the first element of the tuple is the HTML content
            html_content = reslut[0]
            if isinstance(html_content, bytes):
                html_content = html_content.decode('utf-8')
        else:
            # If reslut is not a tuple, assume it is already a string
            html_content = reslut

        soup = BeautifulSoup(html_content, 'html.parser')
        ul_tag = soup.find('ul', class_='file-list')
        if ul_tag is None:
            return comm.Err3
        all_links = ul_tag.find_all('a')
        for link in all_links:
            href_value = link.get('href')
            linkList.append(href_value)

        return linkList
    def getUrlparse(self,link):

        if link is None:
            return comm.Err4
        parsed_url = urlparse(link)
        scheme_https=parsed_url.scheme
        if scheme_https=="https":

           query_params = parse_qs(parsed_url.query)
           file_name = parsed_url.path.split('/')[-1]
           if comm.hreflink in file_name:
               file_name=re.sub(r'%20',' ',file_name)
           pkg_name = parsed_url.path.split('/')[1]
           downloadLink=link+"&fp="+comm.URL_FP+"&ip="+comm.URL_IP

        else:
            print("Link error")
            file_name="NoFile.apk"
            pkg_name='com.null'
            downloadLink=''
        return file_name, pkg_name, downloadLink
    def getApkPureUrl(self,link):
        if link is None:
            return comm.Err4

        parsed_url = urlparse(link)
        scheme_https = parsed_url.scheme
        if scheme_https == "https":
            pkg_name = parsed_url.path.split('/')[-1]
            file_name=pkg_name+"_latest"
            downloadLink=link
        else:
            print("Link error")
            file_name=comm.APK_FAILED
            pkg_name=comm.PKG_FAILED
            downloadLink=''
        return file_name, pkg_name, downloadLink


    def setChrome(self,save_path):
        chrome_options = webdriver.ChromeOptions()
        d = webdriver.DesiredCapabilities.CHROME
        print("Save APK Path:"+save_path)
        prefs = {'profile.default_content_settings.popups': 0 , "download.default_directory": save_path}
        chrome_options.add_experimental_option("prefs", prefs)
        desired_capabilities = DesiredCapabilities.CHROME.copy()
        desired_capabilities['goog:chromeOptions'] = chrome_options.to_capabilities()
        # 设置 ChromeDriver 路径
        chrome_driver_path = Service(ChromeDriverManager(version=comm.DRIVER_MANAGER_V).install())  # 请根据您的实际安装路径修改
        browser=webdriver.Chrome(service=chrome_driver_path, options=chrome_options,desired_capabilities=d)
        # 设置 DesiredCapabilities
        browser.implicitly_wait(30)
        return browser
    def createPath(self,savePath):
        isExists=os.path.exists(savePath)
        if not isExists:
            os.makedirs(savePath)
            print("创建成功")
        else:
            print("路径已建成存在")
    def checkURLSouce(self,link):
        isAPKCOMBO=False
        if link.startswith(comm.APKCOMBO_URL):
            isAPKCOMBO = True
            return isAPKCOMBO
        if link.startswith(comm.APKPURE_URL):
            return isAPKCOMBO



    def runDownload(self,url,pkg):

        startdownload = DownloadView()
        if startdownload.checkURLSouce(url):
            newApkCombo_url=url+comm.APKCOMBO_DOWNLOAD
            res,isFindDownloading= startdownload.connectWithCaptcha(newApkCombo_url)
            if isFindDownloading:
                  link = startdownload.getApkComboDownLink(res)

                  file_name, pkg_name, downloadLink = startdownload.getUrlparse(link[0])

            else:
                file_name=''
                pkg_name=''
                downloadLink=''

        else:
            apkpur='https://d.apkpure.com/b/APK/{}?version=latest'.format(pkg)
            newApkDownload_ulr=url+comm.APKPURE_DOWNLOAD
            # baseUp=BaseUploadView()
            # driver,isTure=baseUp.setChrome("D:/")
            # baseUp.clickAiButton(driver,apkpur)
            # time.sleep(20)
            res ,isFindDownloading= startdownload.connectWithCaptcha(newApkDownload_ulr)
            if isFindDownloading:
                 # print("resapkpure:"+res)
                 linkList=startdownload.getApkpureDownLink(res)
                 file_name, pkg_name, downloadLink=startdownload.getApkPureUrl(linkList[0])
                 if pkg_name not in file_name:
                     file_name=pkg_name

            else:
                file_name = ''
                pkg_name = ''
                downloadLink = ''
        newSaveinfo = {
            'pkg': pkg_name,
            'filename': file_name,
            'link': downloadLink
        }
        print("获取下载链接：（" + "pkg:" + str(pkg_name) + "-Dlink:" + str(downloadLink) + ")")
        return newSaveinfo
    def startDownload(self,app,savepath):


        apkpure_dlink='https://d.apkpure.com/b/APK/'
        try:
            if app['link'].startswith(apkpure_dlink):
                res = self.connectWithCaptchaApkpure(app['link'])
            else:
                res = requests.get(app['link'], stream=True)

            gettype = self.getFilesType(res)
            file_name = os.path.join(savepath, app['pkg'] + gettype)
            with open(file_name, 'wb') as f:
                for chunk in res.iter_content(1024):
                    f.write(chunk)
            file_save_name = file_name
            file_new_name = app['pkg'] + gettype
        except Exception as e:
            file_save_name = savepath + "NoFile.apk"
            file_new_name = "NoFile.apk"

        newSaveinfo={
                'pkg':app['pkg'],
                'filename':file_new_name,
                'path':file_save_name
            }
        print("开始下载安装包：（"+"pkg:"+str(app['pkg'])+"-path:"+str(file_save_name)+")")


        return newSaveinfo

    def getApkVersion(self, app,savepath):
        failedFile = "NoFile.apk"
        if app["filename"] == failedFile:
            version = ""
        else:
            try:
                parseLocal = ParseApkLocal(app['path'])
                if app['filename'].endswith(".apk"):
                    getAPkinfo = parseLocal.get_apk_info()
                if app['filename'].endswith('.xapk'):
                    getAPkinfo = parseLocal.get_xapk_info()
                if app['filename'].endswith('.apks'):
                    getAPkinfo = parseLocal.get_apks_info()
                version = getAPkinfo[0]
            except Exception:
                version=""
        file_extension = app['filename'].split('.')[-1]
        newFile_name = str(app['pkg']) + "_" + str(version) + "_fibonas." + file_extension
        new_save_path = savepath + newFile_name
        newSaveverinfo = {
            'pkg': app['pkg'],
            'filename': newFile_name,
            'path': new_save_path,
            'ver': version

        }

        print("开始获取版本：（" + "pkg:" + str(app['pkg']) + "-ver:" + str(version) + "-Newpath:" + str(
            new_save_path) + ")")
        return newSaveverinfo
    def getFilesType(self,res):
        filetype=''
        try:
            content_disposition= res.headers.get('Content-Disposition', None)
            filename_match = re.search(r'filename="(.+)"', content_disposition)
            if filename_match:
                filename = unquote(filename_match.group(1))
                file_extension = filename.split('.')[-1]
                filetype="."+file_extension
        except Exception:
            filetype='.apk'
        return filetype

    def runStepNext(self,pkg,url,savePath):
       appStep1= self.runDownload(url,pkg)
       appStep2=self.startDownload(appStep1,savePath)
       appStep3=self.getApkVersion(appStep2,savePath)
       return appStep3






    def openDownLink(self,downlink,savepath):
        r=requests.get(downlink,stream=True)
        total_length=int(r.headers.get('content-length'))
        with open(savepath,'wb') as f:
           for ch in progress.bar(r.iter_content(chunk_size=2391975),expected_size=(total_length/1024)+1):
               if ch:
                   f.write(ch)
        f.close()
        return True
    def openDownPoll(self,downlink,savepath):
        try:
            r=requests.get(downlink,stream=True)
            print(r.content)
            with open(savepath,'wb') as f:
                for ch in r:
                    f.write(ch)
                f.close()
            return True
        except Exception as e:
            print(e)
            return False

# if __name__ == "__main__":
#     url="https://apkpure.com/cn/google-chrome-fast-secure/com.android.chrome/"
#
#     startdownload=DownloadView()
#     startdownload.runDownload(url)
    # driver = startdownload.setChrome("D:\\Download")
    # res=startdownload.connectWithCaptcha(url)
    # link=startdownload.getApkComboDownLink(res)
    # print(link[0])
    # file_name,pkg_name,downloadLink=startdownload.getUrlparse(link[0])
    # if downloadLink!='':
    #    driver.get(downloadLink)
    #    driver.close()

