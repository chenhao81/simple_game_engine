# coding: UTF-8

import json
import sys
import pygame
import random
from pygame.locals import *

FPS = 20
UPDATE_TICK = 10
# global variables
WINDOWWIDTH = 840
WINDOWHEIGHT = 680
CELLSIZE = 10
assert WINDOWWIDTH % CELLSIZE == 0, "Window width must be a multiple of cell size"
assert WINDOWHEIGHT % CELLSIZE == 0, "Window height must be a multiple of cell size"
# ensure fill all window
CELLWIDTH = WINDOWWIDTH / CELLSIZE  # x count
CELLHEIGHT = WINDOWHEIGHT / CELLSIZE  # y count
# colours
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GRAY = (30, 30, 30)
GREEN = (0, 255, 0)


# setp1  Creating a blank pygame screen.
def main():
    pygame.init()
    global screen
    FPSCLOCK = pygame.time.Clock()
    screen = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT))
    pygame.display.set_caption('Game of Life')
    screen.fill(WHITE)
    # draw our grid
    draw_grid()
    lifeDict = blank_grid()  # this is dic for data
    # we can modify data , assign random life
    lifeDict = startingGridRandom(lifeDict)
    pause = True
    mouse_down = False
    tick_count = 0

    # color
    for item in lifeDict:
        x = item[0]
        y = item[1]
        colourGrid(item, lifeDict)

    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                pressed = pygame.key.get_pressed()
                if pressed[K_p]:
                    pause = not pause
                    if pause:
                        print 'Pause Game.'
                    else:
                        print 'Resume Game.'

                if pressed[K_c]:
                    clearGrid(lifeDict)
                if pressed[K_s]:
                    saveGrid(lifeDict)
                if pressed[K_l]:
                    lifeDict = loadGrid()

            # 处理鼠标点击
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_down = True

            if event.type == pygame.MOUSEBUTTONUP:
                mouse_down = False

            if mouse_down:
                mouse_pos = pygame.mouse.get_pos()
                mx = mouse_pos[0]
                my = mouse_pos[1]
                x = mx / CELLSIZE
                y = my / CELLSIZE
                print("x:%s y:%s"%(x,y))
                birthGrid(x,y,lifeDict)

        if not pause:
            tick_count += 1
            if tick_count > UPDATE_TICK:
                tick_count = 0
                lifeDict = tick(lifeDict)

        for item in lifeDict:
            colourGrid(item, lifeDict)

        # update all time
        draw_grid()
        pygame.display.update()
        FPSCLOCK.tick(FPS)


# setp2  Creating a blank grid on the pygame screen.
def draw_grid():
    # for x in range(0,WINDOWWIDTH, CELLSIZE)
    for x in range(0, WINDOWWIDTH, CELLSIZE):
        pygame.draw.line(screen, GRAY, (x, 0), (x, WINDOWHEIGHT))
    for y in range(0, WINDOWHEIGHT, CELLSIZE):
        pygame.draw.line(screen, GRAY, (0, y), (WINDOWWIDTH, y))
    pygame.display.update()


# setp3  Creating random coloured cells on the screen.
def blank_grid():
    gridDict = {}
    # all cell set 0
    for y in range(CELLHEIGHT):
        for x in range(CELLWIDTH):
            gridDict[x, y] = 0

    return gridDict


def clearGrid(lifeDict):
    # all cell set 0
    for y in range(CELLHEIGHT):
        for x in range(CELLWIDTH):
            lifeDict[x, y] = 0



# random modify cells
def startingGridRandom(lifeDict):
    '''
    ex: lifeDict[(3,3)] = (0 | 1) (live or dead)
    '''
    for item in lifeDict:  # item = (x,y)
        lifeDict[item] = random.randint(0, 1)
    return lifeDict


def saveGrid(lifeDict):
    lines = []
    for item in lifeDict:  # item = (x,y)
        lines += ["%s:%s\n"%(json.dumps(item),lifeDict[item])]
    with open('save', 'wt') as fp:
        fp.writelines(lines)
        print 'Saved.'


def loadGrid():
    lifeDict = {}
    with open('save','rt') as fp:
        content = fp.readlines()
    for js in content:
        pair = js[:-1].split(':')
        lifeDict[tuple(json.loads(pair[0]))] = int(pair[1])

    return lifeDict

def birthGrid(x, y, lifeDict):
    if x >= 0 and x < CELLWIDTH and y >= 0 and y < CELLHEIGHT:
        lifeDict[x, y] = 1


def colourGrid(item, lifeDict):
    x = item[0]
    y = item[1]
    x = x * CELLSIZE
    y = y * CELLSIZE
    if lifeDict[item] == 0:
        pygame.draw.rect(screen, WHITE, (x, y, CELLSIZE, CELLSIZE))
    if lifeDict[item] == 1:
        pygame.draw.rect(screen, GREEN, (x, y, CELLSIZE, CELLSIZE))
    return None


# setp4  Working Game of Life.
def get_neighbours(item, lifeDict):
    neighbours = 0
    # surround cell
    for x in range(-1, 2):
        for y in range(-1, 2):
            checkCell = (item[0] + x, item[1] + y)
            if checkCell[0] < CELLWIDTH and checkCell[0] >= 0:
                if checkCell[1] < CELLHEIGHT and checkCell[1] >= 0:
                    if lifeDict[checkCell] == 1:
                        if x == 0 and y == 0:
                            neighbours += 0  # self
                        else:
                            neighbours += 1

    return neighbours


def tick(lifeDict):
    newTick = {}
    for item in lifeDict:
        numberNeighbours = get_neighbours(item, lifeDict)
        if lifeDict[item] == 1:
            # live
            if numberNeighbours < 2:
                newTick[item] = 0
            elif numberNeighbours > 3:
                newTick[item] = 0
            else:
                newTick[item] = 1
        elif lifeDict[item] == 0:
            if numberNeighbours == 3:
                newTick[item] = 1
            else:
                newTick[item] = 0
    return newTick


if __name__ == '__main__':
    main()
