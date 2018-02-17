import picamera
import RPi.GPIO as GPIO
import config as cfg
import datetime
class Camera:
	
	def __init__(self, port):
		self.PORT = port
		GPIO.setmode(GPIO.BOARD)
		GPIO.setup(cfg.INNER, GPIO.OUT)
		GPIO.output(port, 0)
		self.device = picamera.PiCamera()
	
	def make_photo(self):
		GPIO.output(self.PORT, 1)
		image_time = datetime.datetime.now()  # Making a unique name of a string from datetime
		image_time = str(image_time)[:19].replace(' ', '').replace('-', '').replace(':', '')
		image_path = '/home/pi/pywork/new/new_photos/' + image_time + '.jpeg'
		self.device.resolution = (640, 480)
		self.device.brightness = 60
		self.device.contrast = 55
		self.device.capture(image_path, use_video_port=True)
		GPIO.output(self.PORT, 0)
		return image_path

def test():
	cam = Camera(cfg.INNER)
	print(cam.make_photo())

if(__name__=="__main__"):
	test()
