from datetime import datetime, timedelta
from Services import helpers
import json
import requests
import os

latestTime = datetime.now()
latestEmoticon = ''

def messageCheck(level):
    global latestTime, latestEmoticon
    levelStatus = getLevelStatus(level)

    #time past or emoticon / level changed
    if latestTime < datetime.now() or latestEmoticon != levelStatus[0]:
        latestTime = levelStatus[1]
        latestEmoticon = levelStatus[0]

        return sendSlackMessage(level, latestEmoticon)

def sendSlackMessage(level, emoticon):
    url = os.getenv('SLACK_API')
    payload =  {"text": "The current level of CC is: %s %% %s" % (helpers.calculatePercentage(level), emoticon)}
    
    try:
        requests.post(url, data=json.dumps(payload)) 
        return True
    except requests.ConnectionError:
        return False

def getLevelStatus(level):
    if level > 50:
        return (":grinning:", datetime.now() + timedelta(hours=24))
    elif 15 < level <= 50:
        return (":slightly_smiling_face:", datetime.now() + timedelta(hours=12))
    elif 5 < level <= 15:
        return (":cold_sweat:", datetime.now() + timedelta(hours=6))
    else:
        return (":scream:", datetime.now() + timedelta(hours=3))
