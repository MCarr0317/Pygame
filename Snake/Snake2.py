#-------------------------------------------------------------------------------
# Name:        module1
# Purpose:
#
# Author:      Matt
#
# Created:     09/01/2014
# Copyright:   (c) Matt 2014
# Licence:     <your licence>
#-------------------------------------------------------------------------------

import pygame, sys, os, random, time
from pygame.locals import *





def main():

    #this function initializes the snakes position, parameters are initial direction, point list, starting position, and length of the snake
    def initialize_snake(direction, point_list = [], start = [5, 5], num_body_parts = 5):

        if direction == "up" or direction == "down":
            end = [start_pos_x + num_body_parts, start_pos_y]
        elif direction == "left" or direction == "right":
            end = [start_pos_x, start_pos_y + num_body_parts]

        if abs(start[0] - end[0]) == 0: #if they are on a horizontal line

            if direction == "left":
                while end[1] != (start[1]-1):
                    point_list.append([end[0], end[1]])
                    end[1] -= 1

            elif direction == "right":
                while start[1] != (end[1] + 1):
                    point_list.append([start[0], start[1]])
                    start[1] += 1

        elif abs(start[1] - end[1]) == 0: #if they are a vertical line

            if direction == "up":
                while end[0] != (start[0]-1):
                    point_list.append([end[0], end[1]])
                    end[0] -= 1

            elif direction == "down":
                while start[0] != (end[0] + 1):
                    point_list.append([start[0], start[1]])
                    start[0] += 1

        return [point_list, direction]



    #draws the snake
    def drawBoard(screen):

        for i in range(len(point_list)):
            pygame.draw.rect(screen, black, (point_list[i][1] * (BOXSIZE+GAPSIZE) - thickness, point_list[i][0] * (BOXSIZE+GAPSIZE) - thickness, BOXSIZE+thickness, BOXSIZE+thickness), 1)
            pygame.draw.rect(screen, dark_grey, (point_list[i][1] * (BOXSIZE+GAPSIZE) , point_list[i][0] * (BOXSIZE+GAPSIZE), BOXSIZE, BOXSIZE))

        pygame.draw.rect(screen, black, (food_pos[1] * (BOXSIZE+GAPSIZE) - thickness, food_pos[0] * (BOXSIZE+GAPSIZE) - thickness, BOXSIZE + thickness, BOXSIZE+thickness), 1)
        pygame.draw.rect(screen, white, (food_pos[1] * (BOXSIZE+GAPSIZE) , food_pos[0] * (BOXSIZE+GAPSIZE), BOXSIZE, BOXSIZE), 0)




    def check_collision(new_pos, new_x, new_y, point_list):
        #check collisions against itself

        if new_pos in point_list and new_pos != point_list[-1]: # and new_pos != old_pos:
            return True



        #check collisions against walls
        if new_pos[0] < 0:
            new_x = int(height/(BOXSIZE+GAPSIZE))
            return [new_x, new_y]
        elif new_pos[0] >= int(height/(BOXSIZE+GAPSIZE)):
            new_x = -1
            return [new_x, new_y]
        if new_pos[1] < 0:
            new_y = int(width/(BOXSIZE+GAPSIZE))
            return [new_x, new_y]
        elif new_pos[1] >= int(width/(BOXSIZE+GAPSIZE)):
            new_y = -1
            return [new_x, new_y]






    def Generate_food_pos(point_list):
        food_x_pos = random.randrange(0, int(height/(BOXSIZE+GAPSIZE)))
        food_y_pos = random.randrange(0, int(width/(BOXSIZE+GAPSIZE)))
        food_pos = [food_x_pos, food_y_pos]

        while food_pos in point_list:
            food_x_pos = random.randrange(0, int(height/(BOXSIZE+GAPSIZE)))
            food_y_pos = random.randrange(0, int(width/(BOXSIZE+GAPSIZE)))
            food_pos = [food_x_pos, food_y_pos]

        return food_pos


    def check_eat_food(new_pos, food_pos):
        if food_pos == new_pos:
            return True

    #generates 3 integers between 50 and 199 for RGB color values
    def Random_Background():
        rand_Red = random.randrange(150, 200)
        rand_Green = random.randrange(150, 200)
        rand_Blue = random.randrange(150, 200)


        return (rand_Red, rand_Green, rand_Blue)


    #DIMENSIONS---------------------------------------
    BOXSIZE = 10
    thickness = 2
    GAPSIZE = thickness + 1
    width = (BOXSIZE+GAPSIZE)*40 +1
    height = (BOXSIZE+GAPSIZE)*40 +1
    size = [width, height]


    #COLORS-------------------------------------------
    black = (0, 0, 0)
    red = (255, 0, 0)
    green = (0, 152, 0)
    grey = (151, 151, 151)
    dark_grey = (51, 51, 51)
    white = (255, 255, 255)
    background = green

    #positioning variables----------------------------
    start_pos_x = int(width/(BOXSIZE+GAPSIZE))/2
    start_pos_y = int(width/(BOXSIZE+GAPSIZE))/2
    #new_x, new_y = [start_pos_x, start_pos_y]


    #clock and frames-per-second variables------------
    FPS = 20
    clock = pygame.time.Clock()

    #growing and food variables-----------------------
    grow_count = 0
    growth_factor = 10
    grown = True
    placed_food = False
    food_pos = [None, None]

    #initial state------------------------------------
    num_body_parts = 5
    num_points = 0
    paused = False
    new_game = False
    DirectionHasBeenChanged = True
    point_list = []

    #initializing the snake
    [point_list, direction] = initialize_snake("down", point_list, [start_pos_x, start_pos_y], num_body_parts)

    #setting the position of the head of the snake
    if direction == "up" or direction == "left":
        new_x = start_pos_x
        new_y = start_pos_y
        new_pos = [new_x, new_y]
    elif direction == "down":
        new_x = start_pos_x + num_body_parts
        new_y = start_pos_y
        new_pos = [new_x, new_y]
    elif direction == "right":
        new_x = start_pos_x
        new_y = start_pos_y + num_body_parts
        new_pos = [new_x, new_y]



    sound = pygame.mixer.Sound("bite.wav")


    #fonts
    f = pygame.font.SysFont('Arial', 30)









    while True: #main loop------------------------------------------------------

        #create surface
        screen = pygame.display.set_mode(size)

        clock.tick(FPS)
        screen.fill(background)




        for event in pygame.event.get():
            key = pygame.key.get_pressed()
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if key[K_p]:
                paused = not paused
            elif key[K_RETURN]:
                new_game = not new_game



        #change direction when arrow keys pressed
        key = pygame.key.get_pressed()

        if paused == False:
            #print DirectionHasBeenChanged, " ", key[K_LEFT]
            if key[K_UP]:# and key[K_DOWN] == False and key[K_LEFT] == False and key[K_RIGHT] == False:
                if direction != "down":
                    direction = "up"
                    DirectionHasBeenChanged = True

            elif key[K_DOWN]:# and key[K_UP] == False and key[K_LEFT] == False and key[K_RIGHT] == False:
                if direction != "up":
                    direction = "down"
                    DirectionHasBeenChanged = True

            elif key[K_LEFT]:# and key[K_RIGHT] == False and key[K_DOWN] == False and key[K_UP] == False :
                if direction != "right":
                    direction = "left"
                    DirectionHasBeenChanged = True

            elif key[K_RIGHT]:# and key[K_LEFT] == False and key[K_DOWN] == False and key[K_UP] == False:
                if direction != "left":
                    direction = "right"
                    DirectionHasBeenChanged = True



            #change x and y positions by direction
            #if DirectionHasBeenChanged == True:
            if direction == "up":
                new_x -= 1
            elif direction == "down":
                new_x += 1
            elif direction == "left":
                new_y -= 1
            elif direction == "right":
                new_y += 1




        #make new position coordinates
        new_pos = [new_x, new_y]

        #if this position is not in the list, add it
        if new_pos not in point_list:
            point_list.append(new_pos)
            if grown == True:               #if the snake has fully grown, remove the end of the snake
                point_list = point_list[1:]
            else:
                grow_count += 1             #or else grow the snake by 1
                num_body_parts += 1



        #if no food on board, make food
        if placed_food == False:
            food_pos = Generate_food_pos(point_list)
            placed_food = True


        #draw board and snake
        drawBoard(screen)

        #if the snake it itself
        if check_collision(new_pos, new_x, new_y, point_list) == True:
            paused = True
            newgame = f.render("Press Enter to start a new game.", True, black)
            screen.blit(newgame, (0, int(height/2)))

        #if the snake hit a wall, let it go through
        elif check_collision(new_pos, new_x, new_y, point_list) != None:
            new_pos = check_collision(new_pos, new_x, new_y, point_list)
            new_x = new_pos[0]
            new_y = new_pos[1]

        #if the snake has eaten the food
        if check_eat_food(new_pos, food_pos):
            #background = Random_Background()
            sound.play()
            num_points += 1
            placed_food = False
            grown = False

        #display score
        label = f.render(str(num_points), True, black)
        screen.blit(label, (0, 0))

        #determine if we should stop growing
        if grow_count == growth_factor:
            grown = True
            grow_count = 0

        pygame.display.update()


        if new_game == True:
            main()




pygame.init()
pygame.mixer.init()

music = pygame.mixer.Sound("music.ogg")
#music.play(-1)

while True:
    main()
