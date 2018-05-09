from serial import Serial
import sys
class Arduino:
    
    def __init__(self):
        self.arduino = Serial('/dev/ttyACM0', 9600)

    def setState(self, st):
        self.arduino.write(st)
        return self.read()
    
    def read(self):
        return self.arduino.read()

def test():
    a = Arduino()
    while True:
        cmd = sys.stdin.readline()
        if(ord(cmd[0]) == ord('w')):
            a.setState('1')
        elif(ord(cmd[0]) == ord('f')):
            a.setState('3')
        else:
            print('Invalid state')

if(__name__=="__main__"):
    test()
