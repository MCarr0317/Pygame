__author__ = 'Matthew Carr'


import pygame
import copy
import sys
import time
import random
from pygame.locals import *


# Define some colors
black     = (   0,   0,   0)
white     = ( 255, 255, 255)
grey      = ( 127, 127, 127)
green     = (   0, 200,   0)
red       = ( 255,   0,   0)
blue      = (   0,   0, 255)
yellow    = ( 255, 255,   0)
pink      = ( 255,  51, 255)
purple    = (  51,   0, 102)
darkgreen = (   0, 102,   0)
darkblue  = ( 153, 153, 255)
darkred   = (  102,  0, 100)


class Game():
    def __init__(self):
        self.grid = [
                    [0, 0, 0, 0],
                    [0, 0, 0, 0],
                    [0, 0, 0, 0],
                    [0, 0, 0, 0]
                    ]

        self.Game_background = pygame.image.load("template.jpg").convert()
        self.position_list = []
        self.tile_list = []

        self.score = 0

        self.all_cells = [[x, y] for x in range(len(self.grid)) for y in range(len(self.grid[x]))]

    def __repr__(self):  # debugging
        grid_str = '-'*21*4+'\n'
        for row in Game.grid:
            grid_str += '||'
            for spot in row:
                grid_str += str(spot).center(20)
            grid_str += "||\n"

        return grid_str + '-'*21*4+'\n'

    def create_tile(self, value=2, start_position=[-1, -1]):
        if start_position == [-1, -1]:
            open_positions = self.diff(self.all_cells, self.position_list)
            start_position = open_positions[random.randrange(len(open_positions))]
        new_tile = Tile(value, start_position)
        self.grid[start_position[0]][start_position[1]] = new_tile

        self.create_tile_animation(new_tile)
        return new_tile

    @staticmethod
    def create_tile_animation(new_tile):
        clock_animation = pygame.time.Clock()
        coordinates = copy.copy(new_tile.coord)
        coordinates = [coordinates[0]-7, coordinates[1]-7]
        dimensions = [123, 123]
        x_change = 6
        y_change = 6
        while dimensions[0] > 105:
            rect = pygame.Rect(coordinates[0], coordinates[1], dimensions[0], dimensions[1])
            pygame.draw.rect(screen, (255, 255, 255), rect, 0)
            screen.blit(new_tile.number, (new_tile.coord[0] + (0.5*new_tile.height)-5, new_tile.coord[1] + (0.5*new_tile.width)-15))
            pygame.display.update(rect)
            coordinates = [coordinates[0]+x_change/2, coordinates[1]+y_change/2]
            dimensions = [dimensions[0]-x_change, dimensions[1]-y_change]
            clock_animation.tick(25)

    def update_score_label(self):
        self.score_font = pygame.font.Font('C:\Windows\Fonts\Sugabb__.ttf', 30)
        self.score_label = self.score_font.render(str(self.score), 1, white)

        screen.blit(self.score_label, (x+50, 0))

    def get_tile(self, x, direction):
        if direction == 'up':
            if x.pos[0]-1 >= 0:
                return self.grid[x.pos[0]-1][x.pos[1]]
            else:
                return 0
        elif direction == 'down':
            if x.pos[0]+1 <= len(Game.grid[0])-1:
                return self.grid[x.pos[0]+1][x.pos[1]]
            else:
                return 0
        elif direction == 'right':
            if x.pos[1]+1 <= len(Game.grid[0])-1:
                return self.grid[x.pos[0]][x.pos[1]+1]
            else:
                return 0
        elif direction == 'left':
            if x.pos[1]-1 >= 0:
                return self.grid[x.pos[0]][x.pos[1]-1]
            else:
                return 0

    @staticmethod
    def diff(a, b):
        return [n for n in a if n not in b]

    def determine_game_over(self):
        global game_over
        if '2048' in [m.value for n in Game.grid for m in n if m != 0]:
            game_over = True

        if not self.diff(self.all_cells, self.position_list):
            game_over = True
            for i in range(len(self.grid)-1):
                for n in range(len(self.grid[i])-1):
                    if self.grid[i][n] != 0 and self.grid[i][n+1] != 0 and self.grid[i+1][n] != 0:
                        if self.grid[i][n].value == self.grid[i][n+1].value or self.grid[i][n].value == self.grid[i+1][n].value:
                            game_over = False


