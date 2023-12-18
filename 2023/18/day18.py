#!/usr/bin/env python3
import sys
sys.path.append('../..')
import aoc
# for flood fill
# TODO: Use shoelace formula instead
# that will work for part 2 and no
# need to install scikit-image
import numpy as np
from skimage import segmentation

def add_pos_dir(pos, dir):
    return tuple(map(sum, zip(pos, dir)))

dirs = {
    'R': (1, 0),
    'D': (0, 1),
    'L': (-1, 0),
    'U': (0, -1)
}

lines = aoc.lines(sys.argv[1])

edges = dict()
pos = (0, 0)
corners = [pos]
minx = 0
miny = 0
maxx = 0
maxy = 0

def update_max(pos):
    global maxx, minx, maxy, miny
    x, y = pos
    if x < minx:
        minx = x
    if x > maxx:
        maxx = x
    if y < miny:
        miny = y
    if y > maxy:
        maxy = y

for line in lines:
    dir = line[0]
    line = line[2:].split()
    length = int(line[0])
    color = line[1][2:-1]
    d = dirs[dir]
    for _ in range(length):
        pos = add_pos_dir(pos, d)
        edges[pos] = color
    # No need to update inside loop
    update_max(pos)
    corners.append(pos)

width = maxx + 1 - minx
height = maxy + 1 - miny

# Create .# grid for visualization and debugging
grid = [[0 for _ in range(width)] for _ in range(height)]

def dump_grid():
    for row in grid:
        for n in row:
            if n == 0:
                sys.stdout.write('.')
            elif n == 1:
                sys.stdout.write('#')
            elif n == 2:
                sys.stdout.write('O')
        print('')
    print('')

dump_grid()

new_edges = dict()
for pos in edges.keys():
    # Note, minx/miny may be negative, translate to 0,0
    x, y = pos
    x = x - minx
    y = y - miny
    new_edges[(x, y)] = edges[pos]
    grid[y][x] = 1

dump_grid()

def find_inside():
    # Find one '.' on the inside
    for y, row in enumerate(grid):
        inside = False
        for x, c in enumerate(row):
            if c == 1:
                inside = not inside
            elif c == 0 and inside:
                return (x, y)

def flood_fill():
    x, y = find_inside()
    a = np.array(grid)
    new_grid = segmentation.flood_fill(a, (y, x), 2)
    print(new_grid)
    print('Part 1:', np.count_nonzero(new_grid != 0))

flood_fill()