import pygame

class Block(object):
    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.initX = x
        self.width = width
        self.height = height

    def set_offset(self, x):
        self.x = self.initX + x

    def draw(self, window, color):
        pygame.draw.rect(window, color, (self.x, self.y, self.width, self.height))