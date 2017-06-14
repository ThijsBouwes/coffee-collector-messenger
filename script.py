import RPi.GPIO as GPIO
import time
from Services import *

while True:
    localReading = sensor.calculateDistance() if sensor.calculateDistance() else 0
    if (localReading != ""):
        mqtt.publish(str(localReading))

    screen.drawStatsPageOne(localReading)
    time.sleep(2)
    screen.drawStatsPageTwo()
    time.sleep(2)

GPIO.cleanup()