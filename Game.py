import pygame
import Player
import Block

class Game(object):
    def __init__(self):
        self.window_width = 800
        self.window_height = 600
        self.window = pygame.display.set_mode((self.window_width, self.window_height))
        self.running = True
        self.clock = pygame.time.Clock()
        self.top_player = Player.Player(self.window_width // 2, 0)
        self.bottom_player = Player.Player(self.window_width // 2, self.window_height - 50)
        self.top_blocks = []
        self.bottom_blocks = []
        self.top_color = (255, 255, 255)
        self.bottom_color = (0, 0, 0)
        self.viewX = 0
        self.immovable_num = 3

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

        if self.top_player.x > self.window_width / 2 and self.bottom_player.x > self.window_width / 2:
            view_movement = min(self.top_player.x, self.bottom_player.x) - self.window_width // 2
            self.viewX += view_movement
            self.top_player.x -= view_movement
            self.bottom_player.x -= view_movement

            for i in range(self.immovable_num, len(self.top_blocks)):
                self.top_blocks[i].set_offset(-self.viewX)

            for i in range(self.immovable_num, len(self.bottom_blocks)):
                self.bottom_blocks[i].set_offset(-self.viewX)

    def draw(self):
        self.top_blocks[0].draw(self.window, self.top_color)
        self.bottom_blocks[0].draw(self.window, self.bottom_color)

        for i in range(self.immovable_num, len(self.top_blocks)):
            self.top_blocks[i].draw(self.window, self.top_color)

        for i in range(self.immovable_num, len(self.bottom_blocks)):
            self.bottom_blocks[i].draw(self.window, self.bottom_color)

        self.top_player.draw(self.window, self.top_color)
        self.bottom_player.draw(self.window, self.bottom_color)

        pygame.display.update()

    def read_in_blocks(self, file_name):
        self.top_blocks.clear()
        self.bottom_blocks.clear()

        file = open("levels/" + file_name, "r")

        for line in file:
            items = line.split()

            if len(items) != 5 or (len(line) != 0 and line[0] == "#"):
                continue

            if items[0] == "t":
                self.top_blocks.append(Block.Block(float(items[1]), self.window_height // 2 - float(items[2]), float(items[3]), float(items[4])))
            else:
                self.bottom_blocks.append(Block.Block(float(items[1]), self.window_height // 2 + float(items[2]) - float(items[4]), float(items[3]), float(items[4])))

        file.close()

pygame.init()

game = Game()
game.run()

pygame.quit()