import Adafruit_PCA9685
import time
from config import *

pwm = Adafruit_PCA9685.PCA9685()

pwm.set_pwm_freq(75)


def open_up():
    pwm.set_pwm(UP_SERVO, 0, OPEN_UP)


def close_up():
    pwm.set_pwm(UP_SERVO, 0, CLOSE_UP)


def close_down():
    pwm.set_pwm(DOWN_SERVO, 0, CLOSE_DOWN)


def pet_down():
    pwm.set_pwm(DOWN_SERVO, 0, PET_DOWN)


def al_down():
    pwm.set_pwm(DOWN_SERVO, 0, AL_DOWN)


def close_lock():
    pwm.set_pwm(LOCK1_SERVO, 0, LOCK1_CLOSE)
    pwm.set_pwm(LOCK2_SERVO, 0, LOCK2_CLOSE)


def open_lock():
    pwm.set_pwm(LOCK1_SERVO, 0, LOCK1_OPEN)
    pwm.set_pwm(LOCK2_SERVO, 0, LOCK2_OPEN)


while True:
    open_lock()
    close_up()

    pwm.set_pwm(10, 0, 4000)
    for i in range(2000):
        pwm.set_pwm(GREEN, 0, (2000-i)*2)
        pwm.set_pwm(BLUE, 0, i*2)
        #pwm.set_pwm(RED, 0, i)
        #time.sleep(0.00001)
    for i in range(2000):
        pwm.set_pwm(GREEN, 0, i * 2)
        pwm.set_pwm(BLUE, 0, (2000 - i)*2)
        # pwm.set_pwm(RED, 0, i)
        # time.sleep(0.00001)

