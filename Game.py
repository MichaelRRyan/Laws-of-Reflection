import pygame
import Player
import Block
import ParticleSystem

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
        self.top_goal = (0, 0)
        self.bottom_goal = (0, 0)

        pygame.display.set_caption("Mirror")
        self.bottom_player.inverse()

        self.read_in_blocks("level0.txt")

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
        pygame.draw.rect(self.window, self.top_color, (self.top_goal[0], self.top_goal[1], 26, 50), 2)
        pygame.draw.rect(self.window, self.bottom_color, (self.bottom_goal[0], self.bottom_goal[1], 26, 50), 2)

        pygame.display.update()

    def read_in_blocks(self, file_name):
        self.top_blocks.clear()
        self.bottom_blocks.clear()

        file = open("levels/" + file_name, "r")

        for line in file:
            items = line.split()

            if len(items) == 0 or line[0] == "#":
                continue

            if len(items) == 2 and items[0] == "w":
                self.level_width = float(items[1])
                continue

            if len(items) == 3:
                if items[0] == "tg":
                    self.top_goal = (int(items[1]), self.window_height // 2 - int(items[2]))
                elif items[0] == "bg":
                    self.bottom_goal = (int(items[1]), self.window_height // 2 + int(items[2]) - 50)
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

        self.top_goal = ( self.top_goal[0] - int(view_movement), self.top_goal[1])
        self.bottom_goal = ( self.bottom_goal[0] - int(view_movement), self.bottom_goal[1])

pygame.init()

game = Game()
game.run()

pygame.quit()
exit()