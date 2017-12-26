import pygame
import time

pygame.init()

pygame.mixer.music.load('/home/pi/pywork/5.mp3')
pygame.mixer.music.set_volume(1)
pygame.mixer.music.play(0, 0.0)

time.sleep(3)