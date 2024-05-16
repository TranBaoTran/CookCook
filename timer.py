import pygame
import os

import globalvariable


class GameTime:
    font_path = "Grand9K Pixel.ttf"
    font = None  # Font object will be initialized later

    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.reset()
        self.timer_surface = None
        self.timer_text = f"{0:02d}:{0:02d}"
        self.die_time = ""

    @classmethod
    def initialize_font(cls):
        if cls.font is None:
            cls.font = pygame.font.Font(cls.font_path, 13)

    def reset(self):
        self.seconds = 0
        self.minutes = 0
        self.count = 0
        self.die_time = ""

    def compare(self, time):
        if not time:
            return False
        if self.seconds == time[0] and self.count == time[1] and self.minutes == time[2]:
            return True
        return False

    def add(self, sec):
        sum = self.seconds + sec
        if sum > 59:
            return sum - 60, self.count, self.minutes + 1
        else:
            return sum, self.count, self.minutes

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
        self.timer_text = f"{self.minutes:02d}:{self.seconds:02d}"
        self.timer_surface = self.font.render(self.timer_text, True, (0, 0, 0))

    def draw(self, screen):
        if self.timer_surface:
            screen.blit(self.timer_surface, (self.x, self.y))
