import serial
import time

UART = serial.Serial(
    port='/dev/serial0',
    baudrate=9600,
    parity=serial.PARITY_NONE,
    stopbits=serial.STOPBITS_ONE,
    bytesize=serial.EIGHTBITS,
    timeout=1
)

while True:
    buffer = UART.read()
    ID = ""
    if buffer == b'\x02':
        for Counter in range(13):
            buffer = UART.read()
            ID = ID + buffer.decode('utf-8')
        ID = ID.replace('\x03', '')
        print(ID)

        time.sleep(1)
        UART.flushInput()
