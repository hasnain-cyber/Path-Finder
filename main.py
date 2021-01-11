import sys

import pygame

from constants import *

pygame.init()
surface = pygame.display.set_mode((WIDTH, WIDTH))
pygame.display.set_caption("NO MODE SET")
start_pos = None
end_pos = None
obstacles = set()
start_flag = False
end_flag = False
obstacle_flag = False


def set_stage():
    surface.fill(WHITE)
    for i in range(ROWS):
        pygame.draw.line(surface, BLACK, (0, i * rect_width), (WIDTH, i * rect_width))
        pygame.draw.line(surface, BLACK, (i * rect_width, 0), (i * rect_width, WIDTH))
    pygame.display.update()


def get_tile(mouse):
    x = (mouse[0] // rect_width) * rect_width
    y = (mouse[1] // rect_width) * rect_width
    return int(x), int(y)


def get_neighbours(home_position):
    neighbours = set()
    for i in range(2):
        for j in range(2):
            x = home_position[0] + i * rect_width
            y = home_position[1] + j * rect_width
            if (not (0 <= x <= WIDTH - rect_width and 0 <= y <= WIDTH - rect_width)) or (x, y) in obstacles:
                continue
            else:
                neighbours.add((x, y))
    return neighbours


def get_distance(current_pos):
    return abs(current_pos[0] - end_pos[0]) + abs(current_pos[1] - end_pos[1])


def solve():
    pass  # have to complete the algorithm


set_stage()
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit(0)
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_1:
                if not start_flag:
                    pygame.display.set_caption('SET START POSITION')
                    start_flag = True
                    end_flag = False
                    obstacle_flag = False
                else:
                    pygame.display.set_caption("NO MODE SET")
                    start_flag = False
            elif event.key == pygame.K_3:
                if not end_flag:
                    pygame.display.set_caption('SET END POSITION')
                    end_flag = True
                    start_flag = False
                    obstacle_flag = False
                else:
                    pygame.display.set_caption("NO MODE SET")
                    end_flag = False
            elif event.key == pygame.K_2:
                if not obstacle_flag:
                    pygame.display.set_caption('SET OBSTACLES')
                    obstacle_flag = True
                    start_flag = False
                    end_flag = False
                else:
                    pygame.display.set_caption("NO MODE SET")
                    obstacle_flag = False
            elif event.key == pygame.K_SPACE:
                if not (start_pos is None or end_pos is None):
                    solve()
                else:
                    pygame.display.set_caption('PLEASE SET START AND END POSITIONS FIRST!')
        if event.type == pygame.MOUSEBUTTONDOWN:
            # noinspection DuplicatedCode
            if start_flag:
                if start_pos is not None:
                    pygame.draw.rect(surface, WHITE,
                                     [start_pos[0] + 1, start_pos[1] + 1, rect_width - 1, rect_width - 1])
                    start_pos = get_tile(pygame.mouse.get_pos())
                    pygame.draw.rect(surface, RED, [start_pos[0] + 1, start_pos[1] + 1, rect_width - 1, rect_width - 1])
                else:
                    start_pos = get_tile(pygame.mouse.get_pos())
                    pygame.draw.rect(surface, RED,
                                     [start_pos[0] + 1, start_pos[1] + 1, rect_width - 1, rect_width - 1])
                pygame.display.update()
            elif end_flag:
                if end_pos is not None:
                    pygame.draw.rect(surface, WHITE,
                                     [end_pos[0] + 1, end_pos[1] + 1, rect_width - 1, rect_width - 1])
                    end_pos = get_tile(pygame.mouse.get_pos())
                    pygame.draw.rect(surface, BLUE, [end_pos[0] + 1, end_pos[1] + 1, rect_width - 1, rect_width - 1])
                else:
                    end_pos = get_tile(pygame.mouse.get_pos())
                    pygame.draw.rect(surface, BLUE,
                                     [end_pos[0] + 1, end_pos[1] + 1, rect_width - 1, rect_width - 1])
                pygame.display.update()
            elif obstacle_flag:
                run_flag = True
                while run_flag:
                    for event1 in pygame.event.get():
                        if event1.type == pygame.QUIT:
                            pygame.quit()
                            sys.exit(0)
                        if event1.type == pygame.MOUSEBUTTONUP:
                            run_flag = False
                    position = get_tile(pygame.mouse.get_pos())
                    if not ((position == start_pos) or (position == end_pos)):
                        obstacles.add(position)
                        pygame.draw.rect(surface, BLACK, [position[0], position[1], rect_width, rect_width])
                        pygame.display.update()
            if event.button == 3:  # right mouse button click
                position = get_tile(pygame.mouse.get_pos())
                if position in obstacles:
                    obstacles.remove(position)
                    pygame.draw.rect(surface, WHITE, [position[0] + 1, position[1] + 1, rect_width - 1, rect_width - 1])
                    pygame.display.update()
