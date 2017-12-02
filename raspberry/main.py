import RPi.GPIO as GPIO
import time
import urllib.request
import picamera
import logging
import datetime
import requests
import Adafruit_PCA9685
import serial

GPIO.setmode(GPIO.BOARD)

BEEPER = 32
GPIO.setup(BEEPER, GPIO.OUT)
GPIO.output(BEEPER, 1)

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

UP_SERVO = 2  # Upper servo pin
DOWN_SERVO = 0  # Down servo pin
LOCK_SERVO = 1 # Lock servo pin
OPEN_UP = 320  # Positions of servo
CLOSE_UP = 135
CLOSE_DOWN = 473
PET_DOWN = 580
AL_DOWN = 280
LOCK_CLOSE = 480
LOCK_OPEN = 425
pwm.set_pwm_freq(60)

fake = 1

RED = 36
INNER = 38
BLUE = 40
GREEN = 22
GPIO.setup(RED, GPIO.OUT)
GPIO.setup(INNER, GPIO.OUT)
GPIO.setup(BLUE, GPIO.OUT)
GPIO.setup(GREEN, GPIO.OUT)
GPIO.output(RED, 0)
GPIO.output(INNER, 0)
GPIO.output(BLUE, 0)
GPIO.output(GREEN, 0)

TRIG = 18
ECHO = 16
GPIO.setup(TRIG, GPIO.OUT)
GPIO.setup(ECHO, GPIO.IN)

WAIT_LIMIT = 6


def check_rfid():
    code = ''
    while True:
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
    pwm.set_pwm(LOCK_SERVO, 0, LOCK_CLOSE)


def open_lock():
    pwm.set_pwm(LOCK_SERVO, 0, LOCK_OPEN)


def make_photo():
    GPIO.output(INNER, 1)
    GPIO.output(GREEN, 0)
    time.sleep(0.1)
    image_time = datetime.datetime.now()  # Making a unique name of a string from datetime
    image_time = str(image_time)
    image_time = image_time[0:4] + image_time[5:7] + image_time[8:10] + image_time[11:13] + image_time[
                                                                                            14:16] + image_time[17:19]
    image_path = '/home/pi/Documents/Photos/' + image_time + '.jpeg'
    camera.saturation = -20
    camera.brightness = 50
    camera.contrast = 0
    camera.resolution = (640, 480)
    camera.capture(image_path, use_video_port=True)
    GPIO.output(INNER, 0)
    GPIO.output(GREEN, 1)
    return image_path


def upload_to_web(image_path):
    url_api = 'http://217.71.231.9:48777/api/UploadFile4Recognition'
    user_id = 'SmartBin'
    image_type = 'garbage'

    files = {
        'file': ('image.jpg', open(image_path, 'rb'), 'image/jpg', {'Expires': '0'})
    }
    data = {
        'user_id': user_id,
        'filename': image_type
    }
    result = requests.put(url=url_api, files=files, data=data)
    response = result.json()
    recycle_type_id = response.get('Id', None)  # Recognized type id from OpenRecycle database
    logging.info('Recognized: %s' % recycle_type_id)  # Db of all id's
    return recycle_type_id  # https://github.com/openrecycle/open_data/blob/master/waste_db.csv


def contents_type():
    image = make_photo()
    #recognized_type = upload_to_web(image)
    time.sleep(2)
    if fake == 1:
        return '16'
    elif fake == 0:
        return '38'


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

    if (distance > 37) or (distance < 29):
        here = True
    else:
        here = False
    return here


def something_in():
    really = True
    k = 0
    for i in range(30):
        if sonic_check():
            k += 1
    if k < 5:
        really = False
    return really


def user_reg(user_id):
    user_url = 'http://smartbin35.ru.mastertest.ru/api/checkuser?cardCode=' + user_id
    response = urllib.request.urlopen(user_url)
    user_status = response.read()
    if user_status == b'true':
        return True
    else:
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
    time.sleep(10)
    close_lock()
    while True:
        GPIO.output(GREEN, 0)
        GPIO.output(RED, 0)
        GPIO.output(BLUE, 1)
        close_up()
        close_down()

        user = check_rfid()
        if user == "":
            continue

        beep()

        if user == "5605B8DF7642":
            open_lock()
            logging.info("The bin is opened for maintenance")
            while True:
                time.sleep(5)

        try:
            reg_stat = user_reg(user)
        except:
            time.sleep(1)
            UART.flushInput()
        if reg_stat:
            logging.info("User found")
            GPIO.output(BLUE, 0)
            GPIO.output(GREEN, 1)
            entry_time = time.time()
            time_exit = False
            find_exit = False

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
                if find_exit:
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
                        if inner_type == '16':
                            pet_down()
                            time.sleep(2.5)
                            close_down()
                            try:
                                reward(user, 'pet')
                            except:
                                time.sleep(0.5)
                            logging.info('Rewarded for pet!')
                        elif inner_type == '38':
                            al_down()
                            time.sleep(2.5)
                            close_down()
                            try:
                                reward(user, 'al')
                            except:
                                time.sleep(0.5)
                            logging.info('Rewarded for al!')
                        else:
                            GPIO.output(GREEN, 0)
                            GPIO.output(RED, 1)
                            open_up()
                            while something_in():
                                time.sleep(0.01)
                            time.sleep(1)
                            close_up()
                            time_exit = True
                            GPIO.output(RED, 0)
                    else:
                        GPIO.output(GREEN, 0)
                        time.sleep(0.2)
                        GPIO.output(RED, 1)
                        time.sleep(0.2)
                        GPIO.output(RED, 0)
                        time.sleep(0.2)
                        GPIO.output(RED, 1)
                        time.sleep(0.2)
                        GPIO.output(RED, 0)
                        time.sleep(0.2)
                        GPIO.output(RED, 1)
                        time.sleep(0.2)
                        GPIO.output(RED, 0)
                        time.sleep(0.2)
                        GPIO.output(GREEN, 1)
                        entry_time = time.time()

            logging.info("Session closed")
            time.sleep(0.5)
            UART.flushInput()
            logging.info('****************************')
        else:
            GPIO.output(GREEN, 0)
            GPIO.output(BLUE, 0)
            GPIO.output(RED, 1)
            time.sleep(0.5)
            GPIO.output(RED, 0)
            time.sleep(0.5)
            UART.flushInput()


finally:
    GPIO.cleanup()
    camera.close()
