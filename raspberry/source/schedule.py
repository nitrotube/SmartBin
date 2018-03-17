import datetime


def check_silence():
    result = False
    b1 = datetime.time(8, 30)
    f1 = datetime.time(9, 10)
    b2 = datetime.time(9, 20)
    f2 = datetime.time(10, 0)
    b3 = datetime.time(10, 10)
    f3 = datetime.time(10, 50)
    b4 = datetime.time(11, 10)
    f4 = datetime.time(11, 50)
    b5 = datetime.time(12, 10)
    f5 = datetime.time(12, 50)
    b6 = datetime.time(13, 0)
    f6 = datetime.time(13, 40)
    b7 = datetime.time(13, 50)
    f7 = datetime.time(14, 30)
    p7 = datetime.time(14, 10)
    p7 = datetime.time(14, 50)
    if (datetime.datetime.now().time() > b1) and (datetime.datetime.now().time() < f1):
        result = True
    if (datetime.datetime.now().time() > b2) and (datetime.datetime.now().time() < f2):
        result = True
    if (datetime.datetime.now().time() > b3) and (datetime.datetime.now().time() < f3):
        result = True
    if (datetime.datetime.now().time() > b4) and (datetime.datetime.now().time() < f4):
        result = True
    if (datetime.datetime.now().time() > b5) and (datetime.datetime.now().time() < f5):
        result = True
    if (datetime.datetime.now().time() > b6) and (datetime.datetime.now().time() < f6):
        result = True
    if (datetime.datetime.now().time() > p7) and (datetime.datetime.now().time() < f7) and (datetime.datetime.today().weekday() == 0):
        result = True
    if (datetime.datetime.now().time() > b7) and (datetime.datetime.now().time() < f7) and (datetime.datetime.today().weekday() == 0):
        result = True
    return result