class Tile():
    def __init__(self, value=2, pos=[2, 2]):
        self.value = str(value)
        self.pos = pos
        Game.position_list.append(pos)
        Game.tile_list.append(self)
        self.height = 105  # height of the tile
        self.width = 105  # width of the tile
        self.label = pygame.font.Font('C:\Windows\Fonts\Sugabb__.ttf', 60)
        self.coord = [self.pos[1] * 15 + self.pos[1]*105 + 15, self.pos[0] * 15 + self.pos[0]*105 + 15]
        self.rect = pygame.Rect(self.coord[0], self.coord[1], self.height, self.width)
        self.number = self.label.render(self.value, 1, black)

    def __repr__(self):
        return '{}: {} {}'.format(self.__class__.__name__,
                                  self.value,
                                  self.pos)

    def draw_tile(self):
        self.coord = [self.pos[1] * 15 + self.pos[1]*105 + 15, self.pos[0] * 15 + self.pos[0]*105 + 15]
        self.rect = pygame.Rect(self.coord[0], self.coord[1], self.height, self.width)

        #Game.dirty_rects.append(self.rect)  # append our new tile to our dirty rects list

        self.number = self.label.render(self.value, 1, black)
        tile_colors = {'2': 255, '4': 50, '8': 100, '16': 150, '32': 200, '64': 255, '128': 50, '256': 100, '512': 150,
                       '1024': 200, '2048': 255}


        s = pygame.Surface((self.width, self.height))
        s.set_alpha(tile_colors[self.value])
        if int(self.value) <= 2:
            s.fill(white)
        elif int(self.value) <= 64:
            s.fill(red)
        elif int(self.value) <= 2048:
            s.fill(yellow)
        screen.blit(s, (self.coord[0], self.coord[1]))

        # centers the number on each tile if it gets bigger
        if int(self.value) < 10:
            screen.blit(self.number, (self.coord[0] + (0.5*self.height)-15, self.coord[1] + (0.5*self.width)-30))
        elif int(self.value) < 100:
            screen.blit(self.number, (self.coord[0] + (0.5*self.height)-25, self.coord[1] + (0.5*self.width)-30))
        elif int(self.value) < 1000:
            screen.blit(self.number, (self.coord[0] + (0.5*self.height)-35, self.coord[1] + (0.5*self.width)-30))
        elif int(self.value) < 10000:
            screen.blit(self.number, (self.coord[0] + (0.5*self.height)-45, self.coord[1] + (0.5*self.width)-30))

    def move(self, key_input):
        global spawn_new_tile
        # moves the tile until there are no more empty spots in its direction of movement
        while Game.get_tile(self, key_input) == 0 and (self.pos[0] if key_input == 'up' else (self.pos[0] < len(Game.grid[0])-1 if key_input == 'down' else (self.pos[1] if key_input == 'left' else self.pos[1] < len(Game.grid[0])-1))):
            spawn_new_tile = True
            [Game.grid[self.pos[0]+x_direction][self.pos[1]+y_direction], Game.grid[self.pos[0]][self.pos[1]]] = [self, 0]  # make the space above the new tile
            Game.tile_list.remove(self)  # remove the current tile pos from the tile_list
            Game.position_list.remove(self.pos)  # remove the current pos from position_list
            self.pos = [self.pos[0]+x_direction, self.pos[1]+y_direction]  # change the tile position to the new tile
            Game.tile_list.append(self)
            Game.position_list.append(self.pos)

    def combine(self, key_input):
        global combined, spawn_new_tile

        # checks if the reason that it stopped was because it hit a tile, if so, combine them
        if Game.get_tile(self, key_input) != 0 and self.value == Game.get_tile(self, key_input).value:
            combined = True
            spawn_new_tile = True
            #print tile, "has hit ", Game.grid[self.pos[0]+x_direction][self.pos[1]+y_direction], "and combined into ",
            Game.grid[self.pos[0]+x_direction][self.pos[1]+y_direction].value = str(int(self.value) * 2)
            Game.score += int(self.value) * 2
            #print Game.get_tile(self, key_input), "\n\n"
            Game.grid[self.pos[0]][self.pos[1]] = 0
            Game.tile_list.remove(self)
            Game.position_list.remove(self.pos)





# Initialize pygame
pygame.init()
#x = 497
#y = 497
x = 800
y = 900
size = [x+100+100, y+100]
screen = pygame.display.set_mode(size)
FPS = 20
# Set title of screen
pygame.display.set_caption("2048 - Matt Carr")

#Game instance
Game = Game()
game_over = False
spawn_new_tile = False
# creating initial tiles
Game.create_tile(2)
Game.create_tile(4)

#print Game

while True:
    if game_over:
        print('Game Over\n')
        time.sleep(1)
        pygame.quit()
        sys.exit()

    pygame.Surface.fill(screen, grey)
    screen.blit(Game.Game_background, [0, 0])  # draws the background image
    for each in Game.tile_list:
        each.draw_tile()

    Game.update_score_label()

    for event in pygame.event.get():
        key = pygame.key.get_pressed()
        if event.type == pygame.QUIT:  # If user clicked close
            print ("Game Over")
            pygame.quit()
            sys.exit()

        if key[K_UP] or key[K_DOWN] or key[K_LEFT] or key[K_RIGHT]:
            direction_next_tile = ('up' if key[K_UP] else ('down' if key[K_DOWN] else ('right' if key[K_RIGHT] else 'left')))
            [x_direction, y_direction] = ([-1, 0] if direction_next_tile == 'up' else ([1, 0] if direction_next_tile == 'down' else ([0, -1] if direction_next_tile == 'left' else [0, 1])))

            # Move, combine like tiles, then fill in spaces we made by combining
            for i in range(3):
                for group in (Game.grid if key[K_UP] else (reversed(Game.grid) if key[K_DOWN] else (reversed(Game.grid) if key[K_RIGHT] else Game.grid))):
                    for tile in (group if key[K_UP] else (reversed(group) if key[K_DOWN] else (reversed(group) if key[K_RIGHT] else group))):
                        if tile != 0:
                            if i == 1:
                                tile.combine(direction_next_tile)  # combine the like tiles
                            else:
                                tile.move(direction_next_tile)

            if spawn_new_tile:
                pygame.Surface.fill(screen, grey)
                screen.blit(Game.Game_background, [0, 0])  # draws the background image
                for each in Game.tile_list:
                    each.draw_tile()
                Game.update_score_label()
                pygame.display.flip()
                Game.create_tile()
                spawn_new_tile = not spawn_new_tile
                #print Game
                #print "\tSCORE: ", Game.score

    pygame.display.flip()
    Game.determine_game_over()
