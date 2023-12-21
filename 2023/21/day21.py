#!/usr/bin/env python3
from copy import deepcopy

import sys
sys.path.append('../..')
import aoc

lines = aoc.lines(sys.argv[1])

# Add border of '#' characters
# TODO: This will not work for part 2
# in part 2 the grid extends infinitly
grid = ['#' * (len(lines[0]) + 2)]
for row in lines:
    grid.append('#' + row + '#')
grid.append('#' * (len(lines[0]) + 2))

def dump_grid():
    for y, row in enumerate(grid):
        for x, c in enumerate(row):
            if (x, y) in positions:
                print('O', end='')
            else:
                print(c, end='')
        print('')

positions = set()

# Search for S
for y, row in enumerate(grid):
    if 'S' in row:
        x = row.index('S')
        positions.add((x, y))

# up, east, south, west
dirs = ((0, -1), (1, 0), (0, 1), (-1, 0))

dump_grid()

def add_pos_dir(pos, dir):
    return tuple(map(sum, zip(pos, dir)))

def do_step(positions):
    new_positions = set()
    for pos in positions:
        for dir in dirs:
            x, y = add_pos_dir(pos, dir)
            c = grid[y][x]
            if c == '.' or c == 'S':
                new_positions.add((x, y))
    return new_positions

for _ in range(64):
    old_len = len(positions)
    positions = do_step(positions)
    new_len = len(positions)
    # This diff should start repeating in part 2
    print(new_len - old_len)

dump_grid()

print('Part 1:', len(positions))