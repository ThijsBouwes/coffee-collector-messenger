import sys
import logging
import RPi.GPIO as GPIO
from Services import *
from os.path import join
from datetime import datetime, timedelta

global latestTimeScreenUpdate

logging.basicConfig(level=logging.INFO, filename=join(sys.path[0], 'cc.log'), format='%(asctime)s - %(levelname)s - %(message)s')

latestSensorUpdate = datetime.now()
latestTimeScreenUpdate = datetime.now()
connectedToSlack = True

logging.info('CC starts')

while True:
    reading = False
    if latestSensorUpdate < datetime.now():
        reading = sensor.calculateDistance()
        latestSensorUpdate = datetime.now() + timedelta(seconds=3)
        if reading is not False:
            connectedToSlack = slack.messageCheck(reading)

    if latestTimeScreenUpdate < datetime.now() and reading is not False:
        screen.drawPage({'level': reading, 'connection': connectedToSlack})
        latestTimeScreenUpdate = datetime.now() + timedelta(seconds=3)

logging.warn('CC stops')
GPIO.cleanup()
