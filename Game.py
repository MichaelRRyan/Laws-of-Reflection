import pygame
import Player
import GameObject
import ParticleSystem
import Collision
import Camera
import Level
import Credits
import Menu
import AudioManager
from enum import Enum


class GameState(Enum):
    MENU = 0
    GAMEPLAY = 1
    CREDITS = 2


class Game(object):
    def __init__(self):
        self.window_width = 800
        self.window_height = 600
        self.window = pygame.display.set_mode((self.window_width, self.window_height))
        self.running = True
        self.top_color = (255, 225, 200)
        self.bottom_color = (50, 0, 50)
        self.clock = pygame.time.Clock()
        self.audio_manager = AudioManager.AudioManager()
        self.part_sys = ParticleSystem.ParticleSystem(self.top_color, self.bottom_color)
        self.top_player = Player.Player(self.window_width // 2 - 12, -50, self.part_sys, self.audio_manager)
        self.bottom_player = Player.Player(self.window_width // 2 - 12, self.window_height, self.part_sys, self.audio_manager)
        self.immovable_num = 3
        self.level_num = -1
        self.max_level_num = 5
        self.level = Level.Level()
        self.camera = Camera.Camera(self.window)
        self.game_state = GameState.MENU
        self.credits = Credits.Credits(self.window_width, self.window_height, self.top_color)
        self.menu = Menu.Menu(self.window_width, self.window_height, self.bottom_color, self.top_color)

        pygame.display.set_caption("Laws of Reflection")
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
        # Get a list of keys as bools (true if pressed)
        pressed_keys = pygame.key.get_pressed()

        if self.game_state == GameState.MENU:
            if self.menu.update(pressed_keys):
                self.game_state = GameState.GAMEPLAY
        elif self.game_state == GameState.GAMEPLAY:
            self.updateGameplay(pressed_keys)
        else:
            if self.credits.update(pressed_keys):
                self.game_state = GameState.MENU

    def draw(self):

        if self.game_state == GameState.MENU:
            self.menu.draw(self.window)
        elif self.game_state == GameState.GAMEPLAY:
            self.drawGameplay()
        else:
            self.credits.draw(self.window)

        pygame.display.update()

    def check_for_level_complete(self):
        if Collision.is_colliding(self.top_player, self.level.top_goal):
            if Collision.is_colliding(self.bottom_player, self.level.bottom_goal):
                self.next_level()

    def next_level(self):
        self.top_player.reset(self.window_width, self.window_height)
        self.bottom_player.reset(self.window_width, self.window_height)
        self.camera.view_x = 0

        self.level_num += 1

        if self.level_num < self.max_level_num:
            self.level = Level.load_level(self.level_num)
        else:
            self.game_state = GameState.CREDITS

    def update_stationary(self):
        for i in range(0, 2):
            self.level.top_blocks[i].x = self.camera.view_x
            self.level.bottom_blocks[i].x = self.camera.view_x

        self.level.top_blocks[2].x = self.camera.view_x + 800
        self.level.bottom_blocks[2].x = self.camera.view_x + 800

    def updateGameplay(self, pressed_keys):
        # update the players
        self.top_player.update(pressed_keys, self.level.top_blocks)
        self.bottom_player.update(pressed_keys, self.level.bottom_blocks)

        # Update the particles
        self.part_sys.update()

        # Check if level is complete and update camera
        self.check_for_level_complete()
        self.camera.focus_on(self.top_player.x, self.bottom_player.x, self.window_width, self.level.level_width)
        self.update_stationary()

    def drawGameplay(self):
        # Draw the floors
        self.camera.draw_rect(self.top_color, self.level.top_blocks[0])
        self.camera.draw_rect(self.bottom_color, self.level.bottom_blocks[0])

        # Draw the particles
        self.part_sys.draw(self.camera)

        # Draw the platforms
        for i in range(self.immovable_num, len(self.level.top_blocks)):
            self.camera.draw_rect(self.top_color, self.level.top_blocks[i])

        for i in range(self.immovable_num, len(self.level.bottom_blocks)):
            self.camera.draw_rect(self.bottom_color, self.level.bottom_blocks[i])

        # Draw the players
        self.camera.draw_rect(self.top_color, self.top_player)
        self.camera.draw_rect(self.bottom_color, self.bottom_player)

        # Draw the goals
        self.camera.draw_rect(self.top_color, self.level.top_goal)
        self.camera.draw_rect(self.bottom_color, self.level.bottom_goal)

    def reset(self):
        self.part_sys.particles.clear()
        self.level = Level.Level()
        self.top_player.reset()
        self.bottom_player.reset()
        self.level_num = -1

# Start the game
pygame.mixer.pre_init(44100, -16, 1, 512)
pygame.init()

game = Game()
game.run()

pygame.quit()
exit()
