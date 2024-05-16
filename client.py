import random
import pygame
from pygame import mixer

from Data import PlayerData
from network import Network

import globalvariable
import timer
import pytmx
import character
import object

pygame.init()
SCREEN_COLOR = (255, 255, 255)
win = pygame.display.set_mode((globalvariable.SCREEN_WIDTH, globalvariable.SCREEN_HEIGHT),
                              pygame.DOUBLEBUF)
pygame.display.set_caption("SlimeGame")
map_path = "map01.tmx"
bg_img = pygame.image.load("asset/img/craftpix-net-800370-free-nature-backgrounds-pixel-art/nature_5/orig.png")
tiled_map = pytmx.load_pygame(map_path)
bg = pygame.transform.scale(pygame.image.load("asset/img/restart/Background.png"),
                            (globalvariable.SCREEN_WIDTH, globalvariable.SCREEN_HEIGHT))
star = pygame.transform.scale(pygame.image.load("asset/img/restart/star.png"), (50, 50))
f = pygame.font.Font('Grand9k Pixel.ttf', 40)
score_text = f.render('Score :', True, (255, 255, 255))
win_text = f.render('You win', True, (255, 255, 255))
lose_text = f.render('You lose', True, (255, 255, 255))
time_text = f.render('Time :', True, (255, 255, 255))
waiting_text = f.render('Waiting for other player...', True, (255, 255, 255))
number_of_star = 0
restart_img = pygame.image.load("asset/img/restart/restart_btn.png")

red_warning = f.render('Warning! Boss is coming!', True, (255, 0, 0))
white_warning = f.render('Warning! Boss is coming!', True, (247, 226, 30))

smallBullet_image = pygame.transform.scale(pygame.image.load("asset/img/boss/Battle turtle/SmallBullet.png"), (9, 9))
img_smallBullet = pygame.Surface((smallBullet_image.get_width(), smallBullet_image.get_height()), pygame.SRCALPHA)
img_smallBullet.blit(smallBullet_image, (0, 0))
bigBullet_image = pygame.transform.scale(pygame.image.load("asset/img/boss/Battle turtle/Bullet1.png"), (45, 27))
bigBullet_image_flipped = pygame.transform.flip(bigBullet_image, True, False)
bigBullet_img = pygame.Surface((bigBullet_image.get_width(), bigBullet_image.get_height()), pygame.SRCALPHA)
bigBullet_img_flipped = pygame.Surface((bigBullet_image_flipped.get_width(), bigBullet_image_flipped.get_height()),
                                       pygame.SRCALPHA)
bigBullet_img.blit(bigBullet_image, (0, 0))
bigBullet_img_flipped.blit(bigBullet_image_flipped, (0, 0))

rocks = pygame.sprite.Group()
saws = pygame.sprite.Group()
hit_buttons = pygame.sprite.Group()
small_bullets = pygame.sprite.Group()
big_bullets = pygame.sprite.Group()
laser_sprites = pygame.sprite.Group()
warn_laser = []

game_over = False
char_dead = False
isWin = False


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


