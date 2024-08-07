
from google_play_scraper import app
import json
def getGVersion( pkg):
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
        categories = data2['categories']
        print(icon)
    except Exception as e:
        print(e)
        appName = ''
        icon = ''
        categories = ''
        print(icon)
    return [appName, icon, categories]
getGVersion("com.apple.android.music    ")