import RPi.GPIO as GPIO
import time
import Adafruit_PCA9685
import picamera
import logging
import datetime
import serial
import os


TRIG = 31
ECHO = 29

GPIO.setmode(GPIO.BOARD)
GPIO.setup(TRIG, GPIO.OUT)
GPIO.setup(ECHO, GPIO.IN)
GPIO.setup(12, GPIO.OUT)  # Beeper

camera = picamera.PiCamera()
logging.basicConfig(format='%(levelname)s:%(message)s', level=logging.INFO)  # Setting up logging

INNER = 15
GPIO.setup(INNER, GPIO.OUT)

#16, 18 - upper
# 33, 35 - down glass, 29,31 - down back

pwm = Adafruit_PCA9685.PCA9685()
UP_SERVO = 3  # Upper servo pin
DOWN_SERVO = 2  # Down servo pin

OPEN_UP = 200  # Positions of servo
CLOSE_UP = 415
CLOSE_DOWN = 310
PET_DOWN = 520
AL_DOWN = 150

def getTypeLitter(path):
	ip = '192.168.0.225'
	os.system('cp empty.txt type.txt')
	os.system('sshpass -p nebobr scp empty.txt nitrotube@' + ip + ':/Users/nitrotube/tensorflow_hh/tf_files/type.txt')
	os.system('sshpass -p nebobr scp '  + path + ' nitrotube@' + ip + ':/Users/nitrotube/tensorflow_hh/tf_files/temp/')
	res = open('type.txt').readline()

	while (not res):
		os.system('sshpass -p nebobr scp nitrotube@' + ip + ':/Users/nitrotube/tensorflow_hh/tf_files/type.txt type.txt')
		res = open('type.txt').readline()

	return res.split()[0]


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


def make_photo():
    GPIO.output(INNER, 1)
    image_time = datetime.datetime.now()  # Making a unique name of a string from datetime
    image_time = str(image_time)
    image_time = image_time[0:4] + image_time[5:7] + image_time[8:10] + image_time[11:13] + image_time[14:16] + image_time[17:19]
    image_path = '/home/pi/Documents/Photos/' + image_time + '.jpeg'
    camera.resolution = (640, 480)
    camera.brightness = 35
    camera.contrast = 50
    camera.capture(image_path, use_video_port=True)
    GPIO.output(INNER, 0)
    return image_path


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
    #print(distance)

    if (distance > 42) or (distance < 38):
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
        time.sleep(0.03)
    if k < 5:
        really = False
    return really


UART = serial.Serial(
    port='/dev/serial0',
    baudrate=9600,
    parity=serial.PARITY_NONE,
    stopbits=serial.STOPBITS_ONE,
    bytesize=serial.EIGHTBITS,
    timeout=1
)


try:
    while True:
        GPIO.output(12, 0)
        time.sleep(0.2)
        close_up()
        close_down()
        if check_rfid() != "":
            print("Found user")
            GPIO.output(12, 1)
            time.sleep(0.2)
            GPIO.output(12, 0)
            open_up()
            while not(something_in()):
                time.sleep(0.1)
            print("Found bottle")
            close_up()
            time.sleep(1)
            GPIO.output(INNER, 1)
            image_path = make_photo()
            logging.info(image_path)

            trash_type = getTypeLitter(image_path)

            if trash_type == "pet":
                print("Plastic bottle")
                #os.system("mplayer /home/pi/Documents/plastik.mp3")
                al_down()
                time.sleep(1.5)
                close_down()
            elif trash_type == "al":
                print("Aluminium bottle")
                #os.system("mplayer /home/pi/Documents/alu.mp3")
                pet_down()
                time.sleep(1.5)
                close_down()
            else:
                GPIO.output(INNER, 0)
                print("Unrecognized type of litter")
                #os.system("mplayer /home/pi/Documents/unknown.mp3")
                open_up()
                while something_in():
                    time.sleep(0.3)
                time.sleep(1)
                close_up()

            time.sleep(1)
            GPIO.output(INNER, 0)
            UART.flushInput()
            print("Session closed")


finally:
    GPIO.cleanup()
