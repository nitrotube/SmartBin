import serial
import Adafruit_PCA9685
import config as cfg

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
            return ""
        res = self.CODE
        self.CODE = ""
        return res

    def hasCode(self):
        if(self.CODE == ""):
            self.readCode()
            return False
        else:
            return True

def test():
    s = RFID_Scanner(cfg.UART_PORT)
if __name__ == "__name__":
    test()
