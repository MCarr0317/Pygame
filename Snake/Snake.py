#-------------------------------------------------------------------------------
# Name:        module1
# Purpose:
#
# Author:      Matt
#
# Created:     01/03/2014
# Copyright:   (c) Matt 2014
# Licence:     <your licence>
#-------------------------------------------------------------------------------
import pygame, sys, os, random
from pygame.locals import *





def main():

    #draws the snake
    def draw_lines(Points):
        if len(Points) <= num_snake_parts:
            pygame.draw.lines(screen, black, False, Points, 4)
        else:
            Points = Points[len(Points)-int(num_snake_parts):len(Points)] # keep the list of points to only that which is displayed
            pygame.draw.lines(screen, black, False, Points, 4)

        circle_x, circle_y = Points[-1]
        circle_x += 1
        circle_y += 1
        pygame.draw.circle(screen, green, (circle_x,circle_y), 3, 0)


        return Points

    #checks if the new_pos is over the food, returns True if so
    def check_eat_food(new_pos, food_pos):
        if abs(new_pos[0]- food_pos[0]) <= 4+2 and abs(new_pos[1] - food_pos[1]) <= 4+2:
            return True


    #checks if the snake has collided with walls or itself
    def check_collision(new_pos, Points):

        #check collisions against walls
        if new_pos[0] < 0 or new_pos[0] >= width:
            return True
        if new_pos[1] < 0 or new_pos[1] >= height:
            return True


        #check collisions against itself
        if new_pos in Points[0:len(Points)-1] and new_pos != old_pos:
            return True

    #generates the pieces of food
    def Generate_food_pos(Points):

        food_x_pos = food_y_pos = 0
        food_pos = [food_x_pos, food_y_pos]

        #while new_pos is over the food OR the first piece hasn't been made yet -> make a new piece             ###########################################################################################
        while check_eat_food(new_pos, food_pos) or (food_x_pos == 0 and food_y_pos == 0): #or food_pos in Points: #can make a function that checks the abs difference of food_pos and every point in Points
            food_x_pos = random.randrange(10, width-10, 1)
            food_y_pos = random.randrange(10, height-10, 1)

            #while Check_open_area(Points, food_pos) == False:
                #food_x_pos = random.randrange(10, width-10, 1)
                #food_y_pos = random.randrange(10, height-10, 1)

                #food_pos = [food_x_pos, food_y_pos]
            ate_food = False

        food_pos = [food_x_pos, food_y_pos]
        return food_pos

    #generates 3 integers between 50 and 199 for RGB color values
    def Random_Background():
        rand_Red = random.randrange(50, 200)
        rand_Green = random.randrange(50, 200)
        rand_Blue = random.randrange(50, 200)


        return (rand_Red, rand_Green, rand_Blue)

    black = (0, 0, 0)
    red = (255, 0, 0)
    green = (0, 152, 0)
    grey = (151, 151, 151)
    white = (255, 255, 255)
    background = Random_Background()
    width = 500
    height = 200
    size = [width, height]
    num_snake_parts = 2 #start as a dot
    thickness = 4

    change_x = 0
    change_y = 0
    start_pos_x = width/2
    start_pos_y = height/2

    screen = pygame.display.set_mode(size)

    old_pos = [start_pos_x, start_pos_y]
    new_pos = old_pos
    new_x, new_y = [start_pos_x, start_pos_y]
    Points = [old_pos]
    direction = "up"
    last_press = None
    Collision = False
    change_amplitude = 1
    FPS = 90
    clock = pygame.time.Clock()
    food_pos = [0,0]
    placed_food = False
    point_val = 0
    start = False

    sound = pygame.mixer.Sound("bite.wav")

    myFont = pygame.font.Font(None, 25)
    label = myFont.render("Press Space To Begin", 1, black)

    while True: #main loop
        changed = False
        clock.tick(FPS)


        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()

            #change direction when arrow keys pressed
            key = pygame.key.get_pressed()
            old_pos = new_pos

            if key[K_SPACE]:
                start = not start
            if start == True:
                if key[K_UP]:
                    if direction != "down":
                        change_y -= change_amplitude
                        direction = "up"
                        changed = True


                elif key[K_DOWN]:
                    if direction != "up":
                        change_y += change_amplitude
                        direction = "down"
                        changed = True


                elif key[K_LEFT]:
                    if direction != "right":
                        change_x -= change_amplitude
                        direction = "left"
                        changed = True


                elif key[K_RIGHT]:
                    if direction != "left":
                        change_x += change_amplitude
                        direction = "right"
                        changed = True

        #if no keys pressed, keep going in the same direction
        if changed == False and start == True:
            if direction == "up":
                change_y -= change_amplitude
            elif direction == "down":
                change_y += change_amplitude
            elif direction == "left":
                change_x -= change_amplitude
            elif direction == "right":
                change_x += change_amplitude


        #make new position coordinates
        new_x, new_y = [start_pos_x + change_x, start_pos_y + change_y]
        new_pos =[new_x, new_y]


        #add new pos to list of points
        Points.append(new_pos)
        screen.fill(background)

        #if no food on board, make food
        if placed_food == False:
            food_pos = Generate_food_pos(Points)
            placed_food = True

        #make food circle
        pygame.draw.circle(screen, white, food_pos, 4, 0)

        #draw snake
        Points = draw_lines(Points)

        if start == False:
            screen.blit(label, (width/2 - 100, height/2))


        pygame.display.update()

        #check if the new snake collided with itself or a wall
        if check_collision(new_pos, Points):
            print "YOU LOSE"
            pygame.time.wait(250)
            return


        if check_eat_food(new_pos, food_pos):
            sound.play()
            print food_pos, Points[-1]
            thickness += 1
            point_val += 1
            print "points: ", point_val
            num_snake_parts += 50
            background = Random_Background()
            placed_food = False



    return




pygame.init()
pygame.mixer.init()

music = pygame.mixer.Sound("music.ogg")
music.play(-1)

while True:
    main()










