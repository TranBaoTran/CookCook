import pygame
import os

import globalvariable


class GameTime:
    font_path = "Grand9K Pixel.ttf"
    font = None  # Font object will be initialized later

    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.seconds = 0
        self.minutes = 0
        self.count = 0
        self.timer_surface = None

    @classmethod
    def initialize_font(cls):
        if cls.font is None:
            cls.font = pygame.font.Font(cls.font_path, 13)

    def update(self):
        self.count += 1
        if self.count == globalvariable.FPS:
            self.seconds += 1
            if self.seconds == 60:
                self.seconds = 0
                self.minutes += 1
            self.update_timer_surface()
        elif self.count > globalvariable.FPS:
            self.count = 0

    def update_timer_surface(self):
        timer_text = f"{self.minutes:02d}:{self.seconds:02d}"
        self.timer_surface = self.font.render(timer_text, True, (0, 0, 0))

    def draw(self, screen):
        if self.timer_surface:
            screen.blit(self.timer_surface, (self.x, self.y))
