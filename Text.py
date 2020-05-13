import pygame

class Text(object):
    def __init__(self, string, position, color, size):
        font = pygame.font.Font("freesansbold.ttf", size)
        self.text = font.render(string, True, color)
        self.text_rect = self.text.get_rect()
        self.text_rect.center = position

    def draw(self, window):
        window.blit(self.text, self.text_rect)