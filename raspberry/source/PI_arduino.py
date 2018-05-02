from serial import *
import time
arduino_usb = Serial('/dev/ttyACM0')
print(arduino_usb.name)
while True:
	cmd = input()
	if cmd == 'q':
		arduino_usb.close()
		break
	arduino_usb.write(b'hello')
	print(arduino_usb.read())
	#time.sleep(1)
