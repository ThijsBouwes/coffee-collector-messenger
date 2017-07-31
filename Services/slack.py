from datetime import datetime, timedelta
from Services.sensor import calculatePercentage
import json
import requests
import random
import os
import time
import logging

USER_ENDPOINT = 'https://slack.com/api/users.list'
sentence = [
    'The universe requires your power: %s :super:',
    'Ohno, the kitchen is about to flood, do something: %s :sweat_drops:'
]
latestTime = datetime.now()
latestLevelTime = datetime.now()
historicLevels = ['', '']

STATUS = {
    'a': [':grinning:', 'good'],
    'b': [':slightly_smiling_face:', '#439FE0'],
    'c': [':cold_sweat:', 'warning'],
    'd': [':scream:', 'danger']
}


# check if we need to send status to slack, if so, do it
def messageCheck(reading):
    global latestTime, historicLevels, latestLevelTime
    currentLevelStatus, nextLevelUpdate = getLevelStatus(reading)

    # Time past or level changed
    if latestTime < datetime.now():
        latestTime = nextLevelUpdate
        message = getMessage(currentLevelStatus, reading)
        logging.info('Slack periodic message Status: %s Level: %s %%', currentLevelStatus, calculatePercentage(reading))

        return sendSlackMessage(message)

    # Send message when the current and previous reading are the same
    # And different than three readings ago, do not send on init
    if historicLevels[0] == currentLevelStatus and historicLevels[1] != currentLevelStatus and historicLevels[1] != '' and latestLevelTime < datetime.now():
        historicLevels[1] = currentLevelStatus
        latestLevelTime = datetime.now() + timedelta(minutes=30)
        message = getMessage(currentLevelStatus, reading)
        logging.info('Slack level change Status: %s Level: %s %%', currentLevelStatus, calculatePercentage(reading))

        return sendSlackMessage(message)
    elif historicLevels[0] != currentLevelStatus:
        # set first step in history
        historicLevels[0] = currentLevelStatus
    else:
        # set two steps in history
        historicLevels[1] = historicLevels[0]
        historicLevels[0] = currentLevelStatus

    return True


# hit incoming webhook slack
def sendSlackMessage(message):
    url = os.environ.get("SLACK_API")

    try:
        requests.post(url, data=json.dumps(message))

        return True
    except requests.ConnectionError:
        logging.warning('Connection Error')

        return False


# build slack message, with attachments
def getMessage(status, reading):
    message = {
        "attachments": [{
            "fallback": "New reading from CC",
            "color": STATUS[status][1],
            "pretext": "New reading from the CC",
            "title": "Details",
            "fields": [
                {
                    "title": "Level",
                    "value": "%s %%" % calculatePercentage(reading),
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

    if status == "d" or status == "c":
        memberNames = filterMembers(getSlackUsers())

        selectedMembers = random.sample(memberNames, 3)
        selectedSentence = random.choice(sentence)

        users = "@"+", @".join(str(x) for x in selectedMembers)
        message["attachments"][0]['text'] = selectedSentence % users

    return message


# get all slack users
def getSlackUsers():
    token =  os.environ.get("SLACK_TOKEN")
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
def getLevelStatus(reading):
    if reading > 32:
        return 'a', datetime.now() + timedelta(hours=24)
    elif 24 < reading <= 32:
        return 'b', datetime.now() + timedelta(hours=12)
    elif 16 < reading <= 24:
        return 'c', datetime.now() + timedelta(hours=6)
    else:
        return 'd', datetime.now() + timedelta(hours=3)
