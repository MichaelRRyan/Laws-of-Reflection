import pygame
import Player
import GameObject
import ParticleSystem
import Collision
import Camera
import Level

class Game(object):
    def __init__(self):
        self.window_width = 800
        self.window_height = 600
        self.window = pygame.display.set_mode((self.window_width, self.window_height))
        self.running = True
        self.clock = pygame.time.Clock()
        self.part_sys = ParticleSystem.ParticleSystem()
        self.top_player = Player.Player(self.window_width // 2- 12, -50, self.part_sys)
        self.bottom_player = Player.Player(self.window_width // 2 - 12, self.window_height, self.part_sys)
        self.top_color = (255, 225, 200)
        self.bottom_color = (50, 0, 50)
        self.immovable_num = 3
        self.level_num = -1
        self.level = Level.Level()
        self.camera = Camera.Camera(self.window)

        pygame.display.set_caption("Mirror")
        self.bottom_player.inverse()

        self.next_level()

    def run(self):
        while self.running:
            self.clock.tick(60)

            self.handle_events()
            self.update()
            self.draw()

    def handle_events(self):
        for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                    break

    def update(self):
        pressed_keys = pygame.key.get_pressed()

        self.top_player.update(pressed_keys, self.level.top_blocks)
        self.bottom_player.update(pressed_keys, self.level.bottom_blocks)
        self.part_sys.update()

        self.check_for_level_complete()
        self.camera.focus_on(self.top_player.x, self.bottom_player.x, self.window_width, self.level.level_width)

    def draw(self):
        self.camera.draw_rect(self.top_color, self.level.top_blocks[0])
        self.camera.draw_rect(self.bottom_color, self.level.bottom_blocks[0])

        self.part_sys.draw(self.camera)

        for i in range(self.immovable_num, len(self.level.top_blocks)):
            self.camera.draw_rect(self.top_color, self.level.top_blocks[i])

        for i in range(self.immovable_num, len(self.level.bottom_blocks)):
            self.camera.draw_rect(self.bottom_color, self.level.bottom_blocks[i])

        self.camera.draw_rect(self.top_color, self.top_player)
        self.camera.draw_rect(self.bottom_color, self.bottom_player)

        # Draw the goals
        self.camera.draw_rect(self.top_color, self.level.top_goal)
        self.camera.draw_rect(self.bottom_color, self.level.bottom_goal)

        pygame.display.update()

    def load_level(self, level_num):
        self.top_player.x = self.window_width // 2- 12
        self.top_player.y = -50
        self.bottom_player.x = self.window_width // 2 - 12
        self.bottom_player.y = self.window_height
        self.camera.view_x = 0

        self.level = Level.load_level(level_num)

    def check_for_level_complete(self):
        if Collision.is_colliding(self.top_player, self.level.top_goal):
            if Collision.is_colliding(self.bottom_player, self.level.bottom_goal):
                self.next_level()

    def next_level(self):
        self.level_num += 1
        self.load_level(self.level_num)

# Start the game
pygame.init()

game = Game()
game.run()

pygame.quit()
exit()