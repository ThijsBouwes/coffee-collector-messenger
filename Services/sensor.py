import RPi.GPIO as GPIO
import time

TRIG = 21
ECHO = 20

GPIO.setmode(GPIO.BCM)
GPIO.setup(TRIG,GPIO.OUT)
GPIO.setup(ECHO,GPIO.IN)

def pulseIn(pin, state):
    while GPIO.input(pin)==state:
        pulseTime = time.time()
    return pulseTime
    
def calculateDistance():
    GPIO.output(TRIG, False)
    time.sleep(0.000002)
    GPIO.output(TRIG, True)
    time.sleep(0.00001)
    GPIO.output(TRIG, False)

    pulse_start = pulseIn(ECHO, 0);
    pulse_end = pulseIn(ECHO, 1);

    # speed of sound 34300 cm/s
    distance = (pulse_end - pulse_start) * 17150
    distance = round(distance, 2)

    if distance > 1 and distance < 400:
        return distance;