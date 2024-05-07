import random

import pygame

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
game_over = False
bg = pygame.transform.scale(pygame.image.load("asset/img/restart/Background.png"),
                            (globalvariable.SCREEN_WIDTH, globalvariable.SCREEN_HEIGHT))
star = pygame.transform.scale(pygame.image.load("asset/img/restart/star.png"), (50, 50))
f = pygame.font.Font('Grand9k Pixel.ttf', 40)
score_text = f.render('Score :', True, (255, 255, 255))
time_text = f.render('Time :', True, (255, 255, 255))
number_of_star = 3
restart_img = pygame.image.load("asset/img/restart/restart_btn.png")
char_dead = False

red_warning = f.render('Warning! Boss is coming!', True, (255, 0, 0))
white_warning = f.render('Warning! Boss is coming!', True, (247, 226, 30))

event = 0
boss1 = "wait"
rock_slide = pygame.USEREVENT + event
saw_up = pygame.USEREVENT + event + 1
small_bullet_run = pygame.USEREVENT + event + 2

saws = pygame.sprite.Group()
hit_buttons = pygame.sprite.Group()
small_bullets = pygame.sprite.Group()

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
    screen.blit(score_text, (restart_text_width, restart_text_height))
    for i in range(0, number_of_star):
        screen.blit(star, (restart_text_content_width + i * 50,
                           restart_text_height + score_text.get_height() / 8))
    screen.blit(time_text, (restart_text_width, restart_text_height + score_text.get_height()))
    timer_text = f.render(time.timer_text, True, (255, 255, 255))
    screen.blit(timer_text,
                (restart_text_content_width, restart_text_height + score_text.get_height() * 9 / 8))
    return restart_button.draw(screen)


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
boss_blocks = []
hit_button_count = 0
hurt_count = 0


def getGround():
    for obj in tiled_map.get_layer_by_name("trigger"):
        rect = pygame.Rect(obj.x, obj.y, obj.width, obj.height)
        blocks.append({"name": obj.name, "rect": rect})


def getBossGround():
    for obj in tiled_map.get_layer_by_name("groundboss"):
        rect = pygame.Rect(obj.x, obj.y, obj.width, obj.height)
        boss_blocks.append({"name": obj.name, "rect": rect})


ground_boss = character.GroundBoss(-144, 200, 144, 144, 2)

# saw = object.Saw(0, 0, 24, 12, 4 / 3)
# hit_button = object.HitButton(0,0,148,81,0.22)
light = object.Lightning(0, 0, 130, 660, 0.8)


def redrawWindow(screen, player, time, offset_x, rocks):
    # screen.fill(SCREEN_COLOR)
    global boss1
    global hurt_count
    drawMap(screen)

    time.draw(screen)

    for hit_button in hit_buttons.sprites():
        hit_button.draw(win)
    player.draw(screen, offset_x)
    for saw in saws.sprites():
        saw.draw(win)
    # saw.draw(win)
    # hit_button.draw(win)
    drawAllMap(screen)
    if boss1 == "text":
        wt.draw(win)
    elif boss1 == "incoming":
        ground_boss.move_in(globalvariable.PLAYER_VEL)
        ground_boss.loop(globalvariable.FPS)
        ground_boss.x_vel = 0
        boss_vertical_collision(ground_boss, ground_boss.y_vel)
        ground_boss.draw(win)
        if ground_boss.rect.x > 352 - 144:
            boss1 = "alive"
            ground_boss.animation_count = 0
            pygame.time.set_timer(rock_slide, globalvariable.ROCK_TIMER)
            pygame.time.set_timer(saw_up, globalvariable.SAW_TIMER)
            pygame.time.set_timer(small_bullet_run, globalvariable.SMALL_BULLET_TIMER)
            ground_boss.set_sprite_name("Battle_turtle_idle")
            blocks.append({"name": "boss", "rect": ground_boss.rect})

    elif boss1 == "alive" or boss1 == "hurting":
        ground_boss.loop(globalvariable.FPS)
        boss_vertical_collision(ground_boss, ground_boss.y_vel)
        ground_boss.draw(win)

    if boss1 == "hurting":
        light.draw(win)
        hurt_count += 1
        if hurt_count >= globalvariable.HURT_TIME:
            boss1 = "alive"
            hurt_count = 0
            for hit_button in hit_buttons:
                hit_button.kill()
            ground_boss.set_sprite_name("Battle_turtle_idle")

    for rock in rocks:
        rock.draw(win)

    for small_bullet in small_bullets:
        small_bullet.draw(win)

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


def boss_vertical_collision(boss, dy):
    collided_objects = []
    for obj in boss_blocks:
        if boss.rect.colliderect(obj["rect"]) and obj["name"] == "bossground":
            if dy > 0:
                boss.rect.bottom = obj["rect"].top
                boss.landed()

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
            if obj["name"] == "boss":
                ground_boss.set_sprite_name("Battle_turtle_attack2")
            print(obj["name"])
            player.animation_count = 0
            over = True
    return over


