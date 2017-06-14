import json
import request 
        
def sendSlackMessage(value):
    url = os.getenv('SLACK_API')
    payload =  {"text": "The current level of CC is: %s cm left %s" % (value, getEmoticon(value))}
    return requests.post(url, data=json.dumps(payload)) 

def getEmoticon(level):
    level = int(level)
    if level > 50:
        return ":grinning:"
    elif level < 50 and level > 15:
        return ":slightly_smiling_face:"
    else:
        return ":triumph:"