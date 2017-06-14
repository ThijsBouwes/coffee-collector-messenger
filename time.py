from datetime import datetime, timedelta

latestTime = datetime.now()
latestEmoticon = ''

def checkTime(level):
    global latestTime, latestEmoticon
    level = int(level)
    emoticon = getEmoticon(level)

    #time past or emoticon / level changed
    if latestTime < datetime.now() or latestEmoticon != emoticon:
        latestTime = getTime(level)
        latestEmoticon = emoticon

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
