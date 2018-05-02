import RPi.GPIO as GPIO
from arduino import Arduino
from motor import Motor
from beeper import Beeper
from sensor import Sensor
from player import Player
from camera import Camera
from RFID_Scanner import RFID_Scanner
import config as cfg
import time

class Container:

    def __init__(self):
		#GPIO.cleanup()
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
        
        # ARDUINO
        #self.arduino = Arduino()

        self.beeper = Beeper(cfg.BEEPER)
        self.top.go(cfg.MOTOR_STATE_TOP_CLOSE)
        self.sort.go(cfg.MOTOR_STATE_SORT_DEFAULT)
        self.lock.go(cfg.MOTOR_STATE_LOCK_CLOSE)
        #self.arduino.write(cfg.TURN_ON)
        self.sens1 = Sensor(cfg.SENS1_TRIG, cfg.SENS1_ECHO, cfg.SENS_RANGE)
        self.sens2 = Sensor(cfg.SENS2_TRIG, cfg.SENS2_ECHO, cfg.SENS_RANGE)
        self.sens3 = Sensor(cfg.SENS3_TRIG, cfg.SENS3_ECHO, cfg.SENS_RANGE)
        self.player = Player()
        self.camera = Camera(cfg.CAMERA)
        self.scanner = RFID_Scanner(cfg.UART_PORT)

    def printDistances(self):
        print(self.sens1.getDistance())
        print(self.sens2.getDistance())
        print(self.sens3.getDistance())
    def smthIn(self):
        return self.sens1.found() or self.sens2.found() or self.sens3.found()

def test():
    cont = Container()
    #cont.sort.go(cfg.MOTOR_STATE_SORT_DEFAULT)
    '''while(1):
        print(cont.sens1.found())
        print(cont.sens2.found())
        print(cont.sens3.found())
        print('------------')
        time.sleep(0.5)''' # Sensors

    # cont.player.play_sound(cfg.ALUM)
    #print(cont.camera.make_photo())
    while(True & 0):
        if(cont.scanner.hasCode()):
            print(cont.scanner.readCode())
        time.sleep(0.7)
    while (True & 0):
        cont.sort.go(cfg.MOTOR_STATE_SORT_ALUM)    
        time.sleep(2)
        cont.sort.go(cfg.MOTOR_STATE_SORT_PET)
        time.sleep(2)
    cont.lock.go(cfg.MOTOR_STATE_LOCK_OPEN)
    time.sleep(2)
    cont.lock.go(cfg.MOTOR_STATE_LOCK_CLOSE)
    

if(__name__ == "__main__"):
	test()
