import pygame
import Camera

class ParticleSystem(object):
    def __init__(self):
        self.particles = []

    def update(self):
        for particle in self.particles:
            particle.update()

            if not(particle.alive):
                self.particles.pop(self.particles.index(particle))

    def draw(self, Camera):
        for particle in self.particles:
            Camera.draw_circle((50, 0, 50), particle)

    def create_ripple(self, x):
        self.particles.append(RippleParticle(x))

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

    def draw(self, window):
        pygame.draw.circle(window, (50, 0, 50), (round(self.x), 300), round(self.radius), 1)