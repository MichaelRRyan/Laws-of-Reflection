import pygame


class Animator(object):
    def __init__(self):
        self.fade_time = 30
        self.timer = 0
        self.faded_out = False
        self.animating = False

    def update(self):
        self.timer += 1

        if self.timer > self.fade_time:
            self.timer = 0

            if not self.faded_out:
                self.faded_out = True
                return True
            else:
                self.animating = False
                self.faded_out = False

        return False

    def draw(self, window):
        if self.animating:
            w, h = pygame.display.get_surface().get_size()
            overlay = pygame.Surface((w, h))
            if not self.faded_out:
                overlay.set_alpha(self.timer / self.fade_time * 255)
            else:
                overlay.set_alpha((1 - self.timer / self.fade_time) * 255)
            overlay.fill((0, 0, 0))
            window.blit(overlay, (0, 0))
