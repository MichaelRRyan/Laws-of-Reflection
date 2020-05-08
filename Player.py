import pygame
import math

class Player(object):
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.width = 25
        self.height = 49
        self.movement_speed = 5
        self.movement_accel = 0.2
        self.friction = 0.9
        self.jump_speed = 8
        self.gravity = 0.3
        self.on_ground = True
        self.velX = 0
        self.velY = 0

    def inverse(self):
        self.gravity = -self.gravity
        self.jump_speed = -self.jump_speed

    def update(self, pressed_keys, blocks):
        self.velY += self.gravity

        movement_input = 0

        if pressed_keys[pygame.K_LEFT]:
            movement_input -= 1

        if pressed_keys[pygame.K_RIGHT]:
            movement_input += 1

        self.velX += movement_input * self.movement_accel

        if movement_input == 0:
            self.velX *= self.friction

        self.velX = math.copysign(min(abs(self.velX), self.movement_speed), self.velX)

        if pressed_keys[pygame.K_UP] and self.on_ground:
            self.velY = -self.jump_speed

        self.handle_collisions(blocks)

    def handle_collisions(self, blocks):
        if not(self.is_colliding(blocks, self.x + self.velX, self.y)):
            self.x += self.velX
        else:
            while not(self.is_colliding(blocks, self.x + math.copysign(1, self.velX), self.y)):
                self.x += math.copysign(1, self.velX)

            self.velX = 0

        if not(self.is_colliding(blocks, self.x, self.y + self.velY)):
            self.y += self.velY
            self.on_ground = False
        else:
            while not(self.is_colliding(blocks, self.x, self.y + math.copysign(1, self.velY))):
                self.y += math.copysign(1, self.velY)

            self.velY = 0
            self.on_ground = True

    def is_colliding(self, blocks, x, y):
        for block in blocks:
            if is_colliding(self, block, x, y):
                return True

        return False

    def draw(self, window, color):
        pygame.draw.rect(window, color, (round(self.x), round(self.y), self.width, self.height))

def is_colliding(object1, object2, x, y):
    if x + object1.width > object2.x and x < object2.x + object2.width:
        if y + object1.height > object2.y and y < object2.y + object2.height:
            return True

    return False