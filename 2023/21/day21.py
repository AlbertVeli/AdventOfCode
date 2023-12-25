#!/usr/bin/env python3
import numpy as np

import sys
sys.path.append('../..')
import aoc

grid = aoc.lines(sys.argv[1])
width = len(grid[0])
height = len(grid)
grid = np.array([list(row) for row in grid])

# TODO: Visualise using pil
def dump_grid():
    for y, row in enumerate(grid):
        for x, c in enumerate(row):
            pos = (x, y)
            if pos in positions:
                print('O', end='')
            elif pos == start_pos:
                print('S', end='')
            else:
                print(c, end='')
        print('')

# Search for S
start_pos = np.where(grid == 'S')
start_pos = (start_pos[0][0], start_pos[1][0])
grid[start_pos] = '.'
positions = {start_pos}

# up, east, south, west
dirs = ((-1, 0), (0, 1), (1, 0), (0, -1))

def add_pos_dir(pos, dir):
    return (pos[0] + dir[0], pos[1] + dir[1])

def do_step(positions):
    new_positions = set()
    for pos in positions:
        for dir in dirs:
            x, y = add_pos_dir(pos, dir)
            c = grid[y % height][x % width]
            if c == '.':
                new_positions.add((x, y))
    return new_positions

points = []
for _ in range(64):
    positions = do_step(positions)
    points.append(len(positions))

#dump_grid()

print('Part 1:', len(positions))

# After 65 steps the diamond covers one grid.
# After 65 + 131 steps it covers one more grid
# to each side. And after another 131 steps
# it has grown one more grid (width is 131).
# 26501365 is of the form n * 131 + 65
# first do one more to get to 65
positions = do_step(positions)
points.append(len(positions))

# 3 points is enough to calculate the answer
# array index start at 0 so the point indexes
# are: 64 + n * width for n in range(3)
for _ in range(width * 2):
    positions = do_step(positions)
    points.append(len(positions))

# Thx William for the calculation below, I would
# have never figured this out on my own.

# Vandermonde matrix
A = np.matrix([[1, 0, 0], [1, 1, 1], [1, 2, 4]])
b = np.array([points[64 + n * width] for n in range(3)])
x = np.linalg.solve(A, b).astype(np.int64)
n = (26501365 - 65) // width
print('Part 2:', x[0] + x[1] * n + x[2] * n ** 2)