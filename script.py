import RPi.GPIO as GPIO
import time
from Services import *

while True:
    reading = sensor.calculateDistance()
    slack.messageCheck(reading)
    screen.drawStatsPageOne(reading)
    time.sleep(2)
    screen.drawStatsPageTwo()
    time.sleep(2)

GPIO.cleanup()