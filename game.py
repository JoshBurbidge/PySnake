# Joshua Burbidge
# a snake game made with Pygame

import pygame
import pygame.freetype
from collections import deque
from math import floor
from random import randrange

'''
TODO:
add margin to top and adjust
reset message
BUG: snake collides with previous location of tail tile
'''

TS = 20
MARGIN = 4
GRIDSIZE = TS + MARGIN
TOP_BANNER = 50
HEIGHT = 360 + TOP_BANNER
WIDTH = 360
GRIDHEIGHT = floor((HEIGHT - TOP_BANNER) / (TS + MARGIN))
GRIDWIDTH = floor(WIDTH / (TS + MARGIN))
INIT_LEN = 5
FPS = 3

WHITE = (255,255,255)
BLACK = (0, 0, 0)

class Tile():
    def __init__(self, xLoc, yLoc):
        self.x = xLoc
        self.y = yLoc

def initialize():
    global screen, blueTile, redTile, greenTile, font, goal, score, tileQ
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("game")
    blueTile = pygame.transform.scale(pygame.image.load("images/blue-tile.png"), (20,20))
    redTile = pygame.transform.scale(pygame.image.load("images/red-tile.png"), (20,20))
    greenTile = pygame.transform.scale(pygame.image.load("images/green-tile.png"), (20,20))
    pygame.freetype.init()
    font = pygame.freetype.SysFont(pygame.freetype.get_default_font(), 30)
    score = 0
    tileQ = deque()
    goal = Tile(-1,-1)
    init_tiles()
    

# initialize tile queue
def init_tiles():
    for i in range(INIT_LEN):
        tileQ.append(Tile(INIT_LEN-i, 8))
    new_goal()


def reset_game():
    tileQ.clear()
    init_tiles()
    global score
    score = 0

# create new goal tile, can't be same location as the old goal tile
# or a location occupied by the snake
def new_goal():
    global goal, goal
    newX = randrange(GRIDWIDTH)
    newY = randrange(GRIDHEIGHT)
    while (newX == goal.x and newY == goal.y) or isInSnake(newX, newY):
        newX = randrange(GRIDWIDTH)
        newY = randrange(GRIDHEIGHT)
    goal = Tile(newX, newY)


def isInSnake(xLoc, yLoc):
    for t in tileQ:
        if xLoc == t.x and yLoc == t.y:
            return True
    return False


# check if a move is valid in a direction
def canMove(dx, dy):
    headX = tileQ[0].x
    headY = tileQ[0].y
    nextX = headX + dx
    nextY = headY + dy
    outOfBounds = nextX < 0 or nextX >= GRIDWIDTH or nextY < 0 or nextY >= GRIDHEIGHT
    selfCollide = isInSnake(nextX, nextY)
    return not outOfBounds and not selfCollide

# moves the snake by one position in a given direction
def move_snake(dx, dy):
    if dx != 0 or dy != 0:
        headX = tileQ[0].x # repeated code
        headY = tileQ[0].y
        nextX = headX + dx
        nextY = headY + dy
        tileQ.appendleft(Tile(nextX, nextY))
        if goal.x != nextX or goal.y != nextY:
            tileQ.pop()
        else:
            global score
            score += 1
            new_goal()


def draw_window():
    screen.fill(BLACK)
    # create the grid drawing by drawing white squares
    x, y = 0, TOP_BANNER
    while y < HEIGHT - TS:
        while x < WIDTH - TS:
            pygame.draw.rect(screen, WHITE, pygame.Rect(x,y,TS,TS))
            x += TS + MARGIN
        x = 0
        y += TS + MARGIN

    screen.blit(greenTile, (goal.x*GRIDSIZE, TOP_BANNER+goal.y*GRIDSIZE))

    for t in tileQ:
        screen.blit(blueTile, (t.x * GRIDSIZE, TOP_BANNER+ t.y*GRIDSIZE))
    screen.blit(redTile, (tileQ[0].x * GRIDSIZE, TOP_BANNER+ tileQ[0].y*GRIDSIZE))
    
    font.render_to(screen, (10, 10), f'score: {score}' , WHITE)

    pygame.display.update()


def main():
    initialize()
    clock = pygame.time.Clock()

    dx = 1
    dy = 0

    run = True
    while run:
        clock.tick(FPS)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            # set direction of snake (can't do 180 degree turn)
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    run = False
                elif event.key == pygame.K_LEFT and dx == 0:
                    dx = -1
                    dy = 0
                    #break # break prevents 2 direction changes in same frame
                elif event.key == pygame.K_RIGHT and dx == 0:
                    dx = 1
                    dy = 0
                    #break
                elif event.key == pygame.K_UP and dy == 0:
                    dy = -1
                    dx = 0
                    #break
                elif event.key == pygame.K_DOWN and dy == 0:
                    dy = 1
                    dx = 0
                    #break
        if canMove(dx, dy):
            move_snake(dx, dy)
        else: # give message
            #run = False # quit back to menu
            reset_game()
            dx = 1
            dy = 0 # change
        draw_window()
    
    pygame.quit()

if __name__ == "__main__":
    main()