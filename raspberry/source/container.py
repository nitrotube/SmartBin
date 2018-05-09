import RPi.GPIO as GPIO
from motor import Motor
from beeper import Beeper
from sensor import Sensor
from player import Player
from camera import Camera
from ledsControl import LedsControl
from RFID_Scanner import RFID_Scanner
import config as cfg
import time

class Container:

    def __init__(self):
        # BOTTLES
        self.pet = 0
        self.al = 0
        # TOP
        self.top = Motor("TOP")
        self.top.addState(cfg.MOTOR_STATE_TOP_OPEN, [(cfg.MOTOR_PIN_TOP, cfg.MOTOR_VAL_TOP_OPEN)])
        self.top.addState(cfg.MOTOR_STATE_TOP_CLOSE, [(cfg.MOTOR_PIN_TOP, cfg.MOTOR_VAL_TOP_CLOSE)])
        # LOCK
        self.lock = Motor("LOCK")
        self.lock.addState(cfg.MOTOR_STATE_LOCK_CLOSE, \
            [
                (cfg.MOTOR_PIN_LOCK1, cfg.MOTOR_VAL_LOCK1_CLOSE),
                (cfg.MOTOR_PIN_LOCK2, cfg.MOTOR_VAL_LOCK2_CLOSE)
            ])
        self.lock.addState(cfg.MOTOR_STATE_LOCK_OPEN, \
            [
                (cfg.MOTOR_PIN_LOCK1, cfg.MOTOR_VAL_LOCK1_OPEN),
                (cfg.MOTOR_PIN_LOCK2, cfg.MOTOR_VAL_LOCK2_OPEN)
            ])

        # SORT
        self.sort = Motor("SORTER")
        self.sort.addState(cfg.MOTOR_STATE_SORT_DEFAULT, [(cfg.MOTOR_PIN_SORT, cfg.MOTOR_VAL_SORT_DEFAULT)])
        self.sort.addState(cfg.MOTOR_STATE_SORT_ALUM, [(cfg.MOTOR_PIN_SORT, cfg.MOTOR_VAL_SORT_ALUM)])
        self.sort.addState(cfg.MOTOR_STATE_SORT_PET, [(cfg.MOTOR_PIN_SORT, cfg.MOTOR_VAL_SORT_PET)])
        
        # LEDS
        self.leds = LedsControl(cfg.ARDUINO_SERIAL_PORT)

        self.beeper = Beeper(cfg.BEEPER)
        self.top.go(cfg.MOTOR_STATE_TOP_CLOSE)
        self.sort.go(cfg.MOTOR_STATE_SORT_DEFAULT)
        self.lock.go(cfg.MOTOR_STATE_LOCK_CLOSE)
        self.sens1 = Sensor(cfg.SENS1_TRIG, cfg.SENS1_ECHO, cfg.SENS_RANGE)
        self.sens2 = Sensor(cfg.SENS2_TRIG, cfg.SENS2_ECHO, cfg.SENS_RANGE)
        self.sens3 = Sensor(cfg.SENS3_TRIG, cfg.SENS3_ECHO, cfg.SENS_RANGE)
        self.player = Player()
        self.camera = Camera(cfg.CAMERA)
        self.scanner = RFID_Scanner(cfg.UART_PORT)
        self.leds.set(cfg.LEDS_WAITING)

    def printDistances(self):
        print(self.sens1.getDistance())
        print(self.sens2.getDistance())
        print(self.sens3.getDistance())

    def smthIn(self):
        return self.sens1.found() or self.sens2.found() or self.sens3.found()
    
    def full(self):
        return self.pet >= cfg.MAX_PET or self.al >= cfg.MAX_AL

def test():
    cont = Container()

if(__name__ == "__main__"):
	test()
