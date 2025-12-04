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

def visualize():
    for y in range(h):
        print(grid[y])
    print('')

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
    poss = []
    for y in range(h):
        for x in range(w):
            if grid[y][x] == '@':
                n = neigh_cnt(x, y)
                if n < 4:
                    poss.append((x, y))
                    if remove:
                        # Remove as we go, faster
                        # but wrong for part 1
                        grid[y][x] = 'x'
                    count += 1
    if not remove:
        for xx, yy in poss:
            grid[yy][xx] = 'x'

    return count

visualize()

cnt = one_pass()

visualize()

print('Part 1:', cnt)

n = 1
while n > 0:
    n = one_pass(remove = True)
    cnt += n

visualize()

print('Part 2:', cnt)
