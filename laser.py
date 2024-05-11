import pygame
import random

# Khai báo một số màu sắc
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Khởi tạo Pygame
pygame.init()

# Khởi tạo cửa sổ
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Random Laser")

# Class cho Laser
class Laser(pygame.sprite.Sprite):
    def __init__(self, x, y, direction):
        super().__init__()
        self.image = pygame.Surface((1500, 10))
        self.image.fill(WHITE)
        self.rect = self.image.get_rect(center=(x, y))
        self.direction = direction
        self.speed = 10

    def update(self):
        self.rect.x += self.speed * self.direction[0]
        self.rect.y += self.speed * self.direction[1]

# Group để chứa các laser
all_sprites = pygame.sprite.Group()

# Vòng lặp chính
running = True
clock = pygame.time.Clock()
while running:
    screen.fill(BLACK)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Tạo laze ngẫu nhiên
    if random.randint(0, 100) < 5:  # Một số ngẫu nhiên để quyết định xem có tạo laze mới không
        x = random.randint(0, WIDTH)
        y = random.randint(0, HEIGHT)
        # Phải sang trái
        direction = (-1,0)
        laser = Laser(WIDTH, y, direction)
        # Trái sang phải
        # direction = (1, 0)
        # laser = Laser(0, y, direction)
        all_sprites.add(laser)

    # Cập nhật và vẽ tất cả các laser
    all_sprites.update()
    all_sprites.draw(screen)

    pygame.display.flip()
    clock.tick(60)

pygame.quit()