import pygame
import Text

class Credits(object):
    def __init__(self, window_width, window_height, text_color):
        self.thanks_text = Text.Text("Thanks for Playing!", (window_width // 2, window_height // 2 - 50),
                                     text_color, 40)
        self.follow_text1 = Text.Text("If you liked this game, consider following",
                                      (window_width // 2, window_height // 2 + 20), text_color, 20)

        self.follow_text2 = Text.Text("me on Twitter @MichaelRainRyan :)", (window_width // 2, window_height // 2 + 60),
                                      text_color, 20)

        self.exit_text = Text.Text("press Esc to exit to menu",
                                      (window_width // 2, window_height // 2 + 250), text_color, 25)

    def update(self, pressed_keys):
        if pressed_keys[pygame.K_ESCAPE]:
            return True
        return False

    def draw(self, window):

        window.fill((0, 0, 0))

        self.thanks_text.draw(window)
        self.follow_text1.draw(window)
        self.follow_text2.draw(window)
        self.exit_text.draw(window)