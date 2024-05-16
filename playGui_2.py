import sys

import client
import globalvariable
import pygame

import main
import slime
import Button

clock = pygame.time.Clock()

pygame.init()
Screen=pygame.display.set_mode((globalvariable.SCREEN_WIDTH, globalvariable.SCREEN_HEIGHT))

white=(255, 255, 255)
white_smoke=(245, 245, 245)
black=(0, 0, 0)
goldMetalic=(212,175,55)
goldenrod_shadow=(164,125,25)
font_link="game_font/Grand9K Pixel.ttf"

background_menu=pygame.image.load("images/background_1.jpg")
background_guide=pygame.image.load("images/1.png")
fix_brguide = pygame.transform.scale(background_guide, (960, 640))


def name_width_size(name, font_size):
    font_shadow = pygame.font.Font(font_link, font_size)
    text_shadow = font_shadow.render(name, True, black)
    return text_shadow.get_width()

def name_height_size(name, font_size):
    font_shadow = pygame.font.Font(font_link, font_size)
    text_shadow = font_shadow.render(name, True, black)
    return text_shadow.get_height()

s_red_button = Button.Button(70 + 96 - name_width_size("Red", 40) // 2, 400, 40, white, goldMetalic, "Red")
s_blue_button = Button.Button(385 + 96 - name_width_size("Blue", 40) // 2, 400, 40, white, goldMetalic, "Blue")
s_green_button = Button.Button(700 + 96 - name_width_size("Green", 40) // 2, 400, 40, white, goldMetalic, "Green")

def drawTitle(name):
    font = pygame.font.Font(font_link, 95)
    text_shadow = font.render(name, True, black)
    Screen.blit(text_shadow, (globalvariable.SCREEN_WIDTH // 2 - text_shadow.get_width() // 2 + 5, 15))
    text = font.render(name, True, (208, 240, 192))
    Screen.blit(text, (globalvariable.SCREEN_WIDTH // 2 - text.get_width() // 2, 10))

def drawName(name, x, y, font_size, color):
    font_shadow = pygame.font.Font(font_link, font_size)
    text_shadow = font_shadow.render(name, True, black)
    Screen.blit(text_shadow, (x+4, y+4))

    text = font_shadow.render(name, True, color)
    Screen.blit(text, (x, y))

def menu():
    play_button=Button.Button(280, 180, 40, white, goldMetalic, "Play")
    instruction_button = Button.Button(280, 240, 40, white, goldMetalic, "How to play")
    quit_button = Button.Button(280, 300, 40, white, goldMetalic, "Quit")
    while True:
        Screen.blit(background_menu, (-20, -400))
        pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)
        mouse_position=pygame.mouse.get_pos()
        drawTitle("SlimeGame")
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type==pygame.MOUSEBUTTONDOWN:
                if play_button.clicked(mouse_position, event) :
                    play_menu()
                    break
                if instruction_button.clicked(mouse_position, event) :
                    guide()
                    break
                if quit_button.clicked(mouse_position, event) :
                    pygame.quit()
                    sys.exit()

        if play_button.hover_over(mouse_position):
            play_button.blit_hover_over(Screen, black)
        else:
            play_button.blit(Screen, black)
        if instruction_button.hover_over(mouse_position):
            instruction_button.blit_hover_over(Screen, black)
        else:
            instruction_button.blit(Screen, black)
        if quit_button.hover_over(mouse_position):
            quit_button.blit_hover_over(Screen, black)
        else:
            quit_button.blit(Screen, black)

        clock.tick(60)
        pygame.display.flip()
        pygame.display.update()

def guide():
    back_button=Button.Button(10, 580, 40, white, goldMetalic, "Back")
    play_button = Button.Button(865, 580, 40, white, goldMetalic, "Play")
    while True:
        Screen.blit(fix_brguide, (0, 0))
        drawTitle("How To Play")
        pygame.draw.rect(Screen, (128, 128, 128), (50, 190, 350, 390))
        drawName("Singleplayer", 50+175-name_width_size("Singleplayer", 50) // 2, 180-name_height_size("Singleplayer", 50) // 2, 50, white)
        pygame.draw.rect(Screen, (128, 128, 128), (410, 190, 500, 390))
        drawName("Multiplayer", 410 + 250 - name_width_size("Multiplayer", 50) // 2, 180 - name_height_size("Singleplayer", 50) // 2, 50, white)
        mouse_position=pygame.mouse.get_pos()
        pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                if back_button.clicked(mouse_position, event):
                    menu()
                    break
                if play_button.clicked(mouse_position, event):
                    play_menu()
                    break

        if back_button.hover_over(mouse_position):
            back_button.blit_hover_over(Screen, black)
        else:
            back_button.blit(Screen, black)
        if play_button.hover_over(mouse_position):
            play_button.blit_hover_over(Screen, black)
        else:
            play_button.blit(Screen, black)

        pygame.display.update()

def play_menu():
    single_button=Button.Button(320, 240, 40, white, goldMetalic, "Singleplayer")
    multi_button = Button.Button(320, 300, 40, white, goldMetalic, "Multiplayer")
    back_button = Button.Button(10, 580, 40, white, goldMetalic, "Back")
    while True:
        Screen.blit(background_menu, (-20, -400))
        drawTitle("SlimeGame")
        font_btn = pygame.font.Font(font_link, 40)

        text_buttonshadow = font_btn.render("Play", True, black)
        Screen.blit(text_buttonshadow, (283, 183))

        text_btn = font_btn.render("Play", True, white)
        Screen.blit(text_btn, (280, 180))

        mouse_position=pygame.mouse.get_pos()
        pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                if single_button.clicked(mouse_position, event):
                    singleplayer()
                    break
                if multi_button.clicked(mouse_position, event):
                    # IPAdressText()
                    client.main()
                    break
                if back_button.clicked(mouse_position, event):
                    menu()
                    break

        if single_button.hover_over(mouse_position):
            single_button.blit_hover_over(Screen, black)
        else:
            single_button.blit(Screen, black)
        if multi_button.hover_over(mouse_position):
            multi_button.blit_hover_over(Screen, black)
        else:
            multi_button.blit(Screen, black)
        if back_button.hover_over(mouse_position):
            back_button.blit_hover_over(Screen, black)
        else:
            back_button.blit(Screen, black)

        pygame.display.update()

def singleplayer():
    red_choose("Singleplayer", 1)

def red_choose(name, player, color_player_1 = None):
    back_button=Button.Button(10, 580, 40, white, goldMetalic, "Back")
    play_button = Button.Button(865, 580, 40, white, goldMetalic, "Play")
    s_red = slime.Slime(130, 340, "Red_Slime - Copy", 1.5)
    s_blue = slime.Slime(440, 340, "Blue_Slime - Copy", 1.5)
    s_green = slime.Slime(750, 340, "Green_Slime - Copy", 1.5)
    while True:
        Screen.blit(fix_brguide, (0, 0))
        s_red.draw(Screen)
        s_blue.draw(Screen)
        s_green.draw(Screen)
        drawTitle(name)
        drawName("Slime Color", 50, 180, 50, white)

        mouse_position=pygame.mouse.get_pos()
        pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)
        s_red_button.blit_hover_over(Screen, black)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                if s_blue_button.clicked(mouse_position, event):
                    blue_choose(name, player ,color_player_1)
                    break

                if s_green_button.clicked(mouse_position, event):
                    green_choose(name, player, color_player_1)
                    break

                if back_button.clicked(mouse_position, event):
                    menu()
                    break

                if play_button.clicked(mouse_position, event):
                    main.main("Red")
                    break


        s_red_button.blit_hover_over(Screen, black)
        if s_blue_button.hover_over(mouse_position):
            s_blue_button.blit_hover_over(Screen, black)
        else:
            s_blue_button.blit(Screen, black)
        if s_green_button.hover_over(mouse_position):
            s_green_button.blit_hover_over(Screen, black)
        else:
            s_green_button.blit(Screen, black)
        if back_button.hover_over(mouse_position):
            back_button.blit_hover_over(Screen, black)
        else:
            back_button.blit(Screen, black)
        if play_button.hover_over(mouse_position):
            play_button.blit_hover_over(Screen, black)
        else:
            play_button.blit(Screen, black)

        pygame.display.update()

        clock.tick(60)

def blue_choose(name, player ,color_player_1 = None):
    back_button = Button.Button(10, 580, 40, white, goldMetalic, "Back")
    play_button = Button.Button(865, 580, 40, white, goldMetalic, "Play")
    s_red = slime.Slime(130, 340, "Red_Slime - Copy", 1.5)
    s_blue = slime.Slime(440, 340, "Blue_Slime - Copy", 1.5)
    s_green = slime.Slime(750, 340, "Green_Slime - Copy", 1.5)
    while True:
        Screen.blit(fix_brguide, (0, 0))
        s_red.draw(Screen)
        s_blue.draw(Screen)
        s_green.draw(Screen)
        drawTitle(name)
        drawName("Slime Color", 50, 180, 50, white)

        mouse_position = pygame.mouse.get_pos()
        pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)
        s_red_button.blit_hover_over(Screen, black)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                if s_red_button.clicked(mouse_position, event):
                    red_choose(name, player, color_player_1)
                    break

                if s_green_button.clicked(mouse_position, event):
                    green_choose(name, player, color_player_1)
                    break

                if back_button.clicked(mouse_position, event):
                    menu()
                    break

                if play_button.clicked(mouse_position, event):
                    main.main("Blue")
                    break


        s_blue_button.blit_hover_over(Screen, black)
        if s_red_button.hover_over(mouse_position):
            s_red_button.blit_hover_over(Screen, black)
        else:
            s_red_button.blit(Screen, black)
        if s_green_button.hover_over(mouse_position):
            s_green_button.blit_hover_over(Screen, black)
        else:
            s_green_button.blit(Screen, black)
        if back_button.hover_over(mouse_position):
            back_button.blit_hover_over(Screen, black)
        else:
            back_button.blit(Screen, black)
        if play_button.hover_over(mouse_position):
            play_button.blit_hover_over(Screen, black)
        else:
            play_button.blit(Screen, black)

        pygame.display.update()

        clock.tick(60)

def green_choose(name, player, color_player_1 = None):
    back_button = Button.Button(10, 580, 40, white, goldMetalic, "Back")
    play_button = Button.Button(865, 580, 40, white, goldMetalic, "Play")
    s_red = slime.Slime(130, 340, "Red_Slime - Copy", 1.5)
    s_blue = slime.Slime(440, 340, "Blue_Slime - Copy", 1.5)
    s_green = slime.Slime(750, 340, "Green_Slime - Copy", 1.5)
    while True:
        Screen.blit(fix_brguide, (0, 0))
        s_red.draw(Screen)
        s_blue.draw(Screen)
        s_green.draw(Screen)
        drawTitle(name)

        drawName("Slime Color", 50, 180, 50, white)
        mouse_position = pygame.mouse.get_pos()
        pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)
        s_red_button.blit_hover_over(Screen, black)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                if s_red_button.clicked(mouse_position, event):
                    red_choose(name, player, color_player_1)
                    break

                if s_blue_button.clicked(mouse_position, event):
                    blue_choose(name, player, color_player_1)
                    break

                if back_button.clicked(mouse_position, event):
                    menu()
                    break

                if play_button.clicked(mouse_position, event):
                    main.main("Green")
                    break


        s_green_button.blit_hover_over(Screen, black)
        if s_red_button.hover_over(mouse_position):
            s_red_button.blit_hover_over(Screen, black)
        else:
            s_red_button.blit(Screen, black)
        if s_blue_button.hover_over(mouse_position):
            s_blue_button.blit_hover_over(Screen, black)
        else:
            s_blue_button.blit(Screen, black)
        if back_button.hover_over(mouse_position):
            back_button.blit_hover_over(Screen, black)
        else:
            back_button.blit(Screen, black)
        if play_button.hover_over(mouse_position):
            play_button.blit_hover_over(Screen, black)
        else:
            play_button.blit(Screen, black)

        pygame.display.update()

        clock.tick(60)

def multiplayer():
    red_choose("Multiplayer", 2)

def IPAdressText():
    back_button = Button.Button(10, 580, 40, white, goldMetalic, "Back")
    next_button = Button.Button(845, 580, 40, white, goldMetalic, "Next")
    font = pygame.font.Font(font_link, 25)
    user_text = ''
    input_shadow = pygame.Rect(325, 245, 500, 50)
    input = pygame.Rect(320, 240, 500, 50)
    active = False
    caret_position = 0

    while True:
        Screen.blit(fix_brguide, (0, 0))
        drawTitle("Server Address")
        drawName("IP Address :", 100, (240+(60/2))-(name_height_size("IP Adress :", 32)/2), 32, white)
        pygame.draw.rect(Screen, black, input_shadow)
        pygame.draw.rect(Screen, white, input)
        text_surface = font.render(user_text, True, black)
        Screen.blit(text_surface, (input.x + 5, input.y + 5))
        mouse_position = pygame.mouse.get_pos()
        pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if back_button.clicked(mouse_position, event):
                play_menu()
                break

            if next_button.clicked(mouse_position, event):
                multiplayer()
                break

            if event.type == pygame.MOUSEBUTTONDOWN:
                if input.collidepoint(event.pos):
                    active = True
                else:
                    active = False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_BACKSPACE:
                    if caret_position >0:
                        user_text=user_text[:caret_position-1] + user_text[caret_position:]
                        caret_position -=1
                elif event.key ==pygame.K_RIGHT:
                    caret_position=min(caret_position+1, len(user_text))
                elif event.key == pygame.K_LEFT:
                    caret_position=max(caret_position-1, 0)
                else:
                    user_text=user_text[:caret_position]+ event.unicode + user_text[caret_position:]
                    caret_position+=1

        if active:
            draw_caret(Screen, 325+ font.size(user_text[:caret_position])[0], 205, 32)
        if back_button.hover_over(mouse_position):
            back_button.blit_hover_over(Screen, black)
        else:
            back_button.blit(Screen, black)
        if next_button.hover_over(mouse_position):
            next_button.blit_hover_over(Screen, black)
        else:
            next_button.blit(Screen, black)

        pygame.display.flip()

        clock.tick(60)

def draw_caret(surface, x, y, height):
    pygame.draw.line(surface, black, (x, y), (x, y + height))

menu()