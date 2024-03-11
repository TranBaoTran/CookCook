import pygame
from pygame.locals import *

DEFAULT_SCREEN_WIDTH = 1000
DEFAULT_SCREEN_HEIGHT = 750
SCREEN_WIDTH = DEFAULT_SCREEN_WIDTH
SCREEN_HEIGHT = DEFAULT_SCREEN_HEIGHT
SCREEN_COLOR = (0, 0, 0)
CHARACTER_HEIGHT = 30
BLOCK_HEIGHT = 50
win = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("CookCook")

clientNumber = 0

class Block():
    def __init__(self, height):
        self.height = height

    def draw(self,win):
        print("lol")

def drawMap():
    print("lol")

class Player():
    def __init__(self, x, y, width, height, color):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.color = color
        self.rect = (x, y, width, height)
        self.vel = 3

    def draw(self, win):
        pygame.draw.rect(win, self.color, self.rect)

    def move(self):
        keys = pygame.key.get_pressed()

        if keys[pygame.K_LEFT]:
            self.x -= self.vel

        if keys[pygame.K_RIGHT]:
            self.x += self.vel

        if keys[pygame.K_UP]:
            self.y -= self.vel

        if keys[pygame.K_DOWN]:
            self.y += self.vel

        self.rect = (self.x, self.y, self.width, self.height)


def redrawWindow(win, player):
    win.fill(SCREEN_COLOR)
    player.draw(win)
    pygame.display.update()


def main():
    run = True
    p = Player(50,50,CHARACTER_HEIGHT,CHARACTER_HEIGHT,(0,255,0))
    clock = pygame.time.Clock()

    while run:
        clock.tick(60)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()

        p.move()
        redrawWindow(win, p)


if __name__ == '__main__':
    pygame.init()
    main()
