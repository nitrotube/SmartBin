import config
import Adafruit_PCA9685
import time
import config as cfg

class Motor:
    def __init__(self, pos):
        self.pwm = Adafruit_PCA9685.PCA9685()
        self.pwm.set_pwm_freq(75)
        self.position = pos
        self.states = {}

    def addState(self, state, ports_vals):
        self.states.update({state : ports_vals})

    def go(self, state):
        for var in self.states[state]:
            self.pwm.set_pwm(var[0], 0, var[1])

def test():
    '''motor = Motor("TOP")
    motor.addState(cfg.MOTOR_STATE_TOP_OPEN, [(cfg.MOTOR_PIN_TOP, cfg.MOTOR_VAL_TOP_OPEN)])
    motor.addState(cfg.MOTOR_STATE_TOP_CLOSE, [(cfg.MOTOR_PIN_TOP, cfg.MOTOR_VAL_TOP_CLOSE)])
    motor.go(cfg.MOTOR_STATE_TOP_OPEN)'''

    motor = Motor("SORTER")
    motor.addState(cfg.MOTOR_STATE_SORT_DEFAULT, [(cfg.MOTOR_PIN_SORT, cfg.MOTOR_VAL_SORT_DEFAULT)])
    motor.addState(cfg.MOTOR_STATE_SORT_ALUM, [(cfg.MOTOR_PIN_SORT, cfg.MOTOR_VAL_SORT_ALUM)])
    motor.go(cfg.MOTOR_STATE_SORT_ALUM)
    time.sleep(2)
    motor.go(cfg.MOTOR_STATE_SORT_DEFAULT)

if __name__=="__main__":
    mot = Motor("w")

