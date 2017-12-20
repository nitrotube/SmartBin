import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BOARD)

TRIG = 16
ECHO = 18

#16, 18 - upper
# 33, 35 - down glass, 5,6 - down back

GPIO.setup(TRIG, GPIO.OUT)
GPIO.setup(ECHO, GPIO.IN)


def sonic_check():
    GPIO.output(TRIG, False)
    time.sleep(0.01)
    GPIO.output(TRIG, True)
    time.sleep(0.00001)
    GPIO.output(TRIG, False)

    while GPIO.input(ECHO) == 0:
        pulse_start = time.time()

    while GPIO.input(ECHO) == 1:
        pulse_end = time.time()

    pulse_duration = pulse_end - pulse_start
    distance = pulse_duration * 17150
    distance = round(distance, 2)
    distance = distance - 0.5
    print(distance)

    if (distance > 37) or (distance < 29):
        here = True
    else:
        here = False
    return here


def something_in():
    really = True
    k = 0
    for i in range(30):
        k += 1
    if k < 5:
        really = False
    return really


try:
    while True:
        print(sonic_check())
        time.sleep(1)
finally:
    GPIO.cleanup()
