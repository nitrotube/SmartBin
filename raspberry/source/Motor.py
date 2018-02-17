import config
import Adafruit_PCA9685
import time

class Motor:
	def __init__(self, port, up, down, pos):
		self.PORT = port
		self.pwm = Adafruit_PCA9685.PCA9685()
		self.pwm.set_pwm_freq(75)
		self.UP = up
		self.DOWN = down
		self.POSITION = pos

	def up(self):
		try:
			self.pwm.set_pwm(self.PORT, 0, self.UP)
			time.sleep(0.5)
		except:
			print("LOG: cannot open %s" % self.POSITION)
		
	def down(self):
		try:
			self.pwm.set_pwm(self.PORT, 0, self.DOWN)
			time.sleep(0.5)
		except:
			print("LOG: cannot close %s"%(self.POSITION))

def test():
	m = Motor(config.UP_SERVO, config.OPEN_UP, config.CLOSE_UP, "UP")
	m.up()
	print("Up success")
	m.down()
	print("Down success")

if __name__=="__main__":
	test()
