from os.path import join

import pygame
import pygame.sprite

import globalvariable


def get_sprite_sheet(dir1, width, height, scale):
    path = join("asset", "img", "weapon", dir1)
    sprite_sheet = pygame.image.load(path).convert_alpha()
    sprites = []
    for i in range(sprite_sheet.get_width() // width):
        surface = pygame.Surface((width, height), pygame.SRCALPHA)
        rect = pygame.Rect(i * width, 0, width, height)
        surface.blit(sprite_sheet, (0, 0), rect)
        img = pygame.transform.scale(surface, (width * scale, height * scale))
        sprites.append(img)
    return sprites


explode_image = pygame.transform.scale(pygame.image.load("asset/img/weapon/exploded.png"), (30, 30))
img_explode = pygame.Surface((explode_image.get_width(), explode_image.get_height()), pygame.SRCALPHA)
img_explode.blit(explode_image, (0, 0))


class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height, scale, images):
        super().__init__()
        self.rect = pygame.Rect(x, y, width * scale, height * scale)
        self.index = 0
        self.release = False
        self.images = images
        self.index = 0
        self.img_explode = img_explode
        self.exploded = 0
        self.hit = False
        self.time_remained = 0

    def draw(self, screen):
        screen.blit(self.sprite, self.rect)

    def move_towards_player(self, player):
        dirvect = pygame.math.Vector2(player.rect.x + player.rect.width / 3 - self.rect.x,
                                      player.rect.y + player.rect.height / 3 - self.rect.y)
        if self.time_remained > globalvariable.SMALL_BULLET_TIMEOUT:
            self.release = True
            self.sprite = self.img_explode
            self.time_remained = 0
        if not self.release:
            if globalvariable.BULLET_VEL >= dirvect.length():
                self.hit = True
                self.sprite = self.img_explode
                self.time_remained = 0
            else:
                dirvect.normalize()
                dirvect.scale_to_length(globalvariable.BULLET_VEL)
                self.rect.move_ip(dirvect)
                self.sprite = self.images[self.index]
        self.time_remained += 1

    def move_towards_player2(self, player):
        if self.rect.x > player.rect.x:
            self.index = 0
        else:
            self.index = 1
        dirvect = pygame.math.Vector2(player.rect.x + player.rect.width / 3 - self.rect.x,
                                      player.rect.y + player.rect.height / 3 - self.rect.y)
        if not self.hit:
            if globalvariable.BULLET_VEL >= dirvect.length():
                self.hit = True
                self.sprite = self.img_explode
                self.time_remained = 0
            else:
                dirvect.normalize()
                dirvect.scale_to_length(globalvariable.BIG_BULLET_VEL)
                self.rect.move_ip(dirvect)
                self.sprite = self.images[self.index]
        self.time_remained += 1



class SmallBullet(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height, scale):
        super().__init__()
        self.images = []
        image = pygame.transform.scale(pygame.image.load("asset/img/boss/Battle turtle/Bullet1.png"), (width, height))
        # self.img = pygame.Surface((image.get_width(), image.get_height()), pygame.SRCALPHA)
        # self.img.blit(image, (0, 0), (0, 0, image.get_width(), image.get_height()))
        image_flipped = pygame.transform.flip(image, True, False)
        img = pygame.Surface((image.get_width(), image.get_height()), pygame.SRCALPHA)
        img_flipped = pygame.Surface((image_flipped.get_width(), image.get_height()), pygame.SRCALPHA)
        img.blit(image, (0, 0))
        img_flipped.blit(image_flipped, (0, 0))
        self.images.append(img)
        self.images.append(img_flipped)
        self.rect = pygame.Rect(x, y, width * scale, height * scale)
        self.index = 0
        self.release = False

    def draw(self, screen):
        screen.blit(self.images[self.index], self.rect)

    def move(self, dx, dy):
        self.rect.x += dx
        self.rect.y += dy

    def move_towards_player(self, player, over):
        if self.rect.x > player.rect.x:
            self.index = 0
        else:
            self.index = 1
        dirvect = pygame.math.Vector2(player.rect.x + player.rect.width / 2 - self.rect.x,
                                      player.rect.y + player.rect.height / 2 - self.rect.y)
        if dirvect.length() <= 20:
            self.release = True
        print(f"{dirvect.length()}     {self.release}")
        if globalvariable.BULLET_VEL >= dirvect.length():
            over = True
        else:
            if self.release:
                if self.index == 1:
                    self.move(globalvariable.BULLET_VEL, 0)
                else:
                    self.move(-globalvariable.BULLET_VEL, 0)
            else:
                dirvect.normalize()
                dirvect.scale_to_length(globalvariable.BULLET_VEL)
                self.rect.move_ip(dirvect)
        return over


class Rock(pygame.sprite.Sprite):
    GRAVITY = 0.5
    image = pygame.transform.scale(pygame.image.load("asset/img/weapon/rock.png"), (50, 50))
    sur_img = pygame.Surface((image.get_width(), image.get_height()), pygame.SRCALPHA)
    sur_img.blit(image, (0, 0), (0, 0, image.get_width(), image.get_height()))

    def __init__(self, x):
        super().__init__()
        self.rect = self.sur_img.get_rect()
        self.rect.x = x
        self.rect.y = -30
        self.fall_count = 0

    def draw(self, screen):
        screen.blit(self.image, self.rect)

    def fall(self, vel, fps):
        self.rect.y += vel + min(1, (self.fall_count / fps) * self.GRAVITY)
        self.fall_count += 1


# width = 12 , height = 22
class Saw(pygame.sprite.Sprite):
    ANIMATION_DELAY = 3

    def __init__(self, x, y, width, height, scale):
        super().__init__()
        self.rect = pygame.Rect(x, y, width * scale, height * scale)
        self.SPRITES = get_sprite_sheet("saw.png", width, height, scale)
        self.animation_count = 0
        self.move = 0

    def move_up(self):
        if self.animation_count > globalvariable.SAW_DOWN and self.move >= 0:
            self.rect.y += 1
            self.move -= 1
        elif self.move < self.rect.height:
            self.rect.y -= 1
            self.move += 1
        # print(str(self.animation_count)+" "+str(self.move))

    def draw(self, screen):
        screen.blit(self.SPRITES[(self.animation_count //
                                  self.ANIMATION_DELAY) % len(self.SPRITES)], self.rect)
        self.animation_count += 1


class HitButton(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height, scale):
        super().__init__()
        self.rect = pygame.Rect(x, y, width * scale, height * scale)
        self.SPRITES = get_sprite_sheet("hit_button.png", width, height, scale)
        self.move = 0
        self.state = 0
        self.clickable = False

    def move_up(self):
        if self.move < self.rect.height:
            self.rect.y -= 1
            self.move += 1
        else:
            self.clickable = True

    def draw(self, screen):
        screen.blit(self.SPRITES[self.state], self.rect)


class Lightning:
    ANIMATION_DELAY = 3

    def __init__(self, x, y, width, height, scale):
        super().__init__()
        self.rect = pygame.Rect(x, y, width * scale, height * scale)
        self.SPRITES = get_sprite_sheet("lightning.png", width, height, scale)
        self.animation_count = 0

    def set_pos(self, x, y):
        self.rect.x = x
        self.rect.y = y

    def draw(self, screen):
        screen.blit(self.SPRITES[(self.animation_count //
                                  self.ANIMATION_DELAY) % len(self.SPRITES)], self.rect)
        self.animation_count += 1
