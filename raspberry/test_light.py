import Adafruit_PCA9685
import time
pwm = Adafruit_PCA9685.PCA9685()

RED = 8
GREEN = 9
BLUE = 10

CurGreen = 4000
CurRed = 100
CurBlue = 1000

pwm.set_pwm_freq(75)
pwm.set_pwm(RED, 0, 0)
pwm.set_pwm(GREEN, 0, 0000)
pwm.set_pwm(BLUE, 0, 000)


