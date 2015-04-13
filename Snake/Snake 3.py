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
            end = [start_pos_x, start_pos_y + num_body_parts]
        elif direction == "left" or direction == "right":
            end = [start_pos_x + num_body_parts, start_pos_y]

        print end

        if abs(start[0] - end[0]) == 0: #if they are on a vertical line

            if direction == "up":
                while end[1] != (start[1]-1):
                    point_list.append([end[0], end[1]])
                    end[1] -= 1

            elif direction == "down":
                while start[1] != (end[1] + 1):
                    point_list.append([start[0], start[1]])
                    start[1] += 1
        elif abs(start[1] - end[1]) == 0: #if they are a horizontal line

            if direction == "left":
                while end[0] != (start[0]-1):
                    point_list.append([end[0], end[1]])
                    end[0] -= 1

            elif direction == "right":
                while start[0] != (end[0] + 1):
                    point_list.append([start[0], start[1]])
                    start[0] += 1

        return [point_list, direction]



    #draws the snake
    def drawBoard(screen):

        for i in range(len(point_list)-1):
            #COOL MIRROR EFFECT-------------------------------------------------
            pygame.draw.rect(screen, black, (mirror_list[i][1] * (BOXSIZE+GAPSIZE), mirror_list[i][0] * (BOXSIZE+GAPSIZE), BOXSIZE, BOXSIZE), 1)

            #actual boxes
            pygame.draw.rect(screen, dark_grey, (point_list[i][0] * (BOXSIZE+GAPSIZE) , point_list[i][1] * (BOXSIZE+GAPSIZE), BOXSIZE, BOXSIZE))

        pygame.draw.rect(screen, red, (point_list[-1][0] * (BOXSIZE+GAPSIZE) , point_list[-1][1] * (BOXSIZE+GAPSIZE), BOXSIZE, BOXSIZE))
        #drawing the food
        pygame.draw.rect(screen, white, (food_pos[0] * (BOXSIZE+GAPSIZE) , food_pos[1] * (BOXSIZE+GAPSIZE), BOXSIZE, BOXSIZE), 0)


    def rand_Direction():
        num = random.randrange(1, 5)
        if num == 1:
            return "up"
        elif num == 2:
            return "down"
        elif num == 3:
            return "left"
        elif num == 4:
            return "right"


    def check_collision(new_pos, new_x, new_y, point_list, mirror_list, num_points):

        #check collisions against itself
        if new_pos in point_list and new_pos != point_list[-1]: # and new_pos != old_pos:
            return True

        #check collisions against mirror
        if new_pos in mirror_list:
            return False

        #DO THIS DIRECTION BASED
        #check collisions against walls
        if new_pos[1] < 0: #top
            new_y = grid_size
            direction = "up"
            return [[new_x, new_y], direction]
        elif new_pos[1] > grid_size -1: #bottom
            new_y = -1
            direction = "down"
            return [[new_x, new_y], direction]
        elif new_pos[0] < 0: #left
            new_x = grid_size
            direction = "left"
            return [[new_x, new_y], direction]
        elif new_pos[0] > grid_size-1: #right
            new_x = -1
            direction = "right"
            return [[new_x, new_y], direction]




    def Generate_food_pos(point_list, mirror_list):
        food_x_pos = random.randrange(0, int(height/(BOXSIZE+GAPSIZE)))
        food_y_pos = random.randrange(0, int(width/(BOXSIZE+GAPSIZE)))
        food_pos = [food_x_pos, food_y_pos]

        while food_pos in point_list or food_pos in mirror_list:
            food_x_pos = random.randrange(0, int(width/(BOXSIZE+GAPSIZE)))
            food_y_pos = random.randrange(0, int(height/(BOXSIZE+GAPSIZE)))
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
    grid_size = 75
    GAPSIZE = 3
    width = (BOXSIZE+GAPSIZE)*grid_size
    height = (BOXSIZE+GAPSIZE)*grid_size
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
    start_pos_y = int(height/(BOXSIZE+GAPSIZE))/2
    mirror_x = start_pos_y
    mirror_y = start_pos_x
    mirror_pos = [mirror_x, mirror_y]
    enemy_direction = rand_Direction()


    #clock and frames-per-second variables------------
    FPS = 20
    clock = pygame.time.Clock()
    start = time.clock()

    #growing and food variables-----------------------
    grow_count = 0
    growth_factor = 10
    grown = True
    placed_food = False
    food_pos = [None, None]

    #initial state------------------------------------
    num_body_parts = 0
    num_points = 150
    paused = False
    new_game = False
    point_list = []
    mirror_list = []

    #initializing the snake
    [point_list, direction] = initialize_snake("down", point_list, [start_pos_x, start_pos_y], num_body_parts)

    mirror_list.append([mirror_x, mirror_y])

    #setting the position of the head of the snake
    if direction == "up" or direction == "left":
        new_x = start_pos_x
        new_y = start_pos_y
        new_pos = [new_x, new_y]
    elif direction == "down":
        new_x = start_pos_x
        new_y = start_pos_y + num_body_parts
        new_pos = [new_x, new_y]
    elif direction == "right":
        new_x = start_pos_x + num_body_parts
        new_y = start_pos_y
        new_pos = [new_x, new_y]


    mirror_pos = [new_pos[1], new_pos[0]]

    sound = pygame.mixer.Sound("bite.wav")


    #fonts
    Arial = pygame.font.SysFont('Arial', 20)







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
                if enemy_direction != "down":
                    enemy_direction = rand_Direction()

            elif key[K_DOWN]:# and key[K_UP] == False and key[K_LEFT] == False and key[K_RIGHT] == False:
                if direction != "up":
                    direction = "down"
                if enemy_direction != "up":
                    enemy_direction = rand_Direction()


            elif key[K_LEFT]:# and key[K_RIGHT] == False and key[K_DOWN] == False and key[K_UP] == False :
                if direction != "right":
                    direction = "left"
                if enemy_direction != "right":
                    enemy_direction = rand_Direction()

            elif key[K_RIGHT]:# and key[K_LEFT] == False and key[K_DOWN] == False and key[K_UP] == False:
                if direction != "left":
                    direction = "right"
                if enemy_direction != "left":
                    enemy_direction = rand_Direction()

            """
            test = rand_Direction()
            while enemy_direction == test:
                test = rand_Direction()

            enemy_direction = test
            """

            if enemy_direction == "up":
                mirror_y -= 1
            elif enemy_direction == "down":
                mirror_y += 1
            elif enemy_direction == "left":
                mirror_x -= 1
            elif enemy_direction == "right":
                mirror_x += 1


            #change x and y positions by direction
            #if DirectionHasBeenChanged == True:
            if direction == "up":
                new_y -= 1
            elif direction == "down":
                new_y += 1
            elif direction == "left":
                new_x -= 1
            elif direction == "right":
                new_x += 1




        #make new position coordinates
        new_pos = [new_x, new_y]
        mirror_pos = [mirror_x, mirror_y]

        #if this position is not in the list, add it
        if new_pos not in point_list:
            point_list.append(new_pos)
            mirror_list.append(mirror_pos)
            if grown == True:               #if the snake has fully grown, remove the end of the snake
                point_list = point_list[1:]
                mirror_list = mirror_list[1:]
            else:
                grow_count += 1             #or else grow the snake by 1
                num_body_parts += 1



        #if no food on board, make food
        if placed_food == False:
            food_pos = Generate_food_pos(point_list, mirror_list)
            placed_food = True


        #draw board and snake
        drawBoard(screen)

        #if the snake it itself
        if check_collision(new_pos, new_x, new_y, point_list, mirror_list, num_points) == True: # or num_points <= 0:
            paused = True
            newgame = Arial.render("Press Enter to start a new game.", True, red)
            screen.blit(newgame, (0, int(height/2)))


        elif check_collision(new_pos, new_x, new_y, point_list, mirror_list, num_points) == False:
            num_points += 1


        #if the snake hit a wall, let it go through
        elif check_collision(new_pos, new_x, new_y, point_list, mirror_list, num_points) != None:
            [new_pos, direction] = check_collision(new_pos, new_x, new_y, point_list, mirror_list, num_points)
            new_x = new_pos[0]
            new_y = new_pos[1]


        #if check_collision(mirror_pos, mirror_x, mirror_y, point_list, mirror_list, num_points) != False and check_collision(mirror_pos, mirror_x, mirror_y, point_list, mirror_list, num_points) != None:
         #   [mirror_pos, direction] = check_collision(mirror_pos, mirror_x, mirror_y, point_list, mirror_list, num_points)
          #  mirror_x = mirror_pos[0]
           # mirror_y = mirror_pos[1]


        #if the snake has eaten the food
        if check_eat_food(new_pos, food_pos):
            background = Random_Background()
            sound.play()
            num_points -= 5
            placed_food = False
            grown = False

        #display score
        label = Arial.render(str(num_points), True, black)
        screen.blit(label, (0, 0))

        #display time
        if paused == False:
            cur_time = time.clock()
        total_time = Arial.render(str(int((cur_time - start))) + " seconds", True, black)
        screen.blit(total_time, (0, height-15))

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
music.play(-1)

while True:
    main()