def handle_boss_move(boss):
    boss.x_vel = 0
    boss_vertical_collision(boss, boss.y_vel)


def remove_dict_by_name(list_of_dicts, name):
    for item in list_of_dicts:
        if item.get('name') == name:
            list_of_dicts.remove(item)


def main():
    global game_over
    global char_dead
    global event
    global boss1
    global hit_button_count
    run = True
    # s = slime.Slime(0, 0, "Red_Slime", 0.7)
    player = character.Player(200, 100, 28, 50, 0.5)
    rocks = []

    offset_x = 0
    clock = pygame.time.Clock()
    timer.GameTime.initialize_font()
    time = timer.GameTime(10, 10)
    getGround()
    getBossGround()
    while run:
        clock.tick(globalvariable.FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_z and player.jump_count < 2:
                    player.jump()
                if event.key == pygame.K_x:
                    for hit_button in hit_buttons:
                        if pygame.sprite.collide_rect(hit_button, player) and hit_button.clickable and hit_button.state == 0:
                            hit_button.state = 1
                            hit_button_count += 1
                            print(hit_button.rect)
            if event.type == rock_slide:
                rocks.append(object.Rock(player.rect.x))
            if event.type == saw_up:
                for sprite in saws.sprites():
                    sprite.kill()
                for obj in boss_blocks:
                    if random.random() > 0.8:
                        if obj["name"] == "saw":
                            saws.add(object.Saw(obj["rect"].x, obj["rect"].y + obj["rect"].height, 24, 12, 4 / 3))
            # if event.type == small_bullet_run:
            #     small_bullets.add(object.SmallBullet(random.uniform(ground_boss.rect.x - 50, ground_boss.rect.x + 50), random.uniform(ground_boss.rect.y - 50, ground_boss.rect.y + 50), 15,9, 1))

        if time.seconds == 5 and time.count == 0 and time.minutes == 0:
            boss1 = "text"
        elif time.seconds == 10 and time.count == 0 and time.minutes == 0:
            boss1 = "incoming"
            ground_boss.set_sprite_name("Battle_turtle_walk")

        elif time.seconds == 40 and time.count == 0 and time.minutes == 0:
            for obj in boss_blocks:
                if obj["name"] == "hit_button":
                    hit_buttons.add(object.HitButton(obj["rect"].x, obj["rect"].y + obj["rect"].height, 148,81,0.22))

        for rock in rocks:
            if rock.rect.y < globalvariable.SCREEN_HEIGHT:
                if not game_over:
                    rock.fall(globalvariable.ROCK_VEL, globalvariable.FPS)
                    if pygame.sprite.collide_rect(rock, player):
                        player.animation_count = 0
                        game_over = True
                else:
                    rock.fall(1, globalvariable.FPS)
            else:
                tmp = rock
                rocks.pop(rocks.index(rock))
                tmp.kill()

        for saw in saws.sprites():
            saw.move_up()
            if not game_over:
                if pygame.sprite.collide_rect(saw, player):
                    player.animation_count = 0
                    game_over = True

        for hit_button in hit_buttons.sprites():
            hit_button.move_up()

        for small_bullet in small_bullets.sprites():
            game_over = small_bullet.move_towards_player(player, game_over)

        print(hit_button_count)

        if hit_button_count == 2:
            ground_boss.set_sprite_name("Battle_turtle_hurt")
            hit_button_count = 0
            boss1 = "hurting"
            light.set_pos(ground_boss.rect.x,0)

        if game_over:
            if player.die() == 2:
                char_dead = True
            if char_dead:
                if restartGame(win, time):
                    game_over = False
                    char_dead = False

                    player.reset(200, 100, 30, 50, 0.5)
                    time.reset()
                    ground_boss.reset(-144, 200, 144, 144, 2)

                    rocks.clear()
                    for sprite in saws.sprites():
                        sprite.kill()
                    for hit_button in hit_buttons.sprites():
                        hit_button.kill()
                    for small_bullet in small_bullets.sprites():
                        small_bullet.kill()

                    hit_button_count = 0
                    pygame.time.set_timer(rock_slide, 0)
                    pygame.time.set_timer(saw_up, 0)

                    boss1 = "wait"
                    remove_dict_by_name(blocks, "boss")
                pygame.display.flip()
            else:
                redrawWindow(win, player, time, offset_x, rocks)
        else:
            player.loop(globalvariable.FPS)
            time.update()
            game_over = handle_move(player, game_over)
            redrawWindow(win, player, time, offset_x, rocks)

    pygame.quit()


if __name__ == '__main__':
    main()
