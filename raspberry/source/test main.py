from config import *
import RPi.GPIO as GPIO
import time
import urllib4
import picamera
import logging
import datetime
import send

import Adafruit_PCA9685
import serial

GPIO.setmode(GPIO.BOARD)

GPIO.setup(BEEPER, GPIO.OUT)
GPIO.output(BEEPER, 1)

CurGreen = 0
CurRed = 0
CurBlue = 0

camera = picamera.PiCamera()
logging.basicConfig(format='%(levelname)s:%(message)s', level=logging.INFO)  # Setting up logging

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

WAIT_LIMIT = 8


def check_rfid():
    code = ''
    while True:
        #logging.info(UART.read().decode("utf-8"))
        if UART.read() == b'\x02':
            code = UART.read(12)
            UART.flushInput()

            break
    code = code.decode("utf-8")
    logging.info(code)
    return code


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


def make_photo():
    GPIO.output(INNER, 1)
    image_time = datetime.datetime.now()  # Making a unique name of a string from datetime
    image_time = str(image_time)[:19].replace(' ', '').replace('-', '').replace(':', '')
    image_path = '/home/pi/Documents/Photos/' + image_time + '.jpeg'
    camera.resolution = (640, 480)
    camera.brightness = 35
    camera.contrast = 50
    camera.capture(image_path, use_video_port=True)
    GPIO.output(INNER, 0)
    return image_path


def contents_type():
    image = make_photo()
    return send.get_class(image)

def waiting():
    global CurGreen, CurBlue
    for i in range(1000):
        pwm.set_pwm(GREEN, 0, CurGreen)
        pwm.set_pwm(BLUE, 0,  CurBlue)
        CurGreen -= 2
        CurBlue += 2
        time.sleep(0.001)

    for i in range(1000):
        pwm.set_pwm(GREEN, 0, CurGreen)
        pwm.set_pwm(BLUE, 0, CurBlue)
        CurGreen += 2
        CurBlue -= 2
        time.sleep(0.001)


def sonic_check(TRIG,ECHO):
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

    if (distance > 42) or (distance < 37):
        return True
    return False


def something_in():
    k = 0
    for i in range(30):
        if sonic_check(TRIG1,ECHO1):
            k += 1
        time.sleep(0.0001)
        if sonic_check(TRIG2,ECHO2):
            k += 1
    if k < 10:
        return False
    return True


def cheat_check():
    k = 0
    for i in range(30):
        if sonic_check(TRIG3,ECHO3):
            k += 1
    if k < 10:
        return False
    return True


def user_reg(user_id):
    user_url = 'http://smartbin35.ru.mastertest.ru/api/checkuser?cardCode=' + user_id
    logging.info(user_id)
    response = urllib.request.urlopen(user_url)
    logging.info(response.read())
    user_status = response.read()
    if user_status == b'true':
        return True
    return False


def reward(user_id, trash_type):
    reward_url = 'http://smartbin35.ru.mastertest.ru/api/bonus?cardCode=' + user_id
    reward_url = reward_url + '&trashType=' + trash_type + '&trashId=2'
    urllib.request.urlopen(reward_url)


def beep():
    GPIO.output(BEEPER, 0)
    time.sleep(0.3)
    GPIO.output(BEEPER, 1)

try:
    time.sleep(1)
    close_lock()
    logging.info("Process started")
    while True:
        # Correct
        close_up()
        close_down()

        user = check_rfid()

        if not(user):
            continue

        beep()

        if user == "5605B8DF7642":
            open_lock()
            logging.info("The bin is opened for maintenance")
            reward(user, 'pet')
            while True:
                time.sleep(5)
        reg_stat = 0
        try:
            reg_stat = user_reg(user)
        except:
            time.sleep(1)
            UART.flushInput()
        if reg_stat:
            logging.info("User found")
            # Correct
            entry_time = time.time()
            time_exit = False

            while not time_exit:
                find_exit = False
                open_up()
                while (not find_exit) and (not time_exit):
                    time.sleep(0.1)
                    current_time = time.time()
                    if current_time - entry_time > WAIT_LIMIT:
                        time_exit = True
                    if something_in():
                        find_exit = True
                time.sleep(0.5)
                close_up()
                time.sleep(0.5)
                if not find_exit:
                    continue

                if something_in():
                    time.sleep(0.7)
                    logging.info("Something in")
                    inner_type = ""
                    if fake == 1:
                        fake = 0
                    else:
                        fake = 1
                    try:
                        inner_type = contents_type()

                    except:
                        time.sleep(5)
                        time_exit = True

                    entry_time = time.time()
                    find_exit = False
                    if inner_type == 'pet':
                        pet_down()
                        time.sleep(2.5)
                        close_down()
                        try:
                            reward(user, 'pet')
                        except:
                            time.sleep(0.5)
                        logging.info('Rewarded for pet!')
                    elif inner_type == 'al':
                        al_down()
                        time.sleep(2.5)
                        close_down()
                        try:
                            reward(user, 'al')
                        except:
                            time.sleep(0.5)
                        logging.info('Rewarded for al!')
                    else:
                        # Correct

                        open_up()
                        while something_in():
                            time.sleep(0.01)
                        time.sleep(1)
                        close_up()
                        time_exit = True
                else:
                    entry_time = time.time()
                    # Correct
            logging.info("Session closed")
            logging.info('****************************')
        else:
            pass
            # Correct

        time.sleep(0.5)
        UART.flushInput()


finally:
    GPIO.cleanup()
    camera.close()
