# PINS
BEEPER = 11

UP_SERVO = 0 # Servo pins
DOWN_SERVO = 8
LOCK1_SERVO = 2
LOCK2_SERVO = 12

# SERVO
OPEN_UP = 180  # Positions of servo
CLOSE_UP = 423
CLOSE_DOWN = 380
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

AL_LIMIT = 45
PET_LIMIT = 35

WAIT_LIMIT = 6

authorised_Users = ["5605B8DF7642*", "6900338C7FA9"]
set(authorised_Users)

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
