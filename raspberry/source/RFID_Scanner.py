import serial
import Adafruit_PCA9685
import config as cfg
import time

class RFID_Scanner:
    def __init__(self, port):
        pwm = Adafruit_PCA9685.PCA9685()
        pwm.set_pwm_freq(75)
        pwm.set_pwm(cfg.SCANNER_LED, 0, 4000)
        self.UART = serial.Serial(
            port=port,
            baudrate=9600,
            parity=serial.PARITY_NONE,
            stopbits=serial.STOPBITS_ONE,
            bytesize=serial.EIGHTBITS,
            timeout=1
        )
        self.CODE = ""

    def readCode(self):
        if(self.CODE == ""):
            if(self.UART.read() == b'\x02'):
                self.CODE = self.UART.read(12).decode("utf-8")
            else:
                self.CODE = ""
            self.UART.flushInput()
        return self.CODE

    def getCode(self):
        r = self.CODE
        self.CODE = ""
        return r

    def hasCode(self):
        self.readCode()
        if(self.CODE != ""):
            return True
        return False

def test():
    s = RFID_Scanner(cfg.UART_PORT)
    while 1:
        if(not s.hasCode()):
            continue
        k = 0
        code = s.getCode()
        t1 = time.time()
        print(t1)
        while(t1 + 1.0 > time.time()):
            if(s.hasCode()):
                tmp = s.getCode()
                if(tmp == code):
                    k+=1
        print(k)
if __name__ == "__main__":
    test()
