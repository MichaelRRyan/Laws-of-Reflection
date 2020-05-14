import pygame
import random

class AudioManager(object):
    def __init__(self):
        self.splash_sound = pygame.mixer.Sound("audio/water.wav")
        self.thud0_sound = pygame.mixer.Sound("audio/thud-0.wav")
        self.thud1_sound = pygame.mixer.Sound("audio/thud-1.wav")
        self.thud2_sound = pygame.mixer.Sound("audio/thud-2.wav")

    def play_splash(self):
        self.splash_sound.play()

    def play_thud(self):
        sound = round(random.random() * 3)
        if sound == 0:
            self.thud0_sound.play()
        elif sound == 1:
            self.thud1_sound.play()
        else:
            self.thud2_sound.play()