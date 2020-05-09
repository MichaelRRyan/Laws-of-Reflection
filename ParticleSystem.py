import pygame

class ParticleSystem(object):
    def __init__(self):
        self.particles = []

    def update(self):
        for particle in self.particles:
            particle.update()

            if not(particle.alive):
                self.particles.pop(self.particles.index(particle))

    def draw(self, window):
        for particle in self.particles:
            particle.draw(window)

    def create_ripple(self, x):
        self.particles.append(RippleParticle(x))

class RippleParticle(object):
    def __init__(self, x):
        self.x = x
        self.radius = 10
        self.alive = True

    def update(self):
        self.radius += 1
        if self.radius > 40:
            self.alive = False

    def draw(self, window):
        pygame.draw.circle(window, (50, 0, 50), (round(self.x), 300), round(self.radius), 1)