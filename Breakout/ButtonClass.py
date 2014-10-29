#-------------------------------------------------------------------------------
# Name:        module1
# Purpose:
#
# Author:      Matt
#
# Created:     02/03/2014
# Copyright:   (c) Matt 2014
# Licence:     <your licence>
#-------------------------------------------------------------------------------
import pygame
from config import *



class Button():
    def __init__(self, caption, coord, fontSize):
        self.coord = coord
        self.height = 30
        self.width = 60
        self.rect = pygame.Rect(coord[0], coord[1], 60, 30)
        self.button_label = pygame.font.Font('C:\Windows\Fonts\Sugabb__.ttf', fontSize)
        self.button_caption = caption
        self.text = self.button_label.render(self.button_caption, 1, (255, 255, 255))


    def pressed(self,mouse):

        if mouse[0] > self.rect.topleft[0]:
            if mouse[1] > self.rect.topleft[1]:
                if mouse[0] < self.rect.bottomright[0]:
                    if mouse[1] < self.rect.bottomright[1]:
                        return True
                    else: return False
                else: return False
            else: return False
        else: return False


    def draw_button(self):
        screen.blit(self.text, self.coord)
