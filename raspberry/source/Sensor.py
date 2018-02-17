
import RPi.GPIO as GPIO
import time
import config

GPIO.setmode(GPIO.BOARD)

class Sensor:
	
	def __init__(self, trig, echo):
		self.trig = trig
		self.echo = echo
		GPIO.setup(trig, GPIO.OUT)
		GPIO.setup(echo, GPIO.IN)
		
	def getDistance(self):
	
		GPIO.output(self.trig, False)
		time.sleep(0.01)
		GPIO.output(self.trig, True)
		time.sleep(0.00001)
		GPIO.output(self.trig, False)
		
		while GPIO.input(self.echo) == 0:
			pulse_start = time.time()

		while GPIO.input(self.echo) == 1:
			pulse_end = time.time()

		pulse_duration = pulse_end - pulse_start
		dist = pulse_duration * 17150
		dist = round(dist, 2) - 0.5
		return dist
	
	def found(self):
		dist = self.getDistance()
		if (dist > 42) or (dist < 38):
			return True
		return False

	def cheat_check(self):
    		time.sleep(0.1)
    		k = 0
    		for i in range(30):
			if self.found():
				k += 1
			time.sleep(0.001)
		if k >= 3:
			return False
		return True
	
		
def test():
	sensor = Sensor(config.TRIG2, config.ECHO2)
	while 1:
		time.sleep(0.5)
		print("distance:")
		print(sensor.getDistance())
		if(sensor.found()):
			print("found")
		else:
			print("not found")
if (__name__ == "__main__"):
	test()
