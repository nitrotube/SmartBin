import logging
import serial

logging.basicConfig(format='%(levelname)s:%(message)s', level=logging.INFO)
UART = serial.Serial(
    port='/dev/serial0',
    baudrate=9600,
    parity=serial.PARITY_NONE,
    stopbits=serial.STOPBITS_ONE,
    bytesize=serial.EIGHTBITS,
    timeout=1
)


def check_rfid():
    code = ''
    while True:
        logging.info(UART.read(12))
        if UART.read() == b'\x02':
            code = UART.read(12)
            UART.flushInput()
            break

    logging.info(code.decode("utf-8"))
    return code.decode("utf-8")

check_rfid()