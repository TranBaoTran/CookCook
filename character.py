from os import listdir
from os.path import isfile, join

import pygame


def flip(sprites):
    return [pygame.transform.flip(sprite, True, False) for sprite in sprites]


def load_sprite_sheets(dir1, width, height, scale, direction=False):
    path = join("asset", "img", dir1)
    images = [f for f in listdir(path) if isfile(join(path, f))]

    all_sprites = {}

    for image in images:
        sprite_sheet = pygame.image.load(join(path, image)).convert_alpha()

        sprites = []
        for i in range(sprite_sheet.get_width() // width):
            surface = pygame.Surface((width, height), pygame.SRCALPHA)
            # surface = pygame.Surface((width, height)).convert_alpha()
            rect = pygame.Rect(i * width, 0, width, height)
            surface.blit(sprite_sheet, (0, 0), rect)
            img = pygame.transform.scale(surface, (width * scale, height * scale))
            img = img.subsurface((34 * scale, 66 * scale, 60 * scale, 62 * scale))
            sprites.append(img)

        if direction:
            all_sprites[image.replace(".png", "") + "_right"] = sprites
            all_sprites[image.replace(".png", "") + "_left"] = flip(sprites)
        else:
            all_sprites[image.replace(".png", "")] = sprites

    return all_sprites


def load_boss_sprite(dir1, width, height, scale, direction=False):
    path = join("asset", "img", dir1)
    images = [f for f in listdir(path) if isfile(join(path, f))]

    all_sprites = {}

    for image in images:
        sprite_sheet = pygame.image.load(join(path, image)).convert_alpha()

        sprites = []
        for i in range(sprite_sheet.get_width() // width):
            surface = pygame.Surface((width, height), pygame.SRCALPHA)
            # surface = pygame.Surface((width, height)).convert_alpha()
            rect = pygame.Rect(i * width, 0, width, height)
            surface.blit(sprite_sheet, (0, 0), rect)
            img = pygame.transform.scale(surface, (width * scale, height * scale))
            img = img.subsurface((8 * scale, 32 * scale, 64 * scale, 40 * scale))
            sprites.append(img)

        if direction:
            all_sprites[image.replace(".png", "")] = flip(sprites)
        else:
            all_sprites[image.replace(".png", "")] = sprites

    return all_sprites


class Player(pygame.sprite.Sprite):
    GRAVITY = 1
    ANIMATION_DELAY = 5

    def __init__(self, name, x, y, width, height, scale):
        super().__init__()
        self.SPRITES = load_sprite_sheets("character/"+name+"_Slime - Copy", 128, 128, scale, True)
        self.reset(x, y, width, height, scale)
        self.sprite_sheet_name = "idle_left"

    def reset(self, x, y, width, height, scale):
        self.rect = pygame.Rect(x, y, 47 * scale, 33 * scale)
        self.x_vel = 0
        self.y_vel = 0
        self.direction = "left"
        self.animation_count = 0
        self.fall_count = 0
        self.jump_count = 0
        self.hit_count = 0

    def jump(self):
        self.y_vel = -self.GRAVITY * 8
        self.animation_count = 0
        self.jump_count += 1
        if self.jump_count == 1:
            self.fall_count = 0

    def move(self, dx, dy):
        self.rect.x += dx
        self.rect.y += dy

    def move_left(self, vel):
        self.x_vel = -vel
        if self.direction != "left":
            self.direction = "left"
            self.animation_count = 0

    def move_right(self, vel):
        self.x_vel = vel
        if self.direction != "right":
            self.direction = "right"
            self.animation_count = 0

    def loop(self, fps):
        self.y_vel += min(1, (self.fall_count / fps) * self.GRAVITY)
        self.move(self.x_vel, self.y_vel)
        self.fall_count += 1
        self.update_sprite()

    def landed(self):
        self.fall_count = 0
        self.y_vel = 0
        self.jump_count = 0

    def hit_head(self):
        self.hit_count = 0
        self.y_vel *= -1

    def update_sprite(self):
        sprite_sheet = "idle"
        if self.y_vel < 0:
            if self.jump_count > 0:
                sprite_sheet = "jump"
        elif self.y_vel > self.GRAVITY * 2:
            sprite_sheet = "fall"
        elif self.x_vel != 0:
            sprite_sheet = "walk"
        self.sprite_sheet_name = sprite_sheet + "_" + self.direction
        self.update_state()


    def update_state(self):
        sprites = self.SPRITES[self.sprite_sheet_name]
        sprite_index = (self.animation_count //
                        self.ANIMATION_DELAY) % len(sprites)
        self.sprite = sprites[sprite_index]
        self.animation_count += 1
        self.update()

    def die(self):
        sprite_sheet_name = "dead" + "_" + self.direction
        sprites = self.SPRITES[sprite_sheet_name]
        sprite_index = (self.animation_count //
                        20) % len(sprites)
        self.sprite = sprites[sprite_index]
        self.animation_count += 1
        self.update()
        return sprite_index

    def update(self):
        self.rect = self.sprite.get_rect(topleft=(self.rect.x, self.rect.y))

    def draw(self, win):
        win.blit(self.sprite, (self.rect.x, self.rect.y))


class GroundBoss(pygame.sprite.Sprite):
    ANIMATION_DELAY = 10
    GRAVITY = 1

    def __init__(self, x, y, width, height, scale):
        super().__init__()
        self.SPRITES = load_boss_sprite("boss/Battle turtle", 72, 72, scale, True)
        self.reset(x, y, width, height, scale)

    def reset(self, x, y, width, height, scale):
        self.rect = pygame.Rect(x, y, width * scale, height * scale)
        self.animation_count = 0
        self.x_vel = 0
        self.y_vel = 0
        self.fall_count = 0

    def move_in(self, vel):
        self.rect.x += vel

    def move(self, dx, dy):
        self.rect.x += dx
        self.rect.y += dy

    def landed(self):
        self.fall_count = 0
        self.y_vel = 0

    def set_sprite_name(self, action):
        self.sprite_name = action

    def loop(self, fps):
        self.y_vel += min(1, (self.fall_count / fps) * self.GRAVITY)
        self.move(self.x_vel, self.y_vel)
        self.fall_count += 1
        self.update_sprite()

    def update_sprite(self):
        sprite_name = self.sprite_name
        sprites = self.SPRITES[sprite_name]
        sprite_index = (self.animation_count //
                        self.ANIMATION_DELAY) % len(sprites)
        self.sprite = sprites[sprite_index]
        self.animation_count += 1
        self.update()

    def update(self):
        self.rect = self.sprite.get_rect(topleft=(self.rect.x, self.rect.y))

    def draw(self, win):
        win.blit(self.sprite, (self.rect.x, self.rect.y))
