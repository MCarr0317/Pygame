#-------------------------------------------------------------------------------
# Name:        Breakout Game
# Purpose:
#
# Author:      Matt Carr
#
# Created:     03/01/2014
# Copyright:   (c) Matt Carr 2014
# Licence:     <your licence>
#-------------------------------------------------------------------------------
import pygame, os, sys, math, time
import ButtonClass, SmokeClass, PaddleClass, BallClass, config
import grid_designer
from config import *

#----Constants are imported from config file------------------------------------

""" The Game class is responsible for creating all aspects of the game, namely being the ball, paddle, and blocks.
        It performs all computation for collisions and score.
"""
class Game():

    """ PRE: none
        POST: pygame is initialized, screen caption is set to "Breakout", paddle, ball, and score label are created
        DESCR: the constructor for the Game class, creates and instance of Game class
    """
    def __init__(self):
        pygame.init()                                                                       #initialize pygame
        pygame.mixer.init()                                                                 #initialize the pygame mixer for sounds
        pygame.mouse.set_visible(1)                                                         #make the mouse visible
        pygame.display.set_caption("Breakout")                                              #set the caption of the window

        self.paddle = PaddleClass.Paddle(PADDLE_DIMENSIONS)                                             # creates a Paddle object
        self.ball = BallClass.Ball(BALL_DIMENSIONS)                                                   # creates a Ball object

        self.score = pygame.font.Font('C:\Windows\Fonts\Sugabb__.ttf', 24)                  #creates the font for the score label
        self.score_string = score_string                                                      #sets the caption
        self.score_count = 0                                                                #sets the initial score
        self.text = self.score.render(self.score_string + str(self.score_count), 1, WHITE)  #renders the text

        self.smoke = SmokeClass.Smoke(BALL_DIMENSIONS, self.ball.ball_direction)

        self.new_game = ButtonClass.Button(startgame_string, (250, 250), 24)                             # creates the button for new game
        self.grid_designer = ButtonClass.Button(griddesigner_string, (250, 300), 24)                 # creates the button for the grid designer
        self.title = ButtonClass.Button("BREAKOUT", (0, 0), 200)


        #SOUNDS-----------------------------------------------------------------
        self.hit_sound = pygame.mixer.Sound("boop.wav")
        self.music = pygame.mixer.Sound("BreakoutMusic.wav")

        # Variables-------------------------------------------------------------
        self.point_list = []                       # holds the list of points in the grid
        """
        #opens grid design file
        f = open('Lungs.txt', 'r')
        while f.tell() != os.fstat(f.fileno()).st_size:
            self.point_list.append (list(eval(f.readline())))
        f.close()

        #creates a rectangle object for each block
        self.rect_list = []
        for i in xrange(len(self.point_list)):
            rect = pygame.Rect((MARGIN+BOX_WIDTH) * self.point_list[i][0] + MARGIN, (MARGIN+BOX_HEIGHT) * self.point_list[i][1], BOX_WIDTH, BOX_HEIGHT)
            self.rect_list.append(rect)
        """


    def load_grid(self, grid_file):

        #opens grid design file
        f = open(config.grid_file, 'r')
        while f.tell() != os.fstat(f.fileno()).st_size:
            self.point_list.append (list(eval(f.readline())))
        f.close()

        #creates a rectangle object for each block
        self.rect_list = []
        for i in xrange(len(self.point_list)):
            rect = pygame.Rect((MARGIN+BOX_WIDTH) * self.point_list[i][0] + MARGIN, (MARGIN+BOX_HEIGHT) * self.point_list[i][1], BOX_WIDTH, BOX_HEIGHT)
            self.rect_list.append(rect)


    """ PRE: point_list must include at least one coordinate
        POST: all coordinates in point_list are drawn to the screen with dimensions specified at top of code
        DESCR: draws the shape that the blocks are in to the screen
    """
    def draw_shape(self, point_list):
            for i in xrange(len(point_list)):
                screen.blit(block, [(MARGIN+BOX_WIDTH) * point_list[i][0] + MARGIN, (MARGIN+BOX_HEIGHT) * point_list[i][1]])
                #pygame.draw.rect(screen, RED, [(MARGIN+BOX_WIDTH) * point_list[i][0] + MARGIN, (MARGIN+BOX_HEIGHT) * point_list[i][1], BOX_WIDTH, BOX_HEIGHT])

    """ PRE: None
        POST: The score label is blitted to the screen
        DESCR: Draws the label on the screen
    """
    def update_score(self):
        screen.blit(self.text, (0, 0))


    """ PRE: point_list and rect_list must include atleast one coordinate
        POST: direction of the ball is changed upon collision, point_list and rect_list have that element popped if so.
        DESCR: determines if the ball has collided with a block, paddle, or the edges of the screen and changes the direction of the ball accordingly
    """
    def collision(self):
        global speedBoost
        #if the ball hits the sides of the play area
        if self.ball.ball.right >= WIDTH or self.ball.ball.left <= 0:
            self.ball.ball_direction = -(self.ball.ball_direction[0]), self.ball.ball_direction[1]
            self.hit_sound.play()

        # if the ball hits the top of the play area
        elif self.ball.ball.top <= 0:
            self.ball.ball_direction = self.ball.ball_direction[0], -self.ball.ball_direction[1]
            self.hit_sound.play()

        # if you dont catch the ball
        elif self.ball.ball.bottom >= HEIGHT and self.ball.ball.colliderect(self.paddle.paddle) == False:
            self.ball.ball_direction = self.ball.ball_direction[0], -self.ball.ball_direction[1]
            self.balls -= 1
            self.ball = BallClass.Ball(BALL_DIMENSIONS)
            self.smoke = SmokeClass.Smoke(BALL_DIMENSIONS, self.ball.ball_direction)

        #if the ball hits the paddle
        elif self.ball.ball.colliderect(self.paddle.paddle):
            self.hit_sound.play()
            dist = self.ball.ball.midbottom[0] - self.paddle.paddle.midtop[0]
            if dist >= 10: #means the ball hit on the right side of thepaddle
                self.ball.ball_direction = (-math.sin(dist)/2)*self.ball.ball_direction[0]+ 2.5, -self.ball.ball_direction[1]
                #self.ball.ball_direction = self.ball.ball_direction[0], -self.ball.ball_direction[1]

            elif dist <= -10: #means the ball hit on the left
                self.ball.ball_direction = (math.sin(dist)/2)*self.ball.ball_direction[0]- 2.5, -self.ball.ball_direction[1]
                #self.ball.ball_direction = self.ball.ball_direction[0], -self.ball.ball_direction[1]
            else:
                self.ball.ball_direction = self.ball.ball_direction[0], -self.ball.ball_direction[1]



        # if the ball hit a block
        elif self.ball.ball.collidelist(self.rect_list) != -1:
            global FPS
            FPS += 0.25
            self.hit_sound.play()
            index = (self.ball.ball.collidelist(self.rect_list)) #returns the list index of which block we hit

            #moving diagonally up-right
            if self.ball.ball_direction[0] >= 0 and self.ball.ball_direction[1] <= 0:
                diff1 = abs(self.ball.ball.topright[0] - self.rect_list[index].bottomleft[0])
                diff2 = abs(self.ball.ball.topright[1] - self.rect_list[index].bottomleft[1])

            #moving diagonally up-left
            elif self.ball.ball_direction[0] <= 0 and self.ball.ball_direction[1] <= 0:
                diff1 = abs(self.ball.ball.topleft[0] - self.rect_list[index].bottomright[0])
                diff2 = abs(self.ball.ball.topleft[1] - self.rect_list[index].bottomright[1])

            #moving diagonally down-right
            elif self.ball.ball_direction[0] >= 0 and self.ball.ball_direction[1] >= 0:
                diff1 = abs(self.ball.ball.bottomright[0] - self.rect_list[index].topleft[0])
                diff2 = abs(self.ball.ball.bottomright[1] - self.rect_list[index].topleft[1])

            #moving diagonally down-left
            elif self.ball.ball_direction[0] <= 0 and self.ball.ball_direction[1] >= 0:
                diff1 = abs(self.ball.ball.bottomleft[0] - self.rect_list[index].topright[0])
                diff2 = abs(self.ball.ball.bottomleft[1] - self.rect_list[index].topright[1])

            #determine the new direction
            if diff1 > diff2:
                self.ball.ball_direction = self.ball.ball_direction[0], -self.ball.ball_direction[1]
            elif diff1 < diff2:
                self.ball.ball_direction = -self.ball.ball_direction[0], self.ball.ball_direction[1]
            elif diff1 == diff2:
                self.ball.ball_direction = -self.ball.ball_direction[0], -self.ball.ball_direction[1]






            #remove the block that we hit
            self.point_list.pop(index)
            self.rect_list.pop(index)


            #choose the next level
            if len(self.point_list) == 0:
                time.sleep(0.5)
                config.index += 1
                if config.index <= 2:
                    config.grid_file = config.LevelList[config.index]
                    print config.index, config.LevelList[config.index]
                    self.ball = BallClass.Ball(BALL_DIMENSIONS)
                    self.load_grid(config.grid_file)
                else:
                    print "You win!"
                    pygame.quit()
                    sys.exit()


            #update score
            self.score_count += 1
            self.text = self.score.render(self.score_string + str(self.score_count), 1, WHITE)



    """ PRE: None
        POST: All objects and sprites are drawn to the screen, pygame events are controlled here
        DESCR: Main game loop
    """
    def run(self):
        global PADDLE_DIMENSIONS

        clock = pygame.time.Clock()
        self.balls = 100
        start = False
        self.load_grid(grid_file)

        while self.balls > 0:

            # Process events
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                keys = pygame.key.get_pressed()
                if keys[pygame.K_RETURN]:
                    start = not start
                if event.type == pygame.MOUSEMOTION:
                    PADDLE_DIMENSIONS = pygame.mouse.get_pos()[0] - CIG_WIDTH/2, PADDLE_DIMENSIONS[1], PADDLE_DIMENSIONS[2], PADDLE_DIMENSIONS[3]
                    self.paddle = PaddleClass.Paddle(PADDLE_DIMENSIONS)
                else:
                    self.paddle.change_movement(0)


                if start == False: #if we arent currently in game, display the menu
                    screen.fill(RED)
                    self.title.draw_button()    #title
                    self.new_game.draw_button() #start game button
                    self.grid_designer.draw_button()    #grid designer button
                    pygame.mouse.set_visible(1)


                pygame.display.update()

                if event.type == pygame.MOUSEBUTTONDOWN:
                    mouse = pygame.mouse.get_pos()
                    if self.new_game.pressed(mouse):
                        start = True
                    elif self.grid_designer.pressed(mouse):
                        self.point_list = []
                        self.rect_list = []
                        grid_designer.main(screen)
                        screen.fill(BLACK)
                        self.load_grid(file)
                        #Game().run()


            if start == True:
                pygame.mouse.set_visible(0)

                for event in pygame.event.get():
                    #if event.type == pygame.MOUSEMOTION:
                     #   pygame.mouse.set_pos((self.paddle.paddle.midleft[0], self.paddle.paddle.midtop[1]))

                    keys = pygame.key.get_pressed()
                    if keys[pygame.K_RETURN]:
                        start = False

                #move the paddle and the ball
                self.paddle.move_paddle()
                self.ball.move_ball()
                pygame.mouse.set_pos((self.paddle.paddle.left+(CIG_WIDTH/2), self.paddle.paddle.top))
                #check for collisions
                self.collision()
                BALL_DIMENSIONS = self.ball.ball.left, self.ball.ball.top, 15, 15

                #create new smoke object
                self.smoke = SmokeClass.Smoke(BALL_DIMENSIONS, self.ball.ball_direction)
                self.smoke.move_smoke(self.ball.ball_direction)     #move smoke

                #draw everything to the screen
                screen.fill(BLACK)
                self.paddle.draw_paddle()   #draw paddle
                self.draw_shape(self.point_list)    #draw grid
                self.update_score() #draw score label
                #self.smoke.draw_smoke() #draw smoke
                screen.blit(ball, BALL_DIMENSIONS)  #draw ball icon
                #self.ball.draw_ball()   #draw ball


                pygame.display.update()
                clock.tick(FPS)



        pygame.quit()
        sys.exit()


#Game().music.play(-1)
Game().run()
