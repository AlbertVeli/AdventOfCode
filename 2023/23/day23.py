#!/usr/bin/env python3

import sys
sys.path.append('../..')
import aoc
import copy
from collections import deque
from random import shuffle

grid = aoc.char_matrix(sys.argv[1])
width = len(grid[0])
height = len(grid)

start_position = (grid[0].index('.'), 0)
end_position = (grid[-1].index('.'), height - 1)

def dump_grid(visited: list[tuple]):
    for y, row in enumerate(grid):
        for x, c in enumerate(row):
            if (x, y) in visited:
                print('O', end='')
            else:
                print(c, end='')
        print('')

# south, west, up, east
dirs = ((0, 1), (-1, 0), (0, -1), (1, 0))

def add_pos_dir(pos, dir):
    return tuple(map(sum, zip(pos, dir)))

def possible_positions(cur_pos, visited):
    l = []
    for dir in dirs:
        x, y = add_pos_dir(cur_pos, dir)
        if x < 0 or x > width - 1 or y < 0 or y > height - 1:
            continue
        if (x, y) in visited:
            continue
        c = grid[y][x]
        if c == '#':
            continue
        elif c == '>' and dir == (-1, 0):
            continue
        elif c == 'v' and dir == (0, -1):
            continue
        else:
            l.append((x, y))
    return l

def find_max_path(from_pos: tuple, visited: deque[tuple], taken_steps: int, debug = False):
    if from_pos == end_position:
        if debug:
            #dump_grid(single_visited)
            #input('')
            # One of these returns has the correct answer
            # print all of them and find max using max.py
            print(taken_steps)
            sys.stdout.flush()
        return taken_steps

    # Optimization, continue walking until a fork
    # this reduces recursion depth
    single_steps = 0
    single_visited = copy.copy(visited)
    while True:
        positions = possible_positions(from_pos, single_visited)
        l = len(positions)
        if l > 1:
            break
        if l == 0:
            # nowhere to go, return 0
            break
        from_pos = positions[0]
        single_visited.append(from_pos)
        single_steps += 1
        if from_pos == end_position:
            if debug:
                #dump_grid(single_visited)
                #input('')
                # This may also be the correct answer
                print(taken_steps + single_steps)
                sys.stdout.flush()
            return taken_steps + single_steps

    max_steps = 0
    # Do random walk, start multiple instances, aggregate outputs
    # Hope to find max in some of them
    shuffle(positions)
    for new_pos in positions:
        new_visited = copy.copy(single_visited)
        new_visited.append(new_pos)
        new_steps = find_max_path(new_pos, new_visited, taken_steps + single_steps + 1, debug)
        if new_steps > max_steps:
            max_steps = new_steps
    if debug:
        print(max_steps)
        sys.stdout.flush()
    return max_steps

# Probably not good solution if this is needed...
sys.setrecursionlimit(10000)

# deque has faster append than list
#print('Part 1:', find_max_path(start_position, deque([start_position]), 0))
#dump_grid([start_position])
# Part 2, remove all '>', 'v' slopes
for row in grid:
    for x, c in enumerate(row):
        if c == '>' or c == 'v' or c == '<' or c == '^':
            row[x] = '.'
#dump_grid([start_position])

# If you're lucky find_max_path will print the max path after a few hours
# but it will not finish in reasonable time, but there is still a probability
# one of the printed is max. Run multiple instances and aggregate with max.py
print('Part 2:', find_max_path(start_position, deque([start_position]), 0, debug = True))