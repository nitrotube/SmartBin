import config as cfg
import time
import requests
import socket
import Adafruit_PCA9685
import email_warning as email

class Session():
    def __init__(self, container, user):
        self.container = container
        self.user = user
        self.score = 0
        self.pwm = Adafruit_PCA9685.PCA9685()
        self.pwm.set_pwm_freq(75)

    def getClass(self, path):

        host = cfg.HOST
        port = cfg.PORT

        client = socket.socket()
        client.connect((host, port))

        data = open(path, 'rb').read()
        data += b'\r\n\r\n'
        client.send(data)

        response = client.recv(1024).decode('utf-8')
        client.close()

        return response

    def foundUser(self):
        user_url = 'http://smartbin35.ru.mastertest.ru/api/checkuser?cardCode=' + self.user
        response = requests.get(user_url)
        user_status = response.text
        if user_status == b'true':
            return True
        return False


    def rewardUser(self, trash_type):
        reward_url = 'http://smartbin35.ru.mastertest.ru/api/bonus?cardCode=' + self.user
        reward_url = reward_url + '&trashType=' + trash_type + '&trashId=2'
        response = requests.get(reward_url)
        return response

    def finalReward(self):
        if(not self.score):
            return
        self.container.player.play_reward(self.score)
        self.container.leds.set(cfg.LEDS_REWARD)
        time.sleep(3)

    def getType(self):
        img = self.container.camera.make_photo()
        type = self.getClass(img)
        return type

    def LightOn(self):
        self.pwm.set_pwm(cfg.LED_INNER1, 0, cfg.LED_MAX_VAL)
        self.pwm.set_pwm(cfg.LED_INNER2, 0, cfg.LED_MAX_VAL)
    
    def LightOff(self):
        self.pwm.set_pwm(cfg.LED_INNER1, 0, 0)
        self.pwm.set_pwm(cfg.LED_INNER2, 0, 0)

    def adminSession(self):
        self.container.beeper.beep()
        self.container.lock.go(cfg.MOTOR_STATE_LOCK_OPEN)
        self.container.pet = 0
        self.container.al = 0
        while True:
            if(self.container.scanner.hasCode()):
                if(self.container.scanner.getCode() == self.user):
                    break
        self.container.lock.go(cfg.MOTOR_STATE_LOCK_CLOSE)

    def bottleSession(self):
        self.container.beeper.beep()
        self.container.top.go(cfg.MOTOR_STATE_TOP_OPEN)
        sessionStart = time.time()
        while(not self.container.smthIn()):
            if(time.time() - sessionStart > 6):
                self.container.top.go(cfg.MOTOR_STATE_TOP_CLOSE)
                return False
        self.container.top.go(cfg.MOTOR_STATE_TOP_CLOSE)
        if(not self.container.smthIn()):
            return False
        type = self.getType()
        if(type == "pet"):
            self.container.sort.go(cfg.MOTOR_STATE_SORT_PET)
            self.container.sort.go(cfg.MOTOR_STATE_SORT_DEFAULT)
            self.container.player.play_sound(cfg.PET)
            self.rewardUser("pet")
            self.score += 8
            self.container.pet += 1
        elif(type == "al"):
            self.container.sort.go(cfg.MOTOR_STATE_SORT_ALUM)
            self.container.sort.go(cfg.MOTOR_STATE_SORT_DEFAULT)
            self.container.player.play_sound(cfg.ALUM)
            self.rewardUser("al")
            self.score += 5
            self.container.al += 1
        else:
            self.container.leds.set(cfg.LEDS_WARNING)
            self.container.player.play_sound(cfg.ERR)
            self.container.top.go(cfg.MOTOR_STATE_TOP_OPEN)
            while(self.container.smthIn()):
                self.container.top.go(cfg.MOTOR_STATE_TOP_OPEN)
                while(self.container.smthIn()):
                    self.container.beeper.beep()
                self.container.top.go(cfg.MOTOR_STATE_TOP_CLOSE)
                time.sleep(1)
            return False
        if(self.container.full()):
            return False
        return True

    def run(self):
        if(not self.foundUser()):
            self.container.leds.set(cfg.LEDS_WARNING)
            delay(3)
            self.container.leds.set(cfg.LEDS_WAITING)
            return
        self.LightOn()
        k = 0
        if(self.user in cfg.ADMINS):
            startTime = time.time()
            while(startTime + 1.0 > time.time()):
                if(not self.container.scanner.hasCode()):
                    continue
                tmp = self.container.scanner.getCode()
                if(tmp == self.user):
                    k+=1
        if(self.user in cfg.ADMINS and k>=8):
            self.container.leds.set(cfg.LEDS_SESSION)
            self.adminSession()
        elif(not self.container.full()):
            self.container.leds.set(cfg.LEDS_SESSION)
            while(self.bottleSession()):
                pass
            time.sleep(1)
            self.finalReward()
        self.container.scanner.UART.flushInput()
        if(self.container.full()):
            self.container.leds.set(cfg.LEDS_WARNING)
            email.send_warn_full()
        else:
            self.container.leds.set(cfg.LEDS_WAITING)
        self.LightOff()
