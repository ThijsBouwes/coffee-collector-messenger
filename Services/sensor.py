from datetime import datetime, timedelta
import RPi.GPIO as GPIO
import time

TRIG = 21
ECHO = 20

GPIO.setmode(GPIO.BCM)
GPIO.setup(TRIG,GPIO.OUT)
GPIO.setup(ECHO,GPIO.IN)

def pulseIn(pin, state):
    timeout = datetime.now()+timedelta(seconds=5)
    while GPIO.input(pin)==state:
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
        return False

    # speed of sound 34300 cm/s
    distance = round((pulse_end - pulse_start) * 17150, 2)

    return distance if 1 <= distance <= 400 else False
