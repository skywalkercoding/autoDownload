from django.conf import settings

Err1 = "App not found"
Err2 = "Varies with"
Err3 = "no find app"
Err4 = "urlparse Failed"
Upgrade1="YES"
Upgrade2="NO"


#下载地址和下载相关
MALAYSIA_F_URL_PKG='https://www.fibonas.com//app/show?package_name='
# 下地址token和结尾IP地址combo
URL_FP="a1cecdebaa60ed405d4e19cb8b133e7a"
URL_IP="14.137.161.250"
#没有用到setChrome安装版本
DRIVER_MANAGER_V='93.0.4577.63'
DOWNLOAD_SAVE_PATH=""
# 判断URL的地址出处
APKCOMBO_URL='https://apkcombo.com/'
APKCOMBO_CODE='apkcombo'
APKPURE_URL='https://apkpure.com/'
APKPURE_CODE="apkpure"
# 下载APKURL拼接
APKCOMBO_DOWNLOAD='download/apk'
APKPURE_DOWNLOAD='download'
# 去除空格
hreflink="%20"

DOWNLOAD_FAILED_LINK='NoLink'
# 破解人工智能地址
# API_KEY='873b1d7bbb95d9f0e5784b743d1c9ec8d082ba52'
API_KEY='a0183e74532810802c53bc525798d43dd9f39337' #测试api
API_URL='https://api.zenrows.com/v1/'

#下载地址
COMBO_URL = "https://apkcombo.com"
APKPURE_URL = "https://apkpure.com"

APK_FAILED='NoFile.apk'
PKG_FAILED='com.nofile.failed'

# 自动化上传应用到F
F_LOGIN_URL='https://www.fibonas.com/login'  #登录F的URL
ACCOUNT_XPATH='//*[@id="login"]/div/div/form/div[1]/input' #输入账号
PASSWORD_XPATH='//*[@id="login"]/div/div/form/div[2]/input' #输入密码
LOGIN_BUTTON_XPATH='//*[@id="login"]/div/div/form/div[4]/button' #点击登录按钮
Application_button='//*[@id="page-header"]/div/a[1]'  #点击应用按钮，调转去搜索节目
# //*[@id="page-header"]/div/a[1]
# F项目的管理员账号
ACCOUNT='zhuanyongtester@gmail.com'
PASSWORD='123456qazZ'
# 设置Chrome的版本
CHROME_VERSION_MANAGER='116.0.5845.111'

START_BROWER_FAILED="Start Failed"


ADD="add"
CREATE='create'
ChooseValue=1


HUAWEI_OAUTH_TOKEN_URL = 'https://oauth-login.cloud.huawei.com/oauth2/v3/token'  # 这里替换为实际的 URL
CLIENT_ID = '102726023'
CLIENT_SECRET = '5e87b5eb0683627914fbd82a65a32f722ff9fec104484ae2f173bba4c809dbb6'
HUAWEI_APP_REDIRECT_URL = 'http://localhost:8000/redirect'
AUTH_TOKEN = 'authorization_code'
REFRESH_TOKEN = 'refresh_token'