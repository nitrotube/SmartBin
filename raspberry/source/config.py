# Motor states
# TOP
MOTOR_STATE_TOP_OPEN = 0
MOTOR_STATE_TOP_CLOSE = 1
# SORT
MOTOR_STATE_SORT_DEFAULT = 0
MOTOR_STATE_SORT_ALUM = 1
MOTOR_STATE_SORT_PET = 2
# LOCK
MOTOR_STATE_LOCK_CLOSE = 0
MOTOR_STATE_LOCK_OPEN = 1

# Motor pins
# TOP
MOTOR_PIN_TOP = 12
# SORT
MOTOR_PIN_SORT = 8
# LOCK
MOTOR_PIN_LOCK1 = 0
MOTOR_PIN_LOCK2 = 4

# Motor values
# TOP
MOTOR_VAL_TOP_OPEN = 150
MOTOR_VAL_TOP_CLOSE = 520
# SORT
MOTOR_VAL_SORT_DEFAULT = 525
MOTOR_VAL_SORT_PET = 795
MOTOR_VAL_SORT_ALUM = 200
# LOCK
MOTOR_VAL_LOCK1_CLOSE = 480
MOTOR_VAL_LOCK1_OPEN = 405
MOTOR_VAL_LOCK2_CLOSE = 350
MOTOR_VAL_LOCK2_OPEN = 423

# Periphery
BEEPER = 11

# Commands
TURN_ON = 100

# LEDS
LED_INNER1 = 5
LED_INNER2 = 7
LED_STRIP = 6
LED_MAX_VAL = 4000

# UART
UART_PORT = '/dev/serial0'

# SENSORS
SENS1_ECHO = 31
SENS1_TRIG = 29
SENS2_ECHO = 35
SENS2_TRIG = 33
SENS3_ECHO = 38
SENS3_TRIG = 36
SENS_RANGE = (37, 45)

# DATA
ALUM = 'alum'
PET = 'pet'
ERR = 'err'

# BOTTLES
MAX_PET = 3
MAX_AL = 30

# Sound player
SOUNDS = {
    PET:'/home/pi/pywork/sounds/plastic.mp3',
    ALUM:'/home/pi/pywork/sounds/al.mp3',
    ERR:'/home/pi/pywork/sounds/unknown.mp3'
}
SOUNDS_BASE_DIR = '/home/pi/pywork/sounds/'

# CAMERA
CAMERA =  13
CAMERA_PATH_PHOTO = '/home/pi/pywork/new/new_photos/'

# AI
HOST = '192.168.0.133'
PORT = 5000

# ADMINS
ADMINS = set(['5605B8DF7642', '7800807D0782'])

# LEDS
# INNER LEDS
LED1_PIN = 5
LED2_PIN = 7

# SCANNER LED
SCANNER_LED = 6

# ARDUINO 
ARDUINO_SERIAL_PORT = '/dev/ttyACM0'

# LED STATES
LEDS_SAME = 0
LEDS_WAITING = 1
LEDS_WARNING = 2
LEDS_FATAL_ERR = 3
LEDS_SESSION = 4
LEDS_REWARD = 5

# EMAIL
EMAIL = {
    "server" : "smtp.gmail.com",
    "port" : "587",
    "login" : "smartbin.warner@gmail.com",
    "password" : "SBWarner2018",
    "to" : "e.spirin@smartbin.ru",
}
