from os.path import join

import pygame


def load_image(image_name, width, height, scale):
    path = join("asset", "img", "weapon")
    image = pygame.image.load(join(path, image_name)).convert_alpha()
    sprites = []
    surface = pygame.Surface((width, height), pygame.SRCALPHA)
    # surface = pygame.Surface((width, height)).convert_alpha()
    surface.blit(image, (0, 0), (0, 0, width, height))
    img = pygame.transform.scale(surface, (width * scale, height * scale))
    for i in range(0, 11):
        sprites.append(pygame.transform.rotate(img, i * 30))
    return sprites

class Rock(pygame.sprite.Sprite):
    GRAVITY = 0.5
    ANIMATION_DELAY = 5

    def __init__(self):
        super().__init__()
        self.sprite
