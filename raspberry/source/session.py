import Container
import config as cfg
import time
import requests
import socket

class Session():
	def __init__(self, container, user):
		self.container = container
		self.user = user

	def getClass(self, path):

		host = '192.168.0.133'
		port = 5000

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
		self.container.bott1.up()
		self.container.bott2.up()
		while True:
			if(self.container.scaner.hasCode()):
				if(self.container.scaner.readCode() == self.user):
					break
		self.container.bott1.down()
		self.container.bott2.down()

	def bottleSession(self):
		self.container.top.up()
		sessionStart = time.time()
		while(not self.container.smthIn()):
			if(time.time() - sessionStart > cfg.WAIT_LIMIT):
				self.container.top.down()
				return False

		self.container.top.down()
		type = self.getType()

		if(type == "pet"):
			self.container.player.play_sound(cfg.PLASTIC)
			self.container.pet.up()
			self.container.pet.down()
			rewardUser("pet")
		elif(type == "al"):
			self.container.alum.up()
			self.container.alum.down()
			self.container.player.play_sound(cfg.ALUMINIUM)
			rewardUser("al")
		else:
			self.container.player.play_sound(cfg.UNKNOWN)
			self.container.top.up()
			while(self.container.smthIn()):
				pass
			self.container.top.down()
			return False
		return True

	def run(self):
		exit = False
		if(not self.foundUser()):
			return
		self.container.beeper.beep()
		if(self.user in cfg.ADMINS):
			self.adminSession()
		else:
			while(self.bottleSession()):
				pass
		self.container.beeper.beep()
