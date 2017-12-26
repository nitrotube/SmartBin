import picamera
import logging
import datetime
import requests
import time
import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BOARD)
INNER = 38
GPIO.setup(INNER, GPIO.OUT)
GPIO.output(INNER, 1)
time.sleep(0.1)

camera = picamera.PiCamera()
logging.basicConfig(format='%(levelname)s:%(message)s', level=logging.DEBUG)  # Setting up logging


def make_photo():
    image_time = datetime.datetime.now()  # Making a unique name of a string from datetime
    image_time = str(image_time)
    image_time = image_time[0:4] + image_time[5:7] + image_time[8:10] + image_time[11:13] + image_time[14:16] + image_time[17:19]
    image_path = '/home/pi/Documents/Photos/' + image_time + '.jpeg'
    camera.brightness = 85
    camera.contrast = 90
    camera.saturation = -20
    camera.resolution = (299, 299)
    camera.capture(image_path, use_video_port=True)
    return image_path


def upload_to_web(image_path):
    URL_API = 'http://217.71.231.9:48777/api/UploadFile4Recognition'
    USER_ID = 'SmartBin'
    IMAGE_TYPE = 'garbage'

    files = {
        'file': ('image.jpg', open(image_path, 'rb'), 'image/jpg', {'Expires': '0'})
    }
    data = {
        'user_id': USER_ID,
        'filename': IMAGE_TYPE
    }
    result = requests.put(url=URL_API, files=files, data=data)
    ## TODO return error if response.status_code != 200
    response = result.json()
    recycle_type_id = response.get('Id', None)  # Recognized type id from OpenRecycle database
    logging.info('Recognized: %s' % recycle_type_id)  # Db of all id's
    return recycle_type_id  # https://github.com/openrecycle/open_data/blob/master/waste_db.csv

start = time.time()
image_path = make_photo()
logging.info(image_path)
type_id = upload_to_web(image_path)
finish = time.time()
logging.info(finish - start)
camera.close()
GPIO.cleanup()