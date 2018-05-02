from serial import Serial
import sys
class Arduino:
    
    def __init__(self):
        self.arduino = Serial('/dev/ttyACM0', 9600)

    def sendCmd(self, cmd):
        self.arduino.write(str(cmd))
        return self.read()
    
    def read(self):
        return self.arduino.read()

def test():
    a = Arduino()
    while True:
        cmd = sys.stdin.readline()
        print(a.sendCmd(cmd))

if(__name__=="__main__"):
    test()
