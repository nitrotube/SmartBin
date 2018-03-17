from config import *
import RPi.GPIO as GPIO
import time
import picamera
import logging
import datetime
import send
import random

import Adafruit_PCA9685
import serial




GPIO.setmode(GPIO.BOARD)

GPIO.setup(BEEPER, GPIO.OUT)
GPIO.output(BEEPER, 0)


camera = picamera.PiCamera()
logging.basicConfig(format='%(levelname)s:%(message)s', filename='log.txt', level=logging.INFO)  # Setting up logging

UART = serial.Serial(
    port='/dev/serial0',
    baudrate=9600,
    parity=serial.PARITY_NONE,
    stopbits=serial.STOPBITS_ONE,
    bytesize=serial.EIGHTBITS,
    timeout=1
)

pwm = Adafruit_PCA9685.PCA9685()

pwm.set_pwm_freq(75)

fake = 1

GPIO.setup(INNER, GPIO.OUT)
GPIO.output(INNER, 0)

GPIO.setup(TRIG1, GPIO.OUT)
GPIO.setup(ECHO1, GPIO.IN)
GPIO.setup(TRIG2, GPIO.OUT)
GPIO.setup(ECHO2, GPIO.IN)
GPIO.setup(TRIG3, GPIO.OUT)
GPIO.setup(ECHO3, GPIO.IN)

WAIT_LIMIT = 6
command = ''

random.seed()

AL_LIMIT = 50
PET_LIMIT = 15


def open_up():
    try:
        pwm.set_pwm(UP_SERVO, 0, OPEN_UP)
    except:
        time.sleep(0.5)
        pwm.set_pwm(UP_SERVO, 0, OPEN_UP)


def close_up():
    try:
        pwm.set_pwm(UP_SERVO, 0, CLOSE_UP)
    except:
        time.sleep(0.5)
        pwm.set_pwm(UP_SERVO, 0, CLOSE_UP)


def close_down():
    try:
        pwm.set_pwm(DOWN_SERVO, 0, CLOSE_DOWN)
    except:
        time.sleep(0.5)
        pwm.set_pwm(DOWN_SERVO, 0, CLOSE_DOWN)


def pet_down():
    try:
        pwm.set_pwm(DOWN_SERVO, 0, PET_DOWN)
    except:
        time.sleep(0.5)
        pwm.set_pwm(DOWN_SERVO, 0, PET_DOWN)


def al_down():
    try:
        pwm.set_pwm(DOWN_SERVO, 0, AL_DOWN)
    except:
        time.sleep(0.5)
        pwm.set_pwm(DOWN_SERVO, 0, AL_DOWN)


def open_lock():
    try:
        pwm.set_pwm(LOCK1_SERVO, 0, LOCK1_OPEN)
        pwm.set_pwm(LOCK2_SERVO, 0, LOCK2_OPEN)
    except:
        time.sleep(0.5)
        pwm.set_pwm(LOCK1_SERVO, 0, LOCK1_OPEN)
        pwm.set_pwm(LOCK2_SERVO, 0, LOCK2_OPEN)


def make_photo():
    GPIO.output(INNER, 1)
    image_time = datetime.datetime.now()  # Making a unique name of a string from datetime
    image_time = str(image_time)[:19].replace(' ', '').replace('-', '').replace(':', '')
    image_path = '/home/pi/Documents/Photos/' + image_time + '.jpeg'
    camera.resolution = (640, 480)
    camera.brightness = 60
    camera.contrast = 55
    camera.capture(image_path, use_video_port=True)
    return image_path


def contents_type():
    image = make_photo()
    return send.get_class(image)


def static_color(port):  # Just displaying a color
    global CurGreen, CurBlue, CurRed
    CurGreen = 4000
    CurRed = 0
    CurBlue = 2000
    port -= 5

    colors = [CurRed, CurGreen, CurBlue]
    while colors[port] != 4000 or sum(colors) != 4000:
        for i in range(3):
            if i == port:
                colors[i] = min(4000, colors[i] + 25)
            else:
                colors[i] = max(0, colors[i] - 25)
            try:
                pwm.set_pwm(i + 5, 0, colors[i])
            except:
                time.sleep(0.3)
                pwm.set_pwm(i + 5, 0, colors[i])

    CurRed = colors[0]
    CurGreen = colors[1]
    CurBlue = colors[2]


def sonic_check(TRIG, ECHO):
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
    distance = round(distance, 2) - 0.5

    if (distance > 42) or (distance < 38):
        return True
    return False


def something_in():
    k = 0
    for i in range(30):
        if sonic_check(TRIG1, ECHO1):
            k += 1
        time.sleep(0.005)
        if sonic_check(TRIG2, ECHO2):
            k += 1
    if k < 5:
        return False
    return True


def beep():
    GPIO.output(BEEPER, 1)
    time.sleep(0.3)
    GPIO.output(BEEPER, 0)


try:
    open_lock()
    static_color(GREEN)
    open_up()
    close_down()
    GPIO.output(INNER, 1)
    time.sleep(1)
    while True:
        if something_in():
            beep()
            close_up()
            time.sleep(1)
            make_photo()
            pet_down()
            time.sleep(1.5)
            close_down()
            open_up()
            time.sleep(1)


finally:
    GPIO.cleanup()
    camera.close()
