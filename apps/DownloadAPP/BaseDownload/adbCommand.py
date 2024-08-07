from django.views.generic import View
import  apps.DownloadAPP.BaseDownload.downComm as dwComm
import subprocess
class adbCommmand(View):
    def __init__(self,uid=None,path=None,pkg=None):
        self.path=path
        self.uid=uid
        self.pkg=pkg
    def checkConnect(self):
        adbCommmand="adb devices"
        cmdRes=subprocess.getstatusoutput(adbCommmand)
        if cmdRes[0] == 0:
            getRes=cmdRes[1]
        else:
            getRes = cmdRes[1]
        return getRes
    def delpkgcmd(self):
        print(self.uid)
        if self.pkg is None:
            pass
        else:
           adbCommmand = "adb uninstall " + self.pkg
           print(adbCommmand)
           getRes = self.runAdbComand(adbCommmand)
           return getRes
    def install_apk(self):
        adbCommmand="adb -s %s install \"%s\"" % (self.uid,self.path)
        print(adbCommmand)
        getRes=self.runAdbComand(adbCommmand)
        return getRes

    def runAdbComand(self,command):
        isAdbResult=False
        cmdRes = subprocess.getstatusoutput(command)
        if cmdRes[0] == 0:
            isAdbResult = True


        return isAdbResult

