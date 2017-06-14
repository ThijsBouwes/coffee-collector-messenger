from datetime import datetime, timedelta
import json
import request 

latestTime = datetime.now()
latestEmoticon = ''

def messageCheck(level):
    global latestTime, latestEmoticon
    level = int(level)
    emoticon = getEmoticon(level)

    #time past or emoticon / level changed
    if latestTime < datetime.now() or latestEmoticon != emoticon:
        sendSlackMessage(level)
        latestTime = getTime(level)
        latestEmoticon = emoticon

def sendSlackMessage(value):
    url = os.getenv('SLACK_API')
    payload =  {"text": "The current level of CC is: %s cm left %s" % (value, getEmoticon(value))}
    
    return requests.post(url, data=json.dumps(payload)) 

def getEmoticon(level):
    if level > 50:
        return ":grinning:"
    elif level <= 50 and level > 15:
        return ":slightly_smiling_face:"
    elif level <= 15 and level > 5:
        return ":cold_sweat:"
    else:
        return ":scream:"

def getTime(level):
    if level > 50:
        return datetime.now() + timedelta(seconds=24)
    elif level <= 50 and level > 15:
        return datetime.now() + timedelta(seconds=12)
    elif level <= 15 and level > 5:
        return datetime.now() + timedelta(seconds=6)
    else:
        return datetime.now() + timedelta(seconds=3)
