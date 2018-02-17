import RPi.GPIO as GPIO
import time

class Beeper:
	def __init__(self, port):
		self.PORT = port
		GPIO.setmode(GPIO.BOARD)
		GPIO.setup(self.PORT, GPIO.OUT)
		GPIO.output(self.PORT, 0)

	def on(self):
		GPIO.output(self.PORT, 1)

	def off(self):
		GPIO.output(self.PORT, 0)

	def beep(self, timer=0.3):
		GPIO.output(self.PORT, 1)
		time.sleep(timer)
		GPIO.output(self.PORT, 0)
