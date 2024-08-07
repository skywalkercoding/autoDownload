from datetime import datetime
import time,re
from requests.packages import urllib3
import requests
from apps.DownloadAPP.models import DownloadApp
from apps.CheckAPP.models import BaseApp
import lxml.html
from django.views.generic import View
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from webdriver_manager.chrome import ChromeDriverManager
import apps.CheckAPP.Base.HandleExcel.common as comm
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.select import Select
import calendar,os
from PIL import Image
from django.conf import settings
class BaseUploadView(View):

    def setChrome(self, save_path):
        isSetChrome=False
        try:
            chrome_options = webdriver.ChromeOptions()
            prefs = {'profile.default_content_settings.popups': 0, "download.default_directory": save_path}
            chrome_options.add_experimental_option("prefs", prefs)
            desired_capabilities = DesiredCapabilities.CHROME.copy()
            desired_capabilities['goog:chromeOptions'] = chrome_options.to_capabilities()
        # 设置 ChromeDriver 路径
            chrome_driver_path = Service(ChromeDriverManager(driver_version=comm.CHROME_VERSION_MANAGER).install())  # 请根据您的实际安装路径修改
            browser = webdriver.Chrome(service=chrome_driver_path, options=chrome_options)
        # 设置 DesiredCapabilities
            browser.implicitly_wait(30)
            browser.maximize_window()
            isSetChrome=True

        except Exception as e:
            print(e)
            browser=comm.START_BROWER_FAILED
        return browser, isSetChrome

    # //*[@id="page-header"]/div/a[2]  点击登录
    # //*[@id="login"]/div/div/form/div[1]/input
    # //*[@id="login"]/div/div/form/div[2]/input
    # //*[@id="login"]/div/div/form/div[4]/button

    # //*[@id="page-wrap"]/div/div/div/form/div/div[1]/input version
    # //*[@id="status"]
    def loginFproject(self,browser,value):
        add_app_xpath='//*[@id="page-wrap"]/div/div[1]/div[2]/a[1]'
        try:
            wait = WebDriverWait(browser, 20)
            browser.get(comm.F_LOGIN_URL)
            time.sleep(5)
            wait.until(EC.visibility_of_element_located((By.XPATH, comm.ACCOUNT_XPATH)))
            wait.until(EC.visibility_of_element_located((By.XPATH, comm.PASSWORD_XPATH)))
            username_input = browser.find_element(By.XPATH, comm.ACCOUNT_XPATH)
            password_input = browser.find_element(By.XPATH, comm.PASSWORD_XPATH)
            login_button = browser.find_element(By.XPATH, comm.LOGIN_BUTTON_XPATH)
            username_input.send_keys(comm.ACCOUNT)
            password_input.send_keys(comm.PASSWORD)
            login_button.click()
            time.sleep(5)
            browser.switch_to.window(browser.window_handles[-1])

            wait.until(EC.visibility_of_element_located((By.XPATH, comm.Application_button)))
            if value==comm.ADD:
                 wait.until(EC.element_to_be_clickable((By.XPATH,comm.Application_button))).click()
            if value==comm.CREATE:
                 wait.until(EC.element_to_be_clickable((By.XPATH, add_app_xpath))).click()
            return [True,"Login Success"]
        except Exception as e:
            print(e)
            return [False,e]




        # //*[@id="page-header"]/div/a[1]  应用按钮
        # //*[@id="page-header"]/div/a[1]
        # //*[@id="search"]    搜索应用
        # //*[@id="page-wrap"]/div/div[2]/div/div/div/div/div/a[1] more app
        # //*[@id="page-wrap"]/div/div[4]/div[2]/div[1]/form/input[3]
    # //*[@id="page-wrap"]/div/div[2]/div/div[1]/div/div/div/a[1]
    # //*[@id="page-header"]/div/a[1]
    # //*[@id="page-header"]/div/a[1]
    # //*[@id="search"]
    def searchApp(self,browser,pkg,arh,ver,choose,path):
        isSearch = False
        try:
           arh=int(float(arh))
           if arh!=32 or arh!=64:
              arh=64
        except Exception:
            arh=64
        try:
            wait = WebDriverWait(browser, 20)
            search_xpath='//*[@id="search"]'
            search_button='//*[@id="page-wrap"]/div/form/div/div[2]/button'
            more_button_xpath = '//*[@id="page-wrap"]/div/div[2]/div/div/div/div/div/a[1]'
            button32_xpath = '//*[@id="page-wrap"]/div/div[4]/div[2]/div[1]/form/input[3]'
            button64_xpath = '//*[@id="page-wrap"]/div/div[4]/div[2]/div[2]/form/input[3]'

            # //*[@id="page-wrap"]/div/div[2]/div[1]/p[1]

            wait.until(EC.visibility_of_element_located((By.XPATH, search_xpath)))

            # wait.until(EC.visibility_of_element_located((By.XPATH, '//*[@id="page-wrap"]/div/form/div/div[2]/button')))
            wait.until(EC.element_to_be_clickable((By.XPATH,search_xpath))).send_keys(pkg)
            wait.until(EC.element_to_be_clickable((By.XPATH,search_button))).click()
            wait.until(EC.visibility_of_element_located((By.XPATH, more_button_xpath)))
            wait.until(EC.element_to_be_clickable((By.XPATH, more_button_xpath))).click()
            browser.switch_to.window(browser.window_handles[-1])
            getPkgList=self.getFChromeUrl(browser)

            if pkg in getPkgList[0]:
                print(pkg+":Search result correct")
                time.sleep(5)
                wait.until(EC.visibility_of_element_located((By.XPATH, button32_xpath)))
                wait.until(EC.visibility_of_element_located((By.XPATH, button64_xpath)))
                if arh==32:
                    wait.until(EC.element_to_be_clickable((By.XPATH, button32_xpath))).click()
                    time.sleep(5)
                if arh==64:
                    wait.until(EC.element_to_be_clickable((By.XPATH, button64_xpath))).click()
                    time.sleep(5)

                message="Search result correct "
                isUploadApp=self.createUploadapk(browser,ver,choose,path)
                if isUploadApp:
                    message="Upload app success"
                    isSearch = True
            else:
                wait.until(EC.element_to_be_clickable((By.XPATH, comm.Application_button))).click()
                message=pkg+":Upload success"
            return message, isSearch
        except Exception as e:
            print(e)
            return e,isSearch

    def createUploadapk(self,browser,version,choose,apkpath):
        isUploadApp=False
        input_version_xapk='//*[@id="page-wrap"]/div/div/div/form/div/div[1]/input'
        select_xpath='//*[@id="status"]'
        des_xpath='//*[@id="page-wrap"]/div/div/div/form/div/div[3]/textarea'
        upload_apk_xpath='//*[@id="inputGroupFile01"]'
        upload_button_xpath='//*[@id="page-wrap"]/div/div/div/form/div/input[3]'
        # //*[@id="page-wrap"]/div/div/div/form/div/input[3]

        current=datetime.now()
        try:
            wait = WebDriverWait(browser, 20)
            wait.until(EC.visibility_of_element_located((By.XPATH, input_version_xapk)))
            time.sleep(5)
            wait.until(EC.element_to_be_clickable((By.XPATH, input_version_xapk))).send_keys(version)
            status_button=browser.find_element(By.XPATH,select_xpath)
            Select(status_button).select_by_index(choose)
            wait.until(EC.element_to_be_clickable((By.XPATH, des_xpath))).send_keys(str(current))
            wait.until(EC.element_to_be_clickable((By.XPATH, upload_apk_xpath))).send_keys(apkpath)
            wait.until(EC.element_to_be_clickable((By.XPATH, upload_button_xpath))).click()
            time.sleep(20)
            wait.until(EC.visibility_of_element_located((By.XPATH, comm.Application_button)))
            wait.until(EC.element_to_be_clickable((By.XPATH, comm.Application_button))).click()
            browser.switch_to.window(browser.window_handles[-1])
            isUploadApp=True
        except Exception as e:
            print(e)
        return isUploadApp


    def createAppinputInfo(self,browser,pkg,appName,category,icon_path):
        isCreateStatus=False
        pkgName_xpath='//*[@id="page-wrap"]/div/div/div/form/div/div[1]/input'
        appName_xpath='//*[@id="page-wrap"]/div/div/div/form/div/div[2]/input'
        choose_category_xpath='//*[@id="appCategory"]'
        icon_xpath='//*[@id="inputGroupFile01"]'  #//*[@id="inputGroupFile01"]
        # icon_xpath='//*[@id="page-wrap"]/div/div/div/form/div/div[14]/div[2]/label'
        icon_ID='inputGroupFile01'
        create_sure_button_xpath='//*[@id="page-wrap"]/div/div/div/form/div/input'
        try:
            wait = WebDriverWait(browser, 20)
            wait.until(EC.visibility_of_element_located((By.XPATH, pkgName_xpath)))
            wait.until(EC.element_to_be_clickable((By.XPATH, pkgName_xpath))).send_keys(pkg)
            wait.until(EC.element_to_be_clickable((By.XPATH, appName_xpath))).send_keys(appName)
            wait.until(EC.visibility_of_element_located((By.XPATH, choose_category_xpath)))
            category_elements = browser.find_element(By.XPATH, choose_category_xpath)
            select = Select(category_elements)
            # 获取所有选项的文本内容
            all_options = [option.text for option in select.options]
            if category in all_options:
                select.select_by_visible_text(category)
            else:
                select.select_by_value(3)
            print("开始找图片xpath")

            # upload_icon = browser.find_element(By.ID, icon_ID)
            print(str(icon_path))

            upload_icon = wait.until(EC.presence_of_element_located((By.ID, icon_ID)))

            upload_icon.send_keys(icon_path)
            print("上传成功")
            time.sleep(10)
            wait.until(EC.element_to_be_clickable((By.XPATH, create_sure_button_xpath))).click()
            browser.switch_to.window(browser.window_handles[-1])

            isCreateStatus=True

        except Exception as e:
            print(e)
        return isCreateStatus
    def clickAddButton(self,browser):
        isSkipAdd=False
        skip_add_button_xpath='//*[@id="page-header"]/div/a[2]'
        add_create_xpath='//*[@id="page-wrap"]/div/div[1]/div[2]/a[1]'
        try:
           wait = WebDriverWait(browser, 20)
           wait.until(EC.visibility_of_element_located((By.XPATH, skip_add_button_xpath)))
           wait.until(EC.element_to_be_clickable((By.XPATH, skip_add_button_xpath))).click() #点击add跳转add节目
           browser.switch_to.window(browser.window_handles[-1])
           time.sleep(1)
           wait.until(EC.visibility_of_element_located((By.XPATH, add_create_xpath)))
           wait.until(EC.element_to_be_clickable((By.XPATH, add_create_xpath))).click()  # 点击add跳转add节目
           time.sleep(1)
           browser.switch_to.window(browser.window_handles[-1])
           isSkipAdd=True
        except Exception as e:
            print(e)
        return isSkipAdd
    def getFChromeUrl(self,browser):
        # //*[@id="page-wrap"]/div/div[2]/div[1]/p[1]
        html_source=browser.page_source
        htmlvalue=lxml.html.fromstring(html_source)
        getChormePkg_xpath = '//*[@id="page-wrap"]/div/div[2]/div[1]/p[1]'
        itemsPkg = htmlvalue.xpath('//*[@id="page-wrap"]/div/div[2]/div[1]/p[1]//text()')
        itemsVer=htmlvalue.xpath('//*[@id="page-wrap"]/div/div[2]/div[1]/h5/span//text()')
        # 正则 匹配以下内容 \s+ 首空格 \s+$ 尾空格 \n 换行
        pattern = re.compile("^\s+|\s+$|\n")
        clause_pkg = ""
        clause_ver = ""
        for item in itemsPkg:
            # 将匹配到的内容用空替换，即去除匹配的内容，只留下文本
            line = re.sub(pattern, "", item)
            if len(line) > 0:
                clause_pkg += line + "\n"

        for item in itemsVer:
            line = re.sub(pattern, "", item)
            if len(line) > 0:
                clause_ver += line + "\n"

        return [clause_pkg,clause_ver]

    def getDownloadInfo(self,taskid):

        dwlist = []
        dwloadAll = DownloadApp.objects.all()
        checkAll=BaseApp.objects.all()
        apps = dwloadAll.filter(tasknum__contains=taskid)
        for dw in apps:
            if self.checkAppExists(dw.pkgname):
                try:
                    getArh = checkAll.filter(pkgname__contains=dw.pkgname).first()
                    dwinfo = {
                        'pkgName': dw.pkgname,
                        'dversion': dw.dversion,
                        'apkname': dw.apkfilename,
                        'apkpath': dw.apkfilePath,
                        'arh': getArh.arch
                    }
                except Exception:
                    dwinfo = {
                        'pkgName': dw.pkgname,
                        'dversion': dw.dversion,
                        'apkname': dw.apkfilename,
                        'apkpath': dw.apkfilePath,
                        'arh': '64'
                    }

                dwlist.append(dwinfo)
        return dwlist
    def updateSuccessStatus(self,getlist):
        if len(getlist)!=0:
            for app in getlist:
                try:
                 DownloadApp.objects.filter(pkgname=app['pkg'],tasknum=app['id']).update(uploadStatus=app['upstatus'])
                except Exception as e:
                    print(e)

    def getGoogleIcon(self,browser,url,imgpath,pkg):
        icon_xpath='//*[@id="yDmH0d"]/c-wiz[4]/div/div/div[2]/div[1]/div/div/c-wiz/div[1]/img[1]'
        # icon_xpath='//*[@id="yDmH0d"]/c-wiz[2]/div/div/div[2]/div[1]/div/div/c-wiz/div[2]/div[1]/img'
        try:
            wait = WebDriverWait(browser, 20)
            print(url)
            browser.get(url)
            wait.until(EC.visibility_of_element_located((By.XPATH, icon_xpath)))
            element_img =browser.find_element(By.XPATH,icon_xpath)
            img_url=element_img.get_attribute('src')
            print(img_url)

            img_path=self.save_image_path(imgpath,img_url,pkg)
            print(img_path)
        except Exception as e:
            img_url = ""
            print(img_url)
            img_path=self.save_image_path(imgpath,img_url, pkg)
            print(img_path)

    def getAllImage(self,browser,url):
        try:
            wait = WebDriverWait(browser, 20)
            print(url)
            browser.get(url)
            time.sleep(5)
            for image in browser.find_elements_by_tag_name("img"):


                print(image.text)
                print(image.size)
                print(image.tag_name)
        except Exception as e:

            print(e)
    def save_image_path(self, imgPath,showPath,img_url,pkg):
        img_end='_65.png'
        img_name=os.path.join(imgPath,pkg+ img_end)
        try:
            if img_url=='':
                img_url='https://'
            res = requests.get(img_url)
            with open(img_name,'wb') as f:
                f.write(res.content)

            img_path=showPath+pkg+ img_end
            save_path=imgPath+pkg+ img_end
            self.process_image(save_path)
        except Exception as e:
            img_path='img/model/Noimg'+ img_end
            save_path = imgPath+ 'Noimg'+ img_end
            print(pkg+":"+str(e))

        return img_path,save_path

    def compress_image(self, image_path, max_size_kb=150):
        with Image.open(image_path) as img:
            file_size = os.path.getsize(image_path)
            quality = 85  # Initial quality
            while file_size > max_size_kb * 1024 and quality > 10:
                img.save(image_path, quality=quality)
                file_size = os.path.getsize(image_path)
                quality -= 5
                print(f"Compressing image, current quality: {quality}, file size: {file_size // 1024} KB")

            # If still larger than max_size_kb, reduce dimensions further
            while file_size > max_size_kb * 1024 and img.size[0] > 100:
                new_size = (img.size[0] // 2, img.size[1] // 2)
                img = img.resize(new_size, Image.ANTIALIAS)
                img.save(image_path, quality=quality)
                file_size = os.path.getsize(image_path)
                print(f"Reducing dimensions to {new_size}, file size: {file_size // 1024} KB")

            if file_size <= max_size_kb * 1024:
                print(f"Image successfully compressed to {file_size // 1024} KB")
            else:
                print(f"Could not compress image below {max_size_kb} KB, final size: {file_size // 1024} KB")

    def resize_image(self, image_path, target_size=(512, 512), icon_size=(216, 216)):
        with Image.open(image_path) as img:
            # Check if the image size is not target or icon size
            if img.size != target_size and img.size != icon_size:
                # Resize image to the target size (512x512)
                img = img.resize(icon_size, Image.ANTIALIAS)
                img.save(image_path)
                print(f"Image resized to {target_size}")

    def process_image(self,image_path):
        self.compress_image(image_path)
        self.resize_image(image_path)

    def createPath(self, savePath):
        isExists = os.path.exists(savePath)
        if not isExists:

            os.makedirs(savePath)
            print("创建成功:"+savePath)
        else:

            print("路径已建成存在")
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
    def clickAiButton(self,browser,url):

        ai_button_xpath='//*[@id="challenge-stage"]/div/label/input'
        try:
            browser.get(url)
            wait = WebDriverWait(browser, 20)
            wait.until(EC.visibility_of_element_located((By.XPATH, ai_button_xpath)))
            wait.until(EC.element_to_be_clickable((By.XPATH, ai_button_xpath))).click()  # 点击add跳转add节目
            browser.switch_to.window(browser.window_handles[-1])
        except Exception as  e:
            print(e)