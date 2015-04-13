#-------------------------------------------------------------------------------
# Name:        module1
# Purpose:
#
# Author:      Matt
#
# Created:     24/12/2013
# Copyright:   (c) Matt 2013
# Licence:     <your licence>
#-------------------------------------------------------------------------------
"""color matching game

    uses a grid of colors
"""

import pygame, sys, random, time
from pygame.locals import *
from random import shuffle

# Define some colors
black     = (   0,   0,   0)
white     = ( 255, 255, 255)
green     = (   0, 200,   0)
red       = ( 255,   0,   0)
blue      = (   0,   0, 255)
yellow    = ( 255, 255,   0)
pink      = ( 255,  51, 255)
purple    = (  51,   0, 102)
darkgreen = (   0, 102,   0)
darkblue  = ( 153, 153, 255)
darkred   = (  102,  0, 100)

wallpaper = pygame.image.load("wood.jpg")
background= ( 90,   90,  90)

num_block_colors = 10


#sets the grid dimensions
gridW = 6
gridH = 6
# This sets the margin between each cell
margin = 7
# This sets the width and height of each box location
boxwidth  = 50
boxheight = 50

FPS = 60

#variables for choice logic
firstpick = True
secondpick = False
firstrow = -1
firstcolumn = -1
currentrow = -1
currentcolumn = -1


def draw_grid():
    global currentrow, currentcolumn, firstrow, firstcolumn
    #Draw the grid
    for x in range(gridH):
        for y in range(gridW):
            if grid[x][y][2] == 1:
                continue
            elif grid[x][y][1] == True:
                drawrectangle(screen, grid[x][y][0], x, y)
            elif grid[x][y][1] == False:
                drawrectangle(screen, background, x, y)


def drawrectangle(screen, color, mouserow, mousecolumn):
    global margin, boxwidth, boxheight
    pygame.draw.rect(screen, color, [(margin+boxwidth)*mousecolumn+margin, (margin+boxheight)*mouserow+margin, boxwidth, boxheight])


def make_grid(randomNums):
    count = 0
    grid = []
    for row in range(gridH):
        grid.append([])
        for column in range(gridW):
          #[color of the box, show the box color?, has it been clicked yet?]
            if randomNums[count] == 1:
                grid[row].append([green, False, 0])
            elif randomNums[count] == 2:
                grid[row].append([red, False, 0])
            elif randomNums[count] == 3:
                grid[row].append([blue, False, 0])
            elif randomNums[count] == 4:
                grid[row].append([yellow, False, 0])
            elif randomNums[count] == 5:
                grid[row].append([black, False, 0])
            elif randomNums[count] == 6:
                grid[row].append([pink, False, 0])
            elif randomNums[count] == 7:
                grid[row].append([purple, False, 0])
            elif randomNums[count] == 8:
                grid[row].append([darkgreen, False, 0])
            elif randomNums[count] == 9:
                grid[row].append([darkblue, False, 0])
            elif randomNums[count] == 10:
                grid[row].append([darkred, False, 0])


            count += 1
    return grid



def make_color_pairs():
    #MAKING SURE THERE ARE 2 OF EACH COLOR
    #generate (gridH * gridW) / 2 random numbers from 0 to the length of the grid, then make a pair for each one
    randomNums = []
    for row in range((gridH*gridW) / 2):
            randInt = random.randrange(1, num_block_colors+1)
            randomNums.append(randInt)


    randomNums += randomNums
    shuffle(randomNums)
    return randomNums

def get_mouse_position():
    pos = pygame.mouse.get_pos()

    # Change the x/y screen coordinates to grid coordinates
    mousecolumn = int(pos[0] / (boxwidth + margin))
    mouserow = int(pos[1] / (boxheight + margin))
    return mouserow, mousecolumn

def determine_match(grid, firstrow, firstcolumn, currentrow, currentcolumn):

    global timer_string
    #if they are the same, remove them
    if grid[firstrow][firstcolumn] == grid[currentrow][currentcolumn]:
        print ("they are a match")
        grid[firstrow][firstcolumn][2] = 1
        grid[currentrow][currentcolumn][2] = 1

        pygame.draw.rect(screen, black, [(margin+boxwidth)*firstcolumn+margin-2, (margin+boxheight)*firstrow+margin-2, boxwidth+4, boxheight+4], 4)
        pygame.draw.rect(screen, black, [(margin+boxwidth)*currentcolumn+margin-2, (margin+boxheight)*currentrow+margin-2, boxwidth+4, boxheight+4], 4)

        #Draw the grid
        draw_grid()

        screen.blit(text, [gridW* (boxwidth+margin) + margin + 20, 20])
        pygame.display.flip()

        pygame.time.wait(500)
        #grid[firstrow][firstcolumn][0] = background
        #grid[currentrow][currentcolumn][0] = background

    #or else replace the white cover
    elif (grid[firstrow][firstcolumn] != grid[currentrow][currentcolumn]):

        #if grid[firstrow][firstcolumn][2] == 0 and grid[currentrow][currentcolumn][2] == 0:
        pygame.draw.rect(screen, black, [(margin+boxwidth)*firstcolumn+margin-2, (margin+boxheight)*firstrow+margin-2, boxwidth+4, boxheight+4], 4)
        pygame.draw.rect(screen, black, [(margin+boxwidth)*currentcolumn+margin-2, (margin+boxheight)*currentrow+margin-2, boxwidth+4, boxheight+4], 4)
        #Draw the grid
        draw_grid()

        screen.blit(text, [gridW* (boxwidth+margin) + margin + 20, 20])
        pygame.display.flip()

        pygame.time.wait(500)
        grid[firstrow][firstcolumn][1] = False
        grid[currentrow][currentcolumn][1] = False


