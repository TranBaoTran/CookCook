import pygame

import globalvariable
import slime

SCREEN_COLOR = (0, 0, 0)
win = pygame.display.set_mode((globalvariable.SCREEN_WIDTH, globalvariable.SCREEN_HEIGHT))
pygame.display.set_caption("SlimeGame")


def redrawWindow(screen, player):
    screen.fill(SCREEN_COLOR)
    player.draw(screen)
    pygame.display.update()


def main():
    run = True
    s = slime.Slime(200, 200, "Blue_Slime", 1)
    clock = pygame.time.Clock()

    while run:
        clock.tick(globalvariable.FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()

        s.move()
        redrawWindow(win, s)


if __name__ == '__main__':
    pygame.init()
    main()
