import pygame
import Player
import Block
import ParticleSystem
import Collision

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
        self.top_blocks = []
        self.bottom_blocks = []
        self.top_color = (255, 225, 200)
        self.bottom_color = (50, 0, 50)
        self.viewX = 0
        self.immovable_num = 3
        self.level_width = 0
        self.top_goal = GoalObject(0, 0, 25, 50)
        self.bottom_goal = GoalObject(0, 0, 25, 50)
        self.level_num = 0

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

        self.top_player.update(pressed_keys, self.top_blocks)
        self.bottom_player.update(pressed_keys, self.bottom_blocks)
        self.part_sys.update()

        self.check_for_level_complete()
        self.move_camera()

    def draw(self):
        self.top_blocks[0].draw(self.window, self.top_color)
        self.bottom_blocks[0].draw(self.window, self.bottom_color)

        self.part_sys.draw(self.window)

        for i in range(self.immovable_num, len(self.top_blocks)):
            self.top_blocks[i].draw(self.window, self.top_color)

        for i in range(self.immovable_num, len(self.bottom_blocks)):
            self.bottom_blocks[i].draw(self.window, self.bottom_color)

        self.top_player.draw(self.window, self.top_color)
        self.bottom_player.draw(self.window, self.bottom_color)

        # Draw the goals
        self.top_goal.draw(self.window, self.top_color)
        self.bottom_goal.draw(self.window, self.bottom_color)

        pygame.display.update()

    def load_level(self, level_num):
        self.top_blocks.clear()
        self.bottom_blocks.clear()
        self.top_player.x = self.window_width // 2- 12
        self.top_player.y = -50
        self.bottom_player.x = self.window_width // 2 - 12
        self.bottom_player.y = self.window_height
        self.viewX = 0

        file = open("levels/level" + str(level_num) + ".data", "r")

        for line in file:
            items = line.split()

            if len(items) == 0 or line[0] == "#":
                continue

            if len(items) == 2 and items[0] == "w":
                self.level_width = float(items[1])
                continue

            if len(items) == 3:
                if items[0] == "tg":
                    self.top_goal.x = int(items[1])
                    self.top_goal.y = self.window_height // 2 - int(items[2])
                elif items[0] == "bg":
                    self.bottom_goal.x = int(items[1])
                    self.bottom_goal.y = self.window_height // 2 + int(items[2]) - self.bottom_goal.height
                continue


            if len(items) == 5:
                if items[0] == "t":
                    self.top_blocks.append(Block.Block(float(items[1]), self.window_height // 2 - float(items[2]), float(items[3]), float(items[4])))
                else:
                    self.bottom_blocks.append(Block.Block(float(items[1]), self.window_height // 2 + float(items[2]) - float(items[4]), float(items[3]), float(items[4])))

        file.close()

    def move_camera(self):
        view_movement = 0

        if self.top_player.x < self.window_width / 2 and self.bottom_player.x < self.window_width / 2:

            view_movement = max(self.top_player.x, self.bottom_player.x) - self.window_width // 2
            self.viewX += view_movement

            if self.viewX < 0:
                view_movement -= self.viewX
                self.viewX = 0

        if self.top_player.x > self.window_width / 2 and self.bottom_player.x > self.window_width / 2:

            view_movement = min(self.top_player.x, self.bottom_player.x) - self.window_width // 2
            self.viewX += view_movement

            if self.viewX > self.level_width:
                view_movement -= self.viewX - self.level_width
                self.viewX = self.level_width

        self.top_player.x -= view_movement
        self.bottom_player.x -= view_movement

        for i in range(self.immovable_num, len(self.top_blocks)):
            self.top_blocks[i].set_offset(-self.viewX)

        for i in range(self.immovable_num, len(self.bottom_blocks)):
            self.bottom_blocks[i].set_offset(-self.viewX)

        self.top_goal.x -= view_movement
        self.bottom_goal.x -= view_movement

    def check_for_level_complete(self):
        if Collision.is_colliding(self.top_player, self.top_goal):
            if Collision.is_colliding(self.bottom_player, self.bottom_goal):
                self.next_level()

    def next_level(self):
        self.level_num += 1
        self.load_level(self.level_num)

class GoalObject(object):
    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height

    def draw(self, window, color):
        pygame.draw.rect(window, color, (round(self.x), self.y, self.width, self.height), 2)

# Start the game
pygame.init()

game = Game()
game.run()

pygame.quit()
exit()