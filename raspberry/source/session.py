import config as cfg
import time
import requests
import socket

class Session():
	def __init__(self, container, user):
		self.container = container
		self.user = user

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


	def getType(self):
		img = self.container.camera.make_photo()
		type = self.getClass(img)
		return type

	def adminSession(self):
        self.comtainer.beeper.beep()
		self.container.lock.go(cfg.MOTOR_STATE_LOCK.OPEN)
        time.sleep(0.5)
		while True:
			if(self.container.scaner.hasCode()):
				if(self.container.scaner.readCode() == self.user):
					break
		self.container.lock.go(cfg.MOTOR_STATE_LOCK_CLOSE)

	def bottleSession(self):
		self.container.top.go(cfg.MOTOR_STATE_TOP_OPEN)
		sessionStart = time.time()
		while(not self.container.smthIn()):
			if(time.time() - sessionStart > 6):
				self.container.top.go(cfg.MOTOR_STATE_TOP_CLOSE)
				return False
		self.container.top.go(cfg.MOTOR_STATE_TOP_CLOSE)
		type = self.getType()
		if(type == "pet"):
			self.container.sort.go(cfg.MOTOR_STATE_SORT_PET)
			self.container.sort.go(cfg.MOTOR_STATE_SORT_DEFAULT)
			self.container.player.play_sound(cfg.PET)
			rewardUser("pet")
		elif(type == "al"):
			self.container.sort.go(cfg.MOTOR_STATE_SORT_ALUM)
			self.container.sort.go(cfg.MOTOR_STATE_SORT_DEFAULT)
			self.container.player.play_sound(cfg.ALUM)
			rewardUser("al")
		else:
			self.container.player.play_sound(cfg.ERR)
			self.container.top.go(cfg.MOTOR_STATE_TOP_OPEN)
			while(self.container.smthIn()):
				pass
            time.sleep(1)
			self.container.top.go(cfg.MOTOR_STATE_TOP_CLOSE)
			return False
		return True

	def run(self):
		exit = False
		if(not self.foundUser()):
			return
		if(0 & self.user in cfg.ADMINIS):
			self.adminSession()
		else:
			while(self.bottleSession()):
				pass
