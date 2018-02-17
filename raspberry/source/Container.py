import RPi.GPIO as GPIO
from Motor import Motor
from Beeper import Beeper
from Sensor import Sensor
from Player import Player
from Camera import Camera
from PassScaner import PassScaner
import config as cfg


class Container:
	
	def __init__(self):
		#GPIO.cleanup()
		self.inner = Sensor(cfg.TRIG2, cfg.ECHO2)
		self.player = Player()
		self.top = Motor(cfg.UP_SERVO, cfg.OPEN_UP, cfg.CLOSE_UP, "TOP")
		self.bott1 = Motor(cfg.LOCK1_SERVO, cfg.LOCK1_OPEN, cfg.LOCK1_CLOSE, "BOOTOM1")
		self.bott2 = Motor(cfg.LOCK2_SERVO, cfg.LOCK2_OPEN, cfg.LOCK2_CLOSE, "BOTTOM2")
		self.alum = Motor(cfg.DOWN_SERVO, cfg.AL_DOWN, cfg.CLOSE_DOWN, "ALUMINIUM")
		self.pet = Motor(cfg.DOWN_SERVO, cfg.PET_DOWN, cfg.CLOSE_DOWN, "PET")
		self.camera = Camera(cfg.INNER)
		self.scaner = PassScaner()
		self.beeper = Beeper(cfg.BEEPER)
		self.checker = Sensor(cfg.TRIG3, cfg.ECHO3)
		
		self.top.down()
		self.bott1.down()
		self.bott2.down()
		self.top.down()
		self.alum.down()
		self.beeper.off()
		
	def smthIn(self):
		return self.inner.found() and self.checker.cheat_check()
	
if(__name__=="__main__"):
	t = Container()
