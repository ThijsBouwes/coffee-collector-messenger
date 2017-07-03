from datetime import datetime, timedelta
from Services import helpers
import json
import requests
import random
import os
import time

USER_ENDPOINT = 'https://slack.com/api/users.list'
sentence = [
    'The universe requires your power: %s :super:',
    'Ohno, the kitchen is overflowing do something: %s :sweat_drops:'
]
latestTime = datetime.now()
latestLevel = ''

STATUS = {
    'a': [':grinning:', 'good'],
    'b': [':slightly_smiling_face:', '#439FE0'],
    'c': [':cold_sweat:', 'warning'],
    'd': [':scream:', 'danger']
}

# check if we need to send status to slack
def messageCheck(level):
    global latestTime, latestLevel
    levelStatus = getLevelStatus(level)

    # Time past or emoticon / level changed
    if latestTime < datetime.now() or latestLevel != levelStatus[0]:
        latestLevel = levelStatus[0]
        latestTime = levelStatus[1]
        message = getMessage(levelStatus[0], level)

        return sendSlackMessage(message)

# hit incoming webhook slack
def sendSlackMessage(message):
    url = os.getenv('SLACK_API')

    try:
        requests.post(url, data=json.dumps(message))
        return True
    except requests.ConnectionError:
        return False

# build slack message, with attachments
def getMessage(status, level):
    message = {
        "attachments": [{
            "fallback": "New reading from CC",
            "color": STATUS[status][1],
            "pretext": "New reading from the CC",
            "title": "Details",
            "fields": [
                {
                    "title": "Level",
                    "value": "%s %%" % helpers.calculatePercentage(level),
                    "short": True
                },
                {
                    "title": "Feeling",
                    "value": STATUS[status][0],
                    "short": True
                }
            ],
            "footer": "CC Power",
            "footer_icon": "https://media.licdn.com/mpr/mpr/shrink_200_200/AAEAAQAAAAAAAASqAAAAJDg5ZWM2Nzk5LTg2YjUtNDIyNS1hMjljLWRmMWJjNmUwZjMyYg.png",
            "ts": time.time()
        }]
    }

    if status == "d":
        memberNames = filterMembers(getSlackUsers())

        selectedMembers = random.sample(memberNames, 3)
        selectedSentence = random.choice(sentence)

        users = "@"+", @".join(str(x) for x in selectedMembers)
        message["attachments"][0]['text'] = selectedSentence % users

    return message

# get all slack users
def getSlackUsers():
    token = os.getenv('SLACK_TOKEN')
    payload =  {"token": token}
    r = requests.post(USER_ENDPOINT, data=payload)
    data = json.loads(r.text)

    return data['members']

# return member names, only active users
def filterMembers(members):
    elements = []

    for member in members:

        if member['deleted'] == False and member['is_bot'] == False and member['is_restricted'] == False and member['is_ultra_restricted'] == False and member['name'] != "slackbot":
            elements.append(member['name'])

    return elements

# return level status and next time to check
def getLevelStatus(level):
    if level > 50:
        return ('a', datetime.now() + timedelta(hours=24))
    elif 15 < level <= 50:
        return ('b', datetime.now() + timedelta(hours=12))
    elif 5 < level <= 15:
        return ('c', datetime.now() + timedelta(hours=6))
    else:
        return ('d', datetime.now() + timedelta(hours=3))
