#!/usr/bin/env python3

import sys
sys.path.append('../..')
import aoc

grid = aoc.char_matrix(sys.argv[1])

h = len(grid)
w = len(grid[0])

dirs = [
    (-1, -1), (0, -1), (1, -1),
    (-1,  0),          (1,  0),
    (-1,  1), (0,  1), (1,  1),
]

def neigh_cnt(x, y):
    count = 0
    for dx, dy in dirs:
        nx, ny = x + dx, y + dy
        if 0 <= nx < w and 0 <= ny < h:
            if grid[ny][nx] == '@':
                count += 1

    return count

def one_pass(remove = False):
    count = 0
    for y in range(h):
        for x in range(w):
            if grid[y][x] == '@':
                n = neigh_cnt(x, y)
                if n < 4:
                    if remove:
                        grid[y][x] = 'x'
                    count += 1
    return count

print('Part 1:', one_pass())

cnt = 0
n = 1
while n > 0:
    n = one_pass(True)
    cnt += n

print('Part 2:', cnt)
