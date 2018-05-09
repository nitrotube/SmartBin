from serial import *
import time
import config as cfg

class LedsControl:
    def __init__(self):
        self.serial = Serial(cfg.ARDUINO_SERIAL_PORT)

    def set(self, state):
        self.serial.write(bytes(state))

'''serial = Serial('/dev/ttyACM0')
print(serial.name)
while True:
    inp = raw_input()
    if inp == 'q':
        serial.close()
        break
    if( not inp):
        inp = '0'
    serial.write(inp)
    print(ord(serial.read()))
    time.sleep(1)'''
