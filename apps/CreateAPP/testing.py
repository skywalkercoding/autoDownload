from bs4 import BeautifulSoup
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
import time
url='https://appgallery.huawei.com/app/C110641259'
# 创建Chrome WebDriver
driver = webdriver.Chrome(ChromeDriverManager().install())
driver.get(url)
# 获取网页标题
title = driver.title
print("网页标题:", title)
time.sleep(10)
# 获取网页源代码获取网页源代码
html = driver.page_source
soup = BeautifulSoup(html, 'html.parser')

# Extract specific information
app_info = {}
detail_info = soup.find('div', class_='detailInfo')
if detail_info:
    app_info['price'] = detail_info.find('div', class_='info_val').text.strip()
    app_info['size'] = detail_info.find_all('div', class_='info_val')[1].text.strip()
    app_info['rating'] = soup['score']  # Assuming 'score' is the rating
    # Extract other relevant information in a similar manner

print(app_info)