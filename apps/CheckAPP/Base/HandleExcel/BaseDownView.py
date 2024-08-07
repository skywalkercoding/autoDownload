import json
from google_play_scraper import app
def getGVersion( pkg):
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
        print("版本4：" + str(getVersion))
        return getVersion
    except Exception as e:
        print(e)
getGVersion("air.app.scb.breeze.android.main.my.prod")