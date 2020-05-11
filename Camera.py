import pygame

class Camera(object):
    def __init__(self, window):
        self.view_x = 0
        self.change_in_view = 0
        self.window = window

    def focus_on(self, world_x1, world_x2, window_width, level_width):

        local_x1 = world_x1 - self.view_x
        local_x2 = world_x2 - self.view_x

        previous_view = self.view_x

        if local_x1 < window_width / 2 and local_x2 < window_width / 2:

            self.view_x += max(local_x1, local_x2) - window_width // 2

            if self.view_x < 0:
                self.view_x = 0

        if local_x1 > window_width / 2 and local_x2 > window_width / 2:

            self.view_x += min(local_x1, local_x2) - window_width // 2

            if self.view_x > level_width:
                self.view_x = level_width

        self.change_in_view = self.view_x - previous_view

    def draw_rect(self, color, subject):
        pygame.draw.rect(self.window, color, (round(subject.x - self.view_x), round(subject.y), subject.width, subject.height), subject.border)

    def draw_circle(self, color, subject):
        pygame.draw.circle(self.window, color, (round(subject.x - self.view_x), round(subject.y)), subject.radius, subject.border)