class WarningText:
    ANIMATION_DELAY = 10

    def __init__(self, text):
        self.x = (globalvariable.SCREEN_WIDTH - red_warning.get_width()) / 2
        self.y = 50
        self.text = text
        self.animation_count = 0

    def draw(self, screen):
        screen.blit(self.text[(self.animation_count // self.ANIMATION_DELAY) % 2], (self.x, self.y))
        self.animation_count += 1


wt = WarningText((red_warning, white_warning))

restart_button = Button((globalvariable.SCREEN_WIDTH - restart_img.get_width()) / 2,
                        globalvariable.SCREEN_HEIGHT / 2.5 + score_text.get_height() * 3, restart_img)

restart_text_width = (globalvariable.SCREEN_WIDTH - (score_text.get_width() + star.get_width() + 50)) / 2
restart_text_content_width = restart_text_width + score_text.get_width()
restart_text_height = globalvariable.SCREEN_HEIGHT / 2.5


def restartGame(screen, time):
    screen.blit(bg, (0, 0))
    if isWin:
        screen.blit(win_text, ((globalvariable.SCREEN_WIDTH - win_text.get_width())/2, restart_text_height))
    else:
        screen.blit(lose_text, ((globalvariable.SCREEN_WIDTH - lose_text.get_width())/2, restart_text_height))
    screen.blit(time_text, (restart_text_width, restart_text_height + score_text.get_height()))
    timer_text = f.render(time.die_time, True, (255, 255, 255))
    screen.blit(timer_text,
                (restart_text_content_width, restart_text_height + win_text.get_height() * 9 / 8))
    return restart_button.draw(screen)


def waitingGame(screen):
    screen.blit(bg, (0, 0))
    screen.blit(waiting_text, ((globalvariable.SCREEN_WIDTH - waiting_text.get_width()) / 2,
                               (globalvariable.SCREEN_HEIGHT - waiting_text.get_height()) / 2))


def drawMap(screen):
    screen.blit(bg_img, (0, 0))
    for layer in tiled_map.visible_layers:
        if isinstance(layer, pytmx.TiledTileLayer) and layer.name != "background":
            for x, y, gid in layer:
                tile = tiled_map.get_tile_image_by_gid(gid)
                if tile:
                    screen.blit(tile, (x * tiled_map.tilewidth, y * tiled_map.tileheight))


def drawAllMap(screen):
    for layer in tiled_map.visible_layers:
        if isinstance(layer, pytmx.TiledTileLayer) and layer.name == "background":
            for x, y, gid in layer:
                tile = tiled_map.get_tile_image_by_gid(gid)
                if tile:
                    screen.blit(tile, (x * tiled_map.tilewidth, y * tiled_map.tileheight))


blocks = []
hurt_count = 0


def getGround():
    for obj in tiled_map.get_layer_by_name("trigger"):
        rect = pygame.Rect(obj.x, obj.y, obj.width, obj.height)
        blocks.append({"name": obj.name, "rect": rect})


ground_boss = character.GroundBoss(-144, 200, 144, 144, 2)

light = object.Lightning(0, 0, 130, 660, 0.8)


def redrawWindow(screen, player, player2, time):
    global hurt_count
    drawMap(screen)
    time.draw(screen)

    player.draw(screen)
    player2.draw(screen)

    drawAllMap(screen)

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
            player.animation_count = 0
            over = True
    return over


def remove_dict_by_name(list_of_dicts, name):
    for item in list_of_dicts:
        if item.get('name') == name:
            list_of_dicts.remove(item)


def delete_sprite_list(sprite_group):
    for sprite in sprite_group.sprites():
        sprite.kill()


def main():
    global number_of_star
    global game_over
    global char_dead
    global isWin
    run = True
    click_restart = False

    n = Network()

    p1data = n.getP()
    player = character.Player(p1data.name, p1data.x, p1data.y, 28, 50, 0.5)

    p2data = n.send(p1data)
    player2 = character.Player(p2data.name, p2data.x, p2data.y, 28, 50, 0.5)

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
                if event.key == pygame.K_UP and player.jump_count < 2:
                    player.jump()

        p1data.setVal(player.rect.x, player.rect.y, player.sprite_sheet_name, char_dead)
        try:
            p2data = n.send(p1data)
        except:
            print("Couldn't get game")
            break

        if p1data.respawn and p2data.respawn:
            game_over = False
            char_dead = False
            number_of_star = 0
            click_restart = False
            player.reset(200, 100, 30, 50, 0.5)
            time.reset()
            p1data.respawn = False
            isWin = False

        player2.rect.x = p2data.x
        player2.rect.y = p2data.y
        player2.sprite_sheet_name = p2data.sprite_name

        if p2data.connected == 2:
            pass
        else:
            waitingGame(win)
            pygame.display.flip()
            continue

        if game_over and not char_dead and p2data.die:
            isWin = True
        print(f"{char_dead} {p2data.die} ")

        time.update()

        if game_over:
            if click_restart:
                waitingGame(win)
                pygame.display.flip()
                continue
            if not char_dead and player.die() == 2:
                char_dead = True
                time.die_time = f"{time.minutes:02d}:{time.seconds:02d}"
            if char_dead:
                if p2data.restart:
                    if restartGame(win, time):
                        p1data.respawn = True
                        click_restart = True
                    pygame.display.flip()
                else:
                    player2.update_state()
                    redrawWindow(win, player, player2, time)
            else:
                redrawWindow(win, player, player2, time)
        else:
            player.loop(globalvariable.FPS)
            if not p2data.die:
                player2.update_state()
            game_over = handle_move(player, game_over)
            redrawWindow(win, player, player2, time)

    pygame.quit()


if __name__ == '__main__':
    main()
