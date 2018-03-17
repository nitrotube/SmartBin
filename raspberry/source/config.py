# PINS
BEEPER = 11

UP_SERVO = 0 # Servo pins
DOWN_SERVO = 1
LOCK1_SERVO = 2
LOCK2_SERVO = 3

# SERVO
OPEN_UP = 160  # Positions of servo
CLOSE_UP = 407
CLOSE_DOWN = 395
PET_DOWN = 650
AL_DOWN = 170
LOCK1_CLOSE = 480
LOCK1_OPEN = 405
LOCK2_CLOSE = 350
LOCK2_OPEN = 423

RED = 5 # Led pins
GREEN = 6
BLUE = 7
INNER = 13


TRIG1 = 29  # Distance sensors pins (bottle detection)
ECHO1 = 31  # Glass
TRIG2 = 33  # Back
ECHO2 = 35

TRIG3 = 36  # Distance sensors pins (hand check)
ECHO3 = 38

AL_LIMIT = 35
PET_LIMIT = 25

WAIT_LIMIT = 7

PATH = {
    "BASE_DIR" : "/home/pi/pywork",
}

EMAIL = {
    "server" : "smtp.gmail.com",
    "port" : "587",
    "login" : "smartbin.warner@gmail.com",
    "password" : "SBWarner2018",
    "to" : "e.spirin@smartbin.ru",
}
