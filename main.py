import pygame

import globalvariable
import slime
import timer
import pytmx

SCREEN_COLOR = (255, 255, 255)
win = pygame.display.set_mode((globalvariable.SCREEN_WIDTH, globalvariable.SCREEN_HEIGHT))
pygame.display.set_caption("SlimeGame")
map_path = "map01.tmx"
bg_img = pygame.image.load("asset/img/craftpix-net-362692-free-green-zone-tileset-pixel-art/2 Background/Day/1.png")

def redrawWindow(screen, player, time):
    #screen.fill(SCREEN_COLOR)
    tilemap = pytmx.load_pygame(map_path)
    screen.blit(bg_img, (0, 0))
    for layer in tilemap.visible_layers:
        if isinstance(layer, pytmx.TiledTileLayer):
            for x, y, gid in layer:
                tile = tilemap.get_tile_image_by_gid(gid)
                if tile:
                    screen.blit(tile, (x * tilemap.tilewidth, y * tilemap.tileheight))
    player.draw(screen)
    time.draw(screen)
    pygame.display.flip()


def main():
    run = True
    s = slime.Slime(200, 200, "Red_Slime", 0.7)
    clock = pygame.time.Clock()
    timer.GameTime.initialize_font()
    time = timer.GameTime(10,10)

    while run:
        clock.tick(globalvariable.FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()
        s.move()
        time.update()
        redrawWindow(win, s, time)


if __name__ == '__main__':
    pygame.init()
    main()
