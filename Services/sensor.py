from datetime import datetime, timedelta
import RPi.GPIO as GPIO
import time
import logging

HEIGHT_CAN = 45
TRIG = 14
ECHO = 23
READING_ROUND = 5

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

    try:
        pulse_start = pulseIn(ECHO, 0)
        pulse_end = pulseIn(ECHO, 1)
    except ValueError as error:
        logging.warning(str(error))

        return False

    # Speed of sound 34300 cm/s
    distance = round((pulse_end - pulse_start) * 17150)
    # round distance to upper multiple of 5, e.g. 146 -> 150; 140 -> 145
    distance += READING_ROUND - distance % READING_ROUND

    return distance if 0 < distance - READING_ROUND <= HEIGHT_CAN else False


# determines how full the can is
def calculatePercentage(reading):
    percentage = round((HEIGHT_CAN - reading) / HEIGHT_CAN * 100)
    percentage += READING_ROUND - percentage % READING_ROUND

    return 100 if reading > HEIGHT_CAN else percentage
