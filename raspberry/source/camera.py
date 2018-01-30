import picamera
import logging
import datetime
import RPi.GPIO as GPIO
import time

INNER = 38
GPIO.setmode(GPIO.BOARD)
GPIO.setup(INNER, GPIO.OUT)

camera = picamera.PiCamera()
logging.basicConfig(format='%(levelname)s:%(message)s', level=logging.DEBUG)  # Setting up logging


def make_photo():
    GPIO.output(INNER, 1)
    image_time = datetime.datetime.now()  # Making a unique name of a string from datetime
    image_time = str(image_time)
    image_time = image_time[0:4] + image_time[5:7] + image_time[8:10] + image_time[11:13] + image_time[14:16] + image_time[17:19]
    image_path = '/home/pi/Documents/Photos/' + image_time + '.jpeg'
    camera.resolution = (640, 480)
    camera.brightness = 60
    camera.capture(image_path, use_video_port=True)
    GPIO.output(INNER, 0)
    return image_path

for i in range(1):
    time.sleep(0.7)
    image_path = make_photo()
    logging.info(image_path)
