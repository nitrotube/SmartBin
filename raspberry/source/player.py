import os
import config as cfg
from multiprocessing import Process

class Player:

	def __init__(self):
		self.process = 0
		self.command = ""
		pass

	def play_sound(self, type):
		if(type == cfg.PET):
			self.command = "mplayer " + cfg.SOUNDS[cfg.PET] + " -af volume=7"
		elif (type==cfg.ALUM):
			self.command = "mplayer " + cfg.SOUNDS[cfg.ALUM] + " -af volume=7"
		else:
			self.command = "mplayer " + cfg.SOUNDS[cfg.ERR] + " -af volume=7"
		self.process = Process(target=self.cmd_play)
		self.process.start()
		self.command = ""
		self.process = 0

	def cmd_play(self):
		os.system(self.command)

if(__name__=="__main__"):
	p = Player()
	p.play_sound(1)
