import os
import config as cfg
import random
from multiprocessing import Process
from check_silence import check_silence

class Player:

    def __init__(self):
        self.process = 0
        self.command = ""
        pass

    def play_sound(self, type):
        if(not check_silence()):
            return
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

    def play_reward(self, score):
        if(not check_silence()):
            return
        if score <= 29:
            self.command = "mplayer " + cfg.SOUNDS_BASE_DIR + str(score) + ".mp3" + " -af volume=7"
        else:
            choice = random.randInt(1,6)
            self.command = "mplayer " + cfg.SOUNDS_BASE_DIR + "alot" + str(choice) + ".mp3" + " -af colume=7"
        self.process = Process(target=self.cmd_play)
        self.process.start()
        self.command = ""
        self.Process = 0

    def cmd_play(self):
        os.system(self.command)

if(__name__=="__main__"):
    p = Player()
    p.play_sound(1)
