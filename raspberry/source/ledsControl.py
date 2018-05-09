from serial import *
import time
import config as cfg

class LedsControl:
    def __init__(self, port):
        self.serial = Serial(port)

    def set(self, state):
        self.serial.write(bytes(state))
