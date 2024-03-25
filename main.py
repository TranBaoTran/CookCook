import pygame
from pygame import font

import globalvariable
import slime
import timer
import pytmx
import character

pygame.init()
SCREEN_COLOR = (255, 255, 255)
win = pygame.display.set_mode((globalvariable.SCREEN_WIDTH, globalvariable.SCREEN_HEIGHT),
                              pygame.RESIZABLE | pygame.DOUBLEBUF)
pygame.display.set_caption("SlimeGame")
map_path = "map01.tmx"
bg_img = pygame.image.load("asset/img/craftpix-net-800370-free-nature-backgrounds-pixel-art/nature_5/orig.png")
tiled_map = pytmx.load_pygame(map_path)
game_over = False
bg = pygame.transform.scale(pygame.image.load("asset/img/restart/Background.png"),
                            (globalvariable.SCREEN_WIDTH, globalvariable.SCREEN_HEIGHT))
star = pygame.transform.scale(pygame.image.load("asset/img/restart/star.png"), (50, 50))
f = pygame.font.Font('Grand9k Pixel.ttf', 40)
score_text = f.render('Score :', True, (255, 255, 255))
time_text = f.render('Time :', True, (255, 255, 255))
number_of_star = 1
restart_img = pygame.image.load("asset/img/restart/restart_btn.png")


class Button:
    def __init__(self, x, y, image):
        self.image = image
        self.rect = image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.clicked = False

    def draw(self, screen):
        action = False
        pos = pygame.mouse.get_pos()
        if self.rect.collidepoint(pos):
            if pygame.mouse.get_pressed()[0] == 1 and not self.clicked:
                action = True
                self.clicked = True
        if pygame.mouse.get_pressed()[0] == 0:
            self.clicked = False
        screen.blit(self.image, self.rect)
        return action


restart_button = Button((globalvariable.SCREEN_WIDTH - restart_img.get_width()) / 2,
                        globalvariable.SCREEN_HEIGHT / 2.5 + score_text.get_height() * 3, restart_img)


def restartGame(screen, time):
    screen.blit(bg, (0, 0))
    screen.blit(score_text, (
        (globalvariable.SCREEN_WIDTH - (score_text.get_width() + number_of_star * (star.get_width() + 50))) / 2,
        globalvariable.SCREEN_HEIGHT / 2.5))
    for i in range(1, number_of_star + 1):
        screen.blit(star, ((globalvariable.SCREEN_WIDTH - (
                score_text.get_width() + i * (star.get_width() + 50))) / 2 + score_text.get_width(),
                           globalvariable.SCREEN_HEIGHT / 2.5 + score_text.get_height() / 8))
    screen.blit(time_text, (
        (globalvariable.SCREEN_WIDTH - (score_text.get_width() + number_of_star * (star.get_width() + 50))) / 2,
        globalvariable.SCREEN_HEIGHT / 2.5 + score_text.get_height()))
    timer_text = f.render(time.timer_text, True, (255, 255, 255))
    screen.blit(timer_text, ((globalvariable.SCREEN_WIDTH - (
            score_text.get_width() + number_of_star * (star.get_width() + 50))) / 2 + score_text.get_width(),
                             globalvariable.SCREEN_HEIGHT / 2.5 + score_text.get_height() * 9 / 8))
    return restart_button.draw(screen)


def drawMap(screen):
    screen.blit(bg_img, (0, 0))
    for layer in tiled_map.visible_layers:
        if isinstance(layer, pytmx.TiledTileLayer):
            for x, y, gid in layer:
                tile = tiled_map.get_tile_image_by_gid(gid)
                if tile:
                    screen.blit(tile, (x * tiled_map.tilewidth, y * tiled_map.tileheight))


blocks = []


def getGround():
    for obj in tiled_map.get_layer_by_name("trigger"):
        rect = pygame.Rect(obj.x, obj.y, obj.width, obj.height)
        blocks.append({"name": obj.name, "rect": rect})


def redrawWindow(screen, player, time, offset_x):
    # screen.fill(SCREEN_COLOR)
    drawMap(screen)
    player.draw(screen, offset_x)
    time.draw(screen)
    pygame.display.flip()


def collide(player, dx):
    player.move(dx, 0)
    player.update()
    collided_object = None
    for obj in blocks:
        if player.rect.colliderect(obj["rect"]):
            collided_object = obj

    player.move(-dx, 0)
    player.update()
    return collided_object


def handle_vertical_collision(player, dy):
    collided_objects = []
    for obj in blocks:
        if player.rect.colliderect(obj["rect"]):
            if dy > 0:
                player.rect.bottom = obj["rect"].top
                player.landed()
            elif dy < 0:
                player.rect.top = obj["rect"].bottom
                player.hit_head()

            collided_objects.append(obj)

    return collided_objects


def handle_move(player, over):
    keys = pygame.key.get_pressed()

    player.x_vel = 0
    collide_left = collide(player, -globalvariable.PLAYER_VEL * 2)
    collide_right = collide(player, globalvariable.PLAYER_VEL * 2)

    if keys[pygame.K_LEFT] and not collide_left and player.rect.x > 0:
        player.move_left(globalvariable.PLAYER_VEL)
    if keys[pygame.K_RIGHT] and not collide_right and player.rect.right < globalvariable.SCREEN_WIDTH:
        player.move_right(globalvariable.PLAYER_VEL)

    vertical_collide = handle_vertical_collision(player, player.y_vel)
    to_check = [collide_left, collide_right, *vertical_collide]

    for obj in to_check:
        if obj and obj["name"] != "ground":
            over = True

    return over


def main():
    global game_over
    run = True
    # s = slime.Slime(0, 0, "Red_Slime", 0.7)
    player = character.Player(200, 100, 30, 50, 0.5)
    offset_x = 0
    clock = pygame.time.Clock()
    timer.GameTime.initialize_font()
    time = timer.GameTime(10, 10)
    getGround()
    while run:
        clock.tick(globalvariable.FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and player.jump_count < 2:
                    player.jump()
        if game_over:
            if restartGame(win, time):
                game_over = False
                player.reset(200, 100, 30, 50, 0.5)
                time.reset()
            pygame.display.flip()
        else:
            player.loop(globalvariable.FPS)
            time.update()
            game_over = handle_move(player, game_over)
            redrawWindow(win, player, time, offset_x)
        if player.rect.top > globalvariable.SCREEN_HEIGHT:
            game_over = True
    pygame.quit()


if __name__ == '__main__':
    main()
