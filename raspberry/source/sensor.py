
import RPi.GPIO as GPIO
import time
import config as cfg


class Sensor:
    # initialize the sensor
    # trig is a TRIGGER PIN
    # echo is an ECHO PIN
    # distance_range is a tuple of two states (MIN distance found, MAX distance found)
    def __init__(self, trig, echo, distance_range):
        self.trig = trig
        self.echo = echo
        self.min = distance_range[0]
        self.max = distance_range[1]
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

    def fastFound(self):
        dist = self.getDistance()
        return dist < self.min

    def found(self):
        k = 0
        for i in range(15):
            if (self.fastFound()):
                k += 1
            time.sleep(0.005)
        return k>=5

def test():
    pass
if (__name__ == "__main__"):
    test()
