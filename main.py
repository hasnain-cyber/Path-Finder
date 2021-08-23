import queue
import time

import pygame

from constants import *

pygame.init()
surface = pygame.display.set_mode((WIDTH, WIDTH))

start = time.time()
startPosition, endPosition = None, None
obstacles = set()  # set to avoid duplicate coordinates
visitedPaths = set()
mode = 0
positionQueue = queue.Queue()
selectedMouseButton = None


def setMode(modeNumber):
    global mode
    mode = modeNumber
    pygame.display.set_caption(MODE_ARRAY[modeNumber])


def handleMouseButtonDown(mouseMode):
    # mouseMode 1 for paint, 3 for erase
    global startPosition, endPosition, obstacles

    rectX, rectY = getMouseRectPosition(pygame.mouse.get_pos())
    if mouseMode == 1:
        if mode == 1:
            startPosition = (rectX, rectY)
        elif mode == 2:
            endPosition = (rectX, rectY)
        elif mode == 3:
            obstacles.add((rectX, rectY))
    else:
        erasePosition = (rectX, rectY)
        if mode == 1 and startPosition == erasePosition:
            startPosition = None
        elif mode == 2 and endPosition == erasePosition:
            endPosition = None
        elif mode == 3 and erasePosition in obstacles:
            obstacles.remove(erasePosition)
    init()


def handleMouseMove(mouseMode):
    rectX, rectY = getMouseRectPosition(pygame.mouse.get_pos())

    global startPosition, endPosition, obstacles

    if mouseMode == 1:
        if mode == 3:
            obstacles.add((rectX, rectY))
        init()
    else:
        if mode == 1 and (rectX, rectY) == startPosition:
            startPosition = None
        elif mode == 2 and (rectX, rectY) == endPosition:
            endPosition = None
        elif mode == 3 and (rectX, rectY) in obstacles:
            obstacles.remove((rectX, rectY))
        init()


def getMouseRectPosition(mousePosition):
    return int((mousePosition[0] // RECT_WIDTH) * RECT_WIDTH), int((mousePosition[1] // RECT_WIDTH) * RECT_WIDTH)


def getNeighbours(position):
    xArray = [0, 0, 1, -1]
    yArray = [1, -1, 0, 0]

    neighbours = []
    for i in range(4):
        testPosition = (position[0] + xArray[i] * RECT_WIDTH, position[1] + yArray[i] * RECT_WIDTH)
        flag1 = 0 <= testPosition[0] < WIDTH and 0 <= testPosition[1] < WIDTH
        flag2 = testPosition not in obstacles
        flag3 = False if any(
            element[1] == testPosition for element in visitedPaths) else True  # to eliminate visited cells
        if flag1 and flag2 and flag3:
            neighbours.append(testPosition)
    return neighbours


def init():
    setMode(mode)

    surface.fill(WHITE)
    for i in range(ROWS):
        pygame.draw.line(surface, BLACK, (0, i * RECT_WIDTH), (WIDTH, i * RECT_WIDTH))
        pygame.draw.line(surface, BLACK, (i * RECT_WIDTH, 0), (i * RECT_WIDTH, WIDTH))

    if startPosition is not None:
        pygame.draw.rect(surface, RED,
                         [startPosition[0] + 1, startPosition[1] + 1, RECT_WIDTH - 1, RECT_WIDTH - 1])
    if endPosition is not None:
        pygame.draw.rect(surface, BLUE,
                         [endPosition[0] + 1, endPosition[1] + 1, RECT_WIDTH - 1, RECT_WIDTH - 1])
    for element in obstacles:
        pygame.draw.rect(surface, BLACK,
                         [element[0] + 1, element[1] + 1, RECT_WIDTH - 1, RECT_WIDTH - 1])
    pygame.display.update()


# using breadth-first algorithm
def findPath():
    global positionQueue

    while not positionQueue.empty():
        time.sleep(1 / SPEED)
        testPosition = positionQueue.get()
        if testPosition == endPosition:
            reconstructPath()
            return
        neighbours = getNeighbours(testPosition)
        for neighbour in neighbours:
            visitedPaths.add((testPosition, neighbour))
            positionQueue.put(neighbour)
            pygame.draw.rect(surface, GREEN,
                             [neighbour[0] + 1, neighbour[1] + 1, RECT_WIDTH - 1, RECT_WIDTH - 1])
        pygame.display.update()


def reconstructPath():
    init()  # clear the previous colors of processing and plot start, end and obstacle positions

    global visitedPaths, flag
    currentPosition = endPosition
    while currentPosition != startPosition:
        for element in visitedPaths:
            if element[1] == currentPosition:
                currentPosition = element[0]
                break
        pygame.draw.rect(surface, TEAL,
                         [currentPosition[0] + 1, currentPosition[1] + 1, RECT_WIDTH - 1, RECT_WIDTH - 1])
    pygame.draw.rect(surface, RED,
                     [currentPosition[0] + 1, currentPosition[1] + 1, RECT_WIDTH - 1, RECT_WIDTH - 1])
    pygame.display.update()


init()
flag = True
while flag:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            flag = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_1:
                setMode(1)
            elif event.key == pygame.K_2:
                setMode(2)
            elif event.key == pygame.K_3:
                setMode(3)
            elif event.key == pygame.K_SPACE:
                if not (startPosition is None or endPosition is None):
                    positionQueue.put(startPosition)
                    findPath()
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                selectedMouseButton = 1
                handleMouseButtonDown(1)
            elif event.button == 3:
                selectedMouseButton = 3
                handleMouseButtonDown(3)
        elif event.type == pygame.MOUSEMOTION:
            if selectedMouseButton is not None:
                handleMouseMove(selectedMouseButton)
        elif event.type == pygame.MOUSEBUTTONUP:
            selectedMouseButton = None
            init()

print('time taken: ', time.time() - start)
