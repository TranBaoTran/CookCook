import math

import pygame
import globalvariable


class SpriteSheet:
    def __init__(self, image):
        self.sheet = image

    def get_image(self, frame, width, height, scale, colour):
        image = pygame.Surface((width, height)).convert_alpha()
        image.blit(self.sheet, (0, 0), ((frame * width), 0, width, height))
        image = pygame.transform.scale(image, (width * scale, height * scale))
        image.set_colorkey(colour)
        return image


class Slime(pygame.sprite.Sprite):
    vel = 3
    isJump = False
    jumpCount = 10
    left = False
    right = False
    walkCount = 0
    stand_frame = 0
    jump_frame = 0
    animation_step = 8
    animation_jump_step = 13

    def __init__(self, x, y, name, scale):
        pygame.sprite.Sprite.__init__(self)
        self.x = x
        self.y = y
        self.scale = scale
        self.STANDING_IMG = "asset/img/character/" + name + "/Idle.png"
        self.WALKING_IMG = "asset/img/character/" + name + "/walk.png"
        self.JUMPING_IMG = "asset/img/character/" + name + "/Jump.png"
        # stand sprite
        self.sprite_sheet_stand_img = pygame.image.load(self.STANDING_IMG).convert_alpha()
        self.sprite_sheet_stand = SpriteSheet(self.sprite_sheet_stand_img)
        self.animation_stand_list = []
        # walk sprite
        self.sprite_sheet_walk_img = pygame.image.load(self.WALKING_IMG).convert_alpha()
        self.sprite_sheet_walk = SpriteSheet(self.sprite_sheet_walk_img)
        self.animation_walk_left_list = []
        self.animation_walk_right_list = []
        # jump sprite
        self.sprite_sheet_jump_img = pygame.image.load(self.JUMPING_IMG).convert_alpha()
        self.sprite_sheet_jump = SpriteSheet(self.sprite_sheet_jump_img)
        self.animation_jump_list = []
        # number of normal sprites
        self.animation_change_frame = math.ceil(globalvariable.FPS / self.animation_step)
        # number of jump sprites
        self.animation_jump_change_frame = math.ceil(globalvariable.FPS / self.animation_jump_step)
        self.loadImage()
        self.width = 128 * scale
        self.height = 128 * scale

    def loadImage(self):
        # stand
        for x in range(self.animation_step):
            self.animation_stand_list.append(self.sprite_sheet_stand.get_image(x, 128, 128, self.scale, (0, 0, 0)))
        # walk
        for x in range(self.animation_step):
            self.animation_walk_right_list.append(self.sprite_sheet_walk.get_image(x, 128, 128, self.scale, (0, 0, 0)))
            self.animation_walk_left_list.append(
                pygame.transform.flip(self.sprite_sheet_walk.get_image(x, 128, 128, self.scale, (0, 0, 0)), True,
                                      False).convert_alpha())
        # jump
        for x in range(self.animation_jump_step):
            self.animation_jump_list.append(self.sprite_sheet_jump.get_image(x, 128, 128, self.scale, (0, 0, 0)))

    def draw(self, win):
        if self.walkCount + 1 >= globalvariable.FPS:
            self.walkCount = 0

        if self.stand_frame + 1 >= globalvariable.FPS:
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

    def move(self):
        keys = pygame.key.get_pressed()

        if keys[pygame.K_LEFT] and self.x > self.vel:
            self.x -= self.vel
            self.left = True
            self.right = False

        elif keys[pygame.K_RIGHT] and self.x < globalvariable.SCREEN_WIDTH - self.width - self.vel:
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

            if keys[pygame.K_DOWN] and self.y < globalvariable.SCREEN_HEIGHT - self.height - self.vel:
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
