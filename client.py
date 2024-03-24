import pygame
import math
from pygame.locals import *

import slimesheet

DEFAULT_SCREEN_WIDTH = 960
DEFAULT_SCREEN_HEIGHT = 640
SCREEN_WIDTH = DEFAULT_SCREEN_WIDTH
SCREEN_HEIGHT = DEFAULT_SCREEN_HEIGHT
FPS = 36
SCREEN_COLOR = (255, 255, 255)
CHARACTER_HEIGHT = 30
BLOCK_HEIGHT = 50
win = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("CookCook")
last_update = pygame.time.get_ticks()
ANIMATION_COOLDOWN = 500

clientNumber = 0


class Player(pygame.sprite.Sprite):
    STANDING_IMG = "asset/img/character.py/Blue_Slime/Idle.png"
    WALKING_IMG = "asset/img/character.py/Blue_Slime/walk.png"
    JUMPING_IMG = "asset/img/character.py/Blue_Slime/Jump.png"

    def __init__(self, x, y, width, height, color):
        pygame.sprite.Sprite.__init__(self)
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.color = color
        self.rect = (x, y, width, height)
        self.vel = 3
        self.isJump = False
        self.jumpCount = 10
        self.left = False
        self.right = False
        self.walkCount = 0
        self.stand_frame = 0
        self.jump_frame = 0
        # stand sprite
        self.sprite_sheet_stand_img = pygame.image.load(self.STANDING_IMG).convert_alpha()
        self.sprite_sheet_stand = slimesheet.SpriteSheet(self.sprite_sheet_stand_img)
        self.animation_stand_list = []
        # walk sprite
        self.sprite_sheet_walk_img = pygame.image.load(self.WALKING_IMG).convert_alpha()
        self.sprite_sheet_walk = slimesheet.SpriteSheet(self.sprite_sheet_walk_img)
        self.animation_walk_left_list = []
        self.animation_walk_right_list = []
        # jump sprite
        self.sprite_sheet_jump_img = pygame.image.load(self.JUMPING_IMG).convert_alpha()
        self.sprite_sheet_jump = slimesheet.SpriteSheet(self.sprite_sheet_jump_img)
        self.animation_jump_list = []
        # number of normal sprites
        self.animation_step = 8
        self.animation_change_frame = math.ceil(FPS / self.animation_step)
        # number of jump sprites
        self.animation_jump_step = 13
        self.animation_jump_change_frame = math.ceil(FPS / self.animation_jump_step)
        self.loadImage()

    def loadImage(self):
        # stand
        for x in range(self.animation_step):
            self.animation_stand_list.append(self.sprite_sheet_stand.get_image(x, 128, 128, 1, (0, 0, 0)))
        # walk
        for x in range(self.animation_step):
            self.animation_walk_right_list.append(self.sprite_sheet_walk.get_image(x, 128, 128, 1, (0, 0, 0)))
            self.animation_walk_left_list.append(
                pygame.transform.flip(self.sprite_sheet_walk.get_image(x, 128, 128, 1, (0, 0, 0)), True, False))
        # jump
        for x in range(self.animation_jump_step):
            self.animation_jump_list.append(self.sprite_sheet_jump.get_image(x, 128, 128, 1, (0, 0, 0)))

    def draw(self, win):
        if self.walkCount + 1 >= FPS:
            self.walkCount = 0

        if self.stand_frame + 1 >= FPS:
            self.stand_frame = 0

        if self.isJump:
            win.blit(self.animation_jump_list[self.jump_frame // self.animation_jump_change_frame], (self.x, self.y))
            self.jump_frame += 1
            self.stand_frame = 0
        elif self.left:
            win.blit(self.animation_walk_left_list[self.walkCount // self.animation_change_frame], (self.x, self.y))
            self.walkCount += 1
            self.stand_frame = 0
        elif self.right:
            win.blit(self.animation_walk_right_list[self.walkCount // self.animation_change_frame], (self.x, self.y))
            self.walkCount += 1
            self.stand_frame = 0
        else:
            win.blit(self.animation_stand_list[self.stand_frame // self.animation_change_frame], (self.x, self.y))
            self.stand_frame += 1
        pygame.draw.rect(win, self.color, self.rect)

    def move(self):
        keys = pygame.key.get_pressed()

        if keys[pygame.K_LEFT] and self.x > self.vel:
            self.x -= self.vel
            self.left = True
            self.right = False

        elif keys[pygame.K_RIGHT] and self.x < SCREEN_WIDTH - self.width - self.vel:
            self.x += self.vel
            self.left = False
            self.right = True

        else:
            self.right = False
            self.left = False
            self.walkCount = 0

        if not self.isJump:
            if keys[pygame.K_UP] and self.y > self.vel:
                self.y -= self.vel
                self.right = False
                self.left = False
                self.walkCount = 0

            if keys[pygame.K_DOWN] and self.y < SCREEN_HEIGHT - self.height - self.vel:
                self.y += self.vel

            if keys[pygame.K_SPACE]:
                self.isJump = True

        else:
            if self.jumpCount >= -10:
                neg = 1
                if self.jumpCount < 0:
                    neg = -1
                self.y -= (self.jumpCount ** 2) * 0.3 * neg
                self.jumpCount -= 1
            else:
                self.isJump = False
                self.jumpCount = 10
                self.jump_frame = 0
        self.rect = (self.x, self.y, self.width, self.height)


def redrawWindow(win, player):
    win.fill(SCREEN_COLOR)
    player.draw(win)
    pygame.display.update()


def main():
    run = True
    p = Player(50, 400, CHARACTER_HEIGHT, CHARACTER_HEIGHT, (0, 255, 0))
    clock = pygame.time.Clock()

    while run:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()

        p.move()
        redrawWindow(win, p)


if __name__ == '__main__':
    pygame.init()
    main()
