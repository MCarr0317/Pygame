#-------------------------------------------------------------------------------
# Name:        module1
# Purpose:  config file
#
# Author:      Matt
#
# Created:     12/04/2014
# Copyright:   (c) Matt 2014
# Licence:     <your licence>
#-------------------------------------------------------------------------------
import pygame
FPS = 100 # framerate
grid_file = "Level1.txt"
LevelList = [grid_file, "Level2.txt", "Level3.txt"]
index = 0

#colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
BLUE  = (0, 0, 255)
GREY  = (127, 127, 127)
RED   = (127, 0, 0)

#block dimensions
BOX_WIDTH = 30
BOX_HEIGHT = 10
MARGIN = 6

#grid dimensions
GRID_WIDTH = 20
GRID_HEIGHT = 50

#screen dimensions
WIDTH = GRID_WIDTH * (BOX_WIDTH + MARGIN) + MARGIN
HEIGHT = GRID_HEIGHT* (BOX_HEIGHT+MARGIN) + 100
SIZE = WIDTH, HEIGHT
screen = pygame.display.set_mode(SIZE)
SCREEN_AREA = pygame.Rect(0, 0, WIDTH, HEIGHT)
speedBoost = 0

#paddle/ball dimensions
CIG_HEIGHT = 15
CIG_WIDTH = 140
PADDLE_DIMENSIONS = 100, HEIGHT, CIG_WIDTH, CIG_HEIGHT
BALL_DIMENSIONS = 15*(BOX_WIDTH+MARGIN)+MARGIN, HEIGHT-200-CIG_HEIGHT-5, 15, 15
BALL_DIMENSIONS1 = 15*(BOX_WIDTH+MARGIN)+MARGIN, HEIGHT-200-CIG_HEIGHT-5, 20, 20

#labels/captions
score_string = "Score: "
newgame_string = "New Game"
startgame_string = "Start Game"
griddesigner_string = "Grid Designer"

#icons
block = pygame.image.load("block.png")
block = pygame.transform.scale(block, (BOX_WIDTH, BOX_HEIGHT))
ball = pygame.image.load("ball.png")
ball = pygame.transform.scale(ball, (20, 20))