randomNums = make_color_pairs()
grid = make_grid(randomNums)




# Initialize pygame
pygame.init()


size = [gridW* (boxwidth+margin) + margin + 500, gridH* (boxwidth+margin) + margin + 300]
screen = pygame.display.set_mode(size)

# Set title of screen
pygame.display.set_caption("Memory Game - Matt Carr")

# Used to manage how fast the screen updates
clock = pygame.time.Clock()




frame_count = 0

reset = False
done = False
while done == False: #main loop-------------------------------------------------


# --- Timer going up ---
    # Calculate total seconds
    total_seconds = frame_count // FPS

    # Divide by 60 to get total minutes
    minutes = total_seconds // 60

    # Use modulus (remainder) to get seconds
    seconds = total_seconds % 60

    # Use python string formatting to format in leading zeros
    timer_string = "Time: {0:02}:{1:02}".format(minutes, seconds)

    font = pygame.font.Font(None, 24)
    text = font.render(timer_string, 1, (255, 255, 255))

    # Set the screen background
    #screen.fill(background)
    screen.blit(wallpaper, [0,0])

    for event in pygame.event.get(): # User did something
        if event.type == pygame.QUIT: # If user clicked close
            done = True # Flag that we are done so we exit this loop

        elif event.type == pygame.MOUSEBUTTONDOWN:    # User clicks the mouse. Get the position
            mouserow, mousecolumn = get_mouse_position()


            #if the mouse is over the grid
            if (mouserow <= gridW-1 and mousecolumn <= gridH-1):
                if grid[mouserow][mousecolumn][2] == 0: #if it has not been erased already
                    grid[mouserow][mousecolumn][1] = True #make it visible



                #determining if they have picked twice
                if firstpick == True and secondpick == False:
                    if grid[mouserow][mousecolumn][2] == 0:
                        firstrow = mouserow      #record position of first click
                        firstcolumn = mousecolumn
                        firstpick = False        #change picks
                        secondpick = True
                        reset = False
                        draw_grid()
                        screen.blit(text, [gridW* (boxwidth+margin) + margin + 20, 0])
                        pygame.display.flip()


                elif firstpick == False and secondpick == True:
                    if firstrow != mouserow or firstcolumn != mousecolumn:
                        if grid[mouserow][mousecolumn][2] == 0:
                            currentrow = mouserow
                            currentcolumn = mousecolumn
                            secondpick = False
                            firstpick = True
                            reset = True
                            draw_grid()
                            screen.blit(text, [gridW* (boxwidth+margin) + margin + 20, 0])
                            pygame.display.flip()


                        #if they have two choices, see if they match
                        determine_match(grid, firstrow, firstcolumn, currentrow, currentcolumn)

            # debugging
            #print ("firstpick ", firstpick, " secondpick ", secondpick, " firstrow ",
             #                                       firstrow, " firstcolumn ", firstcolumn, " currentrow ", currentrow, " currentcolumn ", currentcolumn, '\n')


#draw all updated values on buffer--------------------------------------------


    if reset == True:
        firstrow = -1
        firstcolumn = -1
        currentrow = -1
        currentcolumn = -1

    if firstpick != -1 and grid[firstrow][firstcolumn][2] == 0 and grid[currentrow][currentcolumn][2] == 0:
        if firstpick == True and secondpick == False and reset == False:
            pygame.draw.rect(screen, black, [(margin+boxwidth)*firstcolumn+margin-2, (margin+boxheight)*firstrow+margin-2, boxwidth+4, boxheight+4], 4)
        elif firstpick == False and secondpick == True:
            pygame.draw.rect(screen, black, [(margin+boxwidth)*firstcolumn+margin-2, (margin+boxheight)*firstrow+margin-2, boxwidth+4, boxheight+4], 4)

    draw_grid()

    frame_count += 1

    # Limit to 60 frames per second
    clock.tick(FPS)

    # Go ahead and update the screen with what we've drawn.
    screen.blit(text, [gridW* (boxwidth+margin) + margin + 20, 20])
    pygame.display.flip()





pygame.quit()
sys.exit()


