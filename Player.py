import pygame
import math
import ParticleSystem
import Collision

class Player(object):
    def __init__(self, x, y, part_sys):
        self.x = x
        self.y = y
        self.width = 25
        self.height = 50
        self.movement_speed = 5
        self.movement_accel = 0.2
        self.friction = 0.9
        self.jump_speed = 8
        self.gravity = 0.3
        self.on_ground = True
        self.velX = 0
        self.velY = 0
        self.part_sys = part_sys
        self.border = 0

    def reset(self, window_width, window_height):
        self.x = window_width / 2 - 12

        if self.gravity > 0:
            self.y = -50
        else:
            self.y = window_height

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
        # Horizontal Collisions
        collider = self.is_colliding(blocks, self.x + self.velX, self.y)#

        if collider == None:
            self.x += self.velX
        else:
            if math.copysign(1, self.velX) > 0:
                self.x = collider.x - self.width
            else:
                self.x = collider.x + collider.width

            self.velX = 0

        # Vertical Collisions
        collider = self.is_colliding(blocks, self.x, self.y + self.velY)

        if collider == None:
            self.y += self.velY
            self.on_ground = False
        else:
            sign = math.copysign(1, self.velY)

            if sign > 0:
                self.y = collider.y - self.height
            else:
                self.y = collider.y + collider.height

            self.velY = 0

            if (sign == math.copysign(1, self.gravity)) and not(self.on_ground):
                self.on_ground = True

                if self.y < 300 and self.y > 249:
                    self.part_sys.create_ripple(self.x + 12)

    def is_colliding(self, blocks, x, y):
        for block in blocks:
            if Collision.is_colliding_at(self, block, x, y):
                return block

        return None