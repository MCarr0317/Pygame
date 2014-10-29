#-------------------------------------------------------------------------------
# Name:        Paddle Class
# Purpose:
#
# Author:      Matt
#
# Created:     12/04/2014
# Copyright:   (c) Matt 2014
# Licence:     <your licence>
#-------------------------------------------------------------------------------

import pygame
from config import *

class Paddle():
    """ PRE: None
        POST: paddle object created, paddle's x movement defined
        DESCR: initializes paddle as a rectangle with a certain x movement
    """
    def __init__(self, PADDLE_DIMENSIONS):
        self.paddle = pygame.Rect(PADDLE_DIMENSIONS)
        self.paddle_movement_x = 0

    """ PRE: there must exist a paddle object
        POST: paddle is moved a distance of paddle_movement_x
        DESCR: moves the paddle
    """
    def move_paddle(self):
        self.paddle.move_ip(self.paddle_movement_x, 0)
        self.paddle.clamp_ip(SCREEN_AREA)

    """ PRE: there must exist a paddle object
        POST: the paddle is drawn to the screen
        DESCR: draws the paddle to the screen
    """
    def draw_paddle(self):
            pygame.draw.rect(screen, WHITE, self.paddle)


    """ PRE: None
        POST: paddle_movement_x is assigned the value stored in change
        DESCR: the x-axis deviation for paddle movement is changed to the argument passed to it
    """
    def change_movement(self, change):
        self.paddle_movement_x = change
