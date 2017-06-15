from datetime import datetime, timedelta
import RPi.GPIO as GPIO
import time
from Services import *

global latestTimeScreenUpdate
latestSensorUpdate = datetime.now()
latestTimeScreenUpdate = datetime.now()

while True:
    connectedToSlack = True

    if latestSensorUpdate < datetime.now():
        reading = sensor.calculateDistance()
        latestSensorUpdate = datetime.now() + timedelta(seconds=3)
        if reading != False:
            connectedToSlack = slack.messageCheck(reading)
    if latestTimeScreenUpdate < datetime.now() and reading != False:
        screen.drawPage({'level': reading, 'connection': connectedToSlack})
        latestTimeScreenUpdate = datetime.now() + timedelta(seconds=3)
        
GPIO.cleanup()