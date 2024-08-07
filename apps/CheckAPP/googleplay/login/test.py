import os

gsfId = os.environ.get('PLAYSTORE_GSFID')
authSubToken = os.environ.get('PLAYSTORE_TOKEN')
tokenDispenser = os.environ.get('PLAYSTORE_DISPENSER_URL')

print(gsfId)