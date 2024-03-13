import pygame

import globalvariable
import slime
import timer

SCREEN_COLOR = (255, 255, 255)
win = pygame.display.set_mode((globalvariable.SCREEN_WIDTH, globalvariable.SCREEN_HEIGHT))
pygame.display.set_caption("SlimeGame")


def redrawWindow(screen, player, time):
    screen.fill(SCREEN_COLOR)
    player.draw(screen)
    time.draw(screen)
    pygame.display.update()


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
