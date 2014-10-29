import pygame
from config import *

class Smoke():
    def __init__(self, BALL_DIMENSIONS, ball_direction):
        self.length = 5
        self.smoke = []
        self.x = 0 #width deviation
        self.y = 0 #heighth deviation
        self.num = 1

        #this code creates each part of the smoke trail
        for i in xrange(self.length):
            if ball_direction[0] >= 0 and ball_direction[1] <= 0: #up right
                self.smoke.append(pygame.Rect(BALL_DIMENSIONS[0]-((2*BOX_WIDTH)/abs(ball_direction[1]))* self.num, BALL_DIMENSIONS[1] + ((2*BOX_HEIGHT)/abs(ball_direction[0]))*self.num, BALL_DIMENSIONS[2] - self.x, BALL_DIMENSIONS[3] - self.y))

            elif ball_direction[0] <= 0 and ball_direction[1] <= 0:# up left
                self.smoke.append(pygame.Rect(BALL_DIMENSIONS[0] +(((2*BOX_WIDTH)/abs(ball_direction[1]))* self.num), BALL_DIMENSIONS[1] + (((2*BOX_HEIGHT)/abs(ball_direction[0]))*self.num), BALL_DIMENSIONS[2] - self.x, BALL_DIMENSIONS[3] - self.y))

            elif ball_direction[0] >= 0 and ball_direction[1] >= 0: #down right
                self.smoke.append(pygame.Rect(BALL_DIMENSIONS[0]-((2*BOX_WIDTH)/abs(ball_direction[1]))* self.num, BALL_DIMENSIONS[1] - ((2*BOX_HEIGHT)/abs(ball_direction[0]))*self.num, BALL_DIMENSIONS[2] - self.x, BALL_DIMENSIONS[3] - self.y))

            elif ball_direction[0] <= 0 and ball_direction[1] >= 0: # down left
                self.smoke.append(pygame.Rect(BALL_DIMENSIONS[0]+((2*BOX_WIDTH)/abs(ball_direction[1]))* self.num, BALL_DIMENSIONS[1] - ((2*BOX_HEIGHT)/abs(ball_direction[0]))*self.num, BALL_DIMENSIONS[2] - self.x, BALL_DIMENSIONS[3] - self.y))


            self.x += 2
            self.y += 2
            self.num += 1


    def move_smoke(self, ball_direction):
        for i in xrange(len(self.smoke)):
            self.smoke[i].move_ip(ball_direction)
            self.smoke[i].clamp_ip(SCREEN_AREA)




    def draw_smoke(self):
        for i in xrange(len(self.smoke)-1, 0, -1):
            pygame.draw.ellipse(screen, GREY, self.smoke[i], 0)
