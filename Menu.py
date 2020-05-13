import pygame
import Text


class Menu(object):
    def __init__(self, window_width, window_height, dark_color, light_color):
        self.light_color = light_color
        self.dark_color = dark_color
        self.title = Text.Text("Laws of Reflection", (window_width // 2, window_height // 2 - 170), light_color, 60)
        self.author_text = Text.Text("A game by Michael Rainsford Ryan", (window_width // 2, window_height // 2 - 100),
                                     light_color, 20)
        self.continue_text = Text.Text("press space to play", (window_width // 2, window_height // 2 + 100),
                                       dark_color, 30)
        self.twitter_text = Text.Text("Twitter: @MichaelRainRyan", (window_width // 2, window_height // 2 + 260),
                                      dark_color, 18)

    def update(self, pressed_keys):
        if pressed_keys[pygame.K_SPACE]:
            return True
        return False

    def draw(self, window):
        window.fill(self.dark_color)
        pygame.draw.rect(window, self.light_color, (0, 300, 800, 300))

        self.title.draw(window)
        self.author_text.draw(window)
        self.continue_text.draw(window)
        self.twitter_text.draw(window)
