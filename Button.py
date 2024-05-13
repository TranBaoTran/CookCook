import pygame
font_link="game_font/Grand9K Pixel.ttf"

class Button:
    def __init__(self, x, y, text_size=None, text_color=None, text_hover_over_color=None, text_str="", picture=""):
        self.x=x
        self.y=y
        self. text_size=text_size
        self.text_color=text_color
        self.text_str=text_str
        if text_hover_over_color:
            self.text_hover_over_color=text_hover_over_color
        else:
            self.text_hover_over_color=text_color
        self.picture=picture
        self.condition=False

    def blit(self, screen, outline_color=None):
        if self.picture=="":
            if self.text_str !="":
                font=pygame.font.Font(font_link, self.text_size)
                text=font.render(self.text_str, True, self.text_color)
                outline_text=font.render(self.text_str, True, outline_color)
                text_position=(self.x, self.y)
                outline_text_position=(self.x+3, self.y+3)
                screen.blit(outline_text, outline_text_position)
                screen.blit(text, text_position)

    def hover_over(self, mouse_position):
        font = pygame.font.Font(font_link, self.text_size)
        width, height=font.size(self.text_str)
        if self.picture=="":
            if self.x-1<mouse_position[0]<self.x+width and self.y<mouse_position[1]<self.y+height:
                pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)
                return True
        else:
            if self.x-1<mouse_position[0]<self.x+width and self.y<mouse_position[1]<self.y+width :
                pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)
                return True
        return False

    def blit_hover_over(self, screen, outline_color=None):
        if self.picture=="":
            if self.text_str!="":
                font=pygame.font.Font(font_link, self.text_size)
                text=font.render(self.text_str, True, self.text_hover_over_color)
                outline_text = font.render(self.text_str, True, outline_color)
                text_position=(self.x, self.y)
                outline_text_position = (self.x + 3, self.y + 3)
                screen.blit(outline_text, outline_text_position)
                screen.blit(text, text_position)

    def clicked(self, mouse_position, event, condition=False):
        if self.hover_over(mouse_position):
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    self.condition=condition
                    return True
        return False