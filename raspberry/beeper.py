import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BOARD)

GPIO.setup(32, GPIO.OUT)

GPIO.output(32, 0)
time.sleep(0.5)
GPIO.output(32, 1)
time.sleep(5)
GPIO.cleanup()
