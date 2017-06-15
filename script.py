from datetime import datetime, timedelta
import RPi.GPIO as GPIO
import time
from Services import *

global latestTimeScreenUpdate
latestSensorUpdate = datetime.now()
latestTimeScreenUpdate = datetime.now()

while True:
    if latestSensorUpdate < datetime.now():
        reading = sensor.calculateDistance()
        latestSensorUpdate = datetime.now() + timedelta(seconds=3)
        if reading != False:
            slack.messageCheck(reading)
    if latestTimeScreenUpdate < datetime.now() and reading != False:
        screen.drawPage(reading)
        latestTimeScreenUpdate = datetime.now() + timedelta(seconds=3)
        
GPIO.cleanup()