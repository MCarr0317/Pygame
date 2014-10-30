#-------------------------------------------------------------------------------
# Name:        Grid designer
# Purpose:
#
# Author:      Matt Carr
#
# Created:     25/02/2014
# Copyright:   (c) Matt 2014
# Licence:     <your licence>
#-------------------------------------------------------------------------------
import pygame, sys, config
from config import *
from pygame.locals import *



def main(screen):


    SIZE = config.GRID_WIDTH * (config.BOX_WIDTH + config.MARGIN) + config.MARGIN, config.GRID_HEIGHT* (config.BOX_HEIGHT+config.MARGIN)

    #COLORS-------------
    BLACK = (0, 0, 0)
    WHITE = (255, 255, 255)
    BLUE  = (0, 0, 200)

    grid_pos_x = grid_pos_y = 0
    mouse_x = mouse_y = 0
    point_list = []
    drag = False

    def draw_screen():
        for x in range(config.GRID_WIDTH):
            for y in range(config.GRID_HEIGHT):
                if (x, y) in point_list:
                    pygame.draw.rect(config.screen, BLUE, [(config.MARGIN+config.BOX_WIDTH) * x + config.MARGIN, (config.MARGIN+config.BOX_HEIGHT) * y, config.BOX_WIDTH, config.BOX_HEIGHT])
                else:
                    pygame.draw.rect(config.screen, WHITE, [(config.MARGIN+config.BOX_WIDTH) * x + config.MARGIN, (config.MARGIN+config.BOX_HEIGHT) * y, config.BOX_WIDTH, config.BOX_HEIGHT])

    def push():
        pass



    while True: #main loop------------------------------------------------------

        #create surface
        #screen = pygame.display.set_mode(SIZE)
        screen.fill(BLACK)



        draw_screen()

        for event in pygame.event.get():
            key = pygame.key.get_pressed()
            if event.type == QUIT:
                return
            if key[K_RETURN]:
                drag = not drag

            if event.type == pygame.MOUSEBUTTONDOWN and not drag:
                mouse_x, mouse_y = pygame.mouse.get_pos()
                grid_pos_x = int(mouse_x / (config.BOX_WIDTH + config.MARGIN))
                grid_pos_y = int(mouse_y / (config.BOX_HEIGHT + config.MARGIN))

                if (grid_pos_x, grid_pos_y) not in point_list:
                    point_list.append((grid_pos_x, grid_pos_y))
                elif (grid_pos_x, grid_pos_y) in point_list:
                    point_list.remove((grid_pos_x, grid_pos_y))

            if event.type == pygame.MOUSEMOTION and drag:
                mouse_x, mouse_y = pygame.mouse.get_pos()
                grid_pos_x = int(mouse_x / (config.BOX_WIDTH + config.MARGIN))
                grid_pos_y = int(mouse_y / (config.BOX_HEIGHT + config.MARGIN))

                if (grid_pos_x, grid_pos_y) not in point_list:
                    point_list.append((grid_pos_x, grid_pos_y))



            if key[K_p]:
                f = open(config.grid_file, 'w')
                string = ''
                for i in xrange(len(point_list)):
                    string += str(point_list[i]) + '\n'

                print string
                f.write(string)
                f.close()
                print "written to file"


        pygame.display.update()
