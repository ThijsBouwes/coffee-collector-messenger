from datetime import datetime, timedelta
import RPi.GPIO as GPIO
import time
import logging
from Services.helpers import HEIGHT_CAN

TRIG = 14
ECHO = 23

GPIO.setmode(GPIO.BCM)
GPIO.setup(TRIG,GPIO.OUT)
GPIO.setup(ECHO,GPIO.IN)


def pulseIn(pin, state):
    timeout = datetime.now()+timedelta(seconds=5)
    pulseTime = time.time()

    while GPIO.input(pin) == state:
        pulseTime = time.time()
        if datetime.now() > timeout:
            raise ValueError('The pulse took to long')
            
    return pulseTime


def calculateDistance():
    GPIO.output(TRIG, False)
    time.sleep(0.000002)
    GPIO.output(TRIG, True)
    time.sleep(0.00001)
    GPIO.output(TRIG, False)
    buffer = 5

    try:
        pulse_start = pulseIn(ECHO, 0)
        pulse_end = pulseIn(ECHO, 1)
    except ValueError as error:
        logging.warning(str(error))

        return False

    # Speed of sound 34300 cm/s
    distance = round((pulse_end - pulse_start) * 17150)
    # round distance to upper multiple of 5, e.g. 146 -> 150; 140 -> 145
    distance += buffer - distance % buffer

    return distance if 0 < distance - buffer <= HEIGHT_CAN else False
