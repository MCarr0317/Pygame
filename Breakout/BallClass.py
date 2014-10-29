#-------------------------------------------------------------------------------
# Name:        BallClass
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

class Ball():
    """ PRE: None
        POST: paddle_movement_x is assigned the value stored in change
        DESCR: initializes ball as a rectangle with an up direction
    """
    def __init__(self, BALL_DIMENSIONS):
        self.ball = pygame.Rect(BALL_DIMENSIONS1)
        self.ball_direction = (3, -6)

    """ PRE: There must exist a Ball object
        POST: the ball moves to its new position based on its direction
        DESCR: moves the ball
    """
    def move_ball(self):
        self.ball.move_ip(self.ball_direction)
        self.ball.clamp_ip(SCREEN_AREA)

        BALL_DIMENSIONS = (self.ball.left, self.ball.top, 15, 15)



    """ PRE: there must exist a Ball object
        POST: an ellipse is drawn to the screen using rectangle coordinates
        DESCR: the ball is drawn to the screen
    """
    def draw_ball(self):
            #pygame.draw.rect(screen, WHITE, self.ball)
            pygame.draw.ellipse(screen, WHITE, self.ball)
