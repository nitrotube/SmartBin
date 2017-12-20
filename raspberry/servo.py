import Adafruit_PCA9685
import time

pwm = Adafruit_PCA9685.PCA9685()
UP_SERVO = 3  # Upper servo pina
DOWN_SERVO = 2  # Down servo pin
LOCK1_SERVO = 15 #15
LOCK2_SERVO = 14
OPEN_UP = 250  # Positions of servo
CLOSE_UP = 530
CLOSE_DOWN = 385
PET_DOWN = 650
AL_DOWN = 170
LOCK1_CLOSE = 472
LOCK1_OPEN = 400
LOCK2_CLOSE = 340
LOCK2_OPEN = 405
RED = 8
GREEN = 9
BLUE = 10
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

