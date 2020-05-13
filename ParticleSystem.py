import pygame
import Camera
import random
import math


class ParticleSystem(object):
    def __init__(self, top_color, bottom_color):
        self.particles = []
        self.top_color = top_color
        self.bottom_color = bottom_color

    def update(self):
        for particle in self.particles:
            particle.update()

            if not (particle.alive):
                self.particles.pop(self.particles.index(particle))

    def draw(self, Camera):
        for particle in self.particles:
            if particle.y < 300:
                Camera.draw_circle(self.top_color, particle)
            else:
                Camera.draw_circle(self.bottom_color, particle)

    def create_ripple(self, x):
        self.particles.append(RippleParticle(x))

    def create_dust(self, x, y, vert_dir, number):
        for i in range(0, number):
            self.particles.append(DustParticle(x, y, vert_dir))


class RippleParticle(object):
    def __init__(self, x):
        self.x = x
        self.y = 300
        self.radius = 10
        self.alive = True
        self.border = 1

    def update(self):
        self.radius += 1
        if self.radius > 40:
            self.alive = False


class DustParticle(object):
    def __init__(self, x, y, vert_dir):
        self.x = x
        self.y = y
        self.dir_x = random.random() * 2.0 - 1.0
        self.dir_y = vert_dir
        self.alive = True
        self.radius = 2
        self.border = 0
        self.time_alive = 0

        dir_mag = math.sqrt(self.dir_x * self.dir_x + self.dir_y * self.dir_y)
        self.dir_x = self.dir_x / dir_mag
        self.dir_y = self.dir_y / dir_mag

    def update(self):
        self.x += self.dir_x
        self.y += self.dir_y
        self.time_alive += 1
        if self.time_alive > 20:
            self.alive = False
