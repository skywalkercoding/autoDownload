from django.conf import settings
import subprocess
from appium import webdriver
from appium.webdriver.common.appiumby import AppiumBy
import time,os
jarPath = 'D:/zhuwei/authAG/Fdownload/AutoUpgradeApp/apps/CheckAPP/Base/JavaDown/StartDownload.jar'
# libPath = settings.JAVA_PATH + '/CheckAPP/Base/JavaDown/lib/*'


uid='3KX0122708000562'
path="D:/zhuwei/downloadfile/Facebook_427.0.0.31.63_apkcombo.com.apk"
cmd= f"adb -s %s install \"%s\"" % (uid, path)
commd="D:/zhuwei/Android/sdk/platform-tools/""\"{}""".format(cmd)
java_classpath = jarPath+";.;"
java_command = f"java -cp {java_classpath} com.StartInstall {commd} "

def runCommad():

    try:
        # 调用Java程序
        result = subprocess.run(java_command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        if result.returncode == 0:
            # Java 程序正常运行，获取结果
            java_output = result.stdout.strip()
            print("Java程序输出：", java_output)

        else:
            # Java 程序运行出错，获取错误信息
            java_error = result.stderr.strip()
            isFindDownloading = False
            print("Java程序错误：", java_error)

    except subprocess.CalledProcessError as e:
        print("调用Java程序时出错：", e)


def connectAppium():
    try:
        caps = {}
        caps['platformName'] = "Android"
        caps["appium:platformVersion"] = "12"
        caps["appium:deviceName"] = uid
        caps["appium:newCommandTimeout"] = 3600

        driver = webdriver.Remote('127.0.0.1:9999/wd/hub', caps)
        driver.implicitly_wait(10)
        print("connected")

    except Exception as e:
        print(e)

    return driver

driver=connectAppium()

runCommad()
driver.find_element(AppiumBy.ID,'android:id/button1').click()
time.sleep(2)
driver.find_element(AppiumBy.ID,'android:id/button1').click()
time.sleep(2)
