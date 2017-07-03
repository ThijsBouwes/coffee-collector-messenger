from datetime import datetime, timedelta
from Services import helpers
import json
import requests
import random
import os

sentence = ['The universe requires your power: %s :super:', 'ohno, the kitchen is overflowing do something: %s :sweat_drops:']
latestTime = datetime.now()
latestEmoticon = ''
USER_ENDPOINT = 'https://slack.com/api/users.list'

def messageCheck(level):
    global latestTime, latestEmoticon
    levelStatus = getLevelStatus(level)

    # Time past or emoticon / level changed
    if latestTime < datetime.now() or latestEmoticon != levelStatus[0]:
        latestEmoticon = levelStatus[0]
        latestTime = levelStatus[1]

        return sendSlackMessage(level, latestEmoticon)

def getSlackUsers():
    token = os.getenv('SLACK_TOKEN')
    payload =  {"token": token}
    r = requests.post(USER_ENDPOINT, data=payload)
    data = json.loads(r.text)

    return data['members']

def filterMembers(members):
    elements = []

    for member in members:

        if member['deleted'] == False and member['is_bot'] == False and member['is_restricted'] == False and member['is_ultra_restricted'] == False:
            elements.append(member['name'])

    return elements

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
        memberNames = filterMembers(getSlackUsers())
        selectedMembers = random.sample(memberNames, 3)
        selectedSentence = random.choice(sentence)
        users = "@"+", @".join(str(x) for x in selectedMembers)

        return (":scream:\n" + selectedSentence % users, datetime.now() + timedelta(hours=3))
