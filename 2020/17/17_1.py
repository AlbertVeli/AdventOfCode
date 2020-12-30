#!/usr/bin/env python3

import sys
from collections import deque
from copy import deepcopy
from itertools import product

# read input
width = len(open(sys.argv[1]).readline().rstrip())
heigth = width
depth = 1

zlayers = deque()
z0 = deque()

def print_layer(rows):
    for i in range(len(rows)):
        print(''.join(rows[i]))

def print_layers():
    zi = 0 - len(zlayers) // 2
    for z in zlayers:
        print('\nz=%d' % (zi))
        print_layer(z)
        zi += 1

def empty_layer(w, h):
    z = deque()
    for y in range(h):
        z.append(deque('.' * w))
    return z

def expand_layers():
    zlayers.appendleft(empty_layer(width, heigth))
    zlayers.append(empty_layer(width, heigth))
    for z in zlayers:
        z.appendleft(deque('.' * width))
        z.append(deque('.' * width))
        for dq in z:
            dq.appendleft('.')
            dq.append('.')

# get pixel from zcopy (write changes to zlayers)
def get_pixel(x, y, z):
    if x >= 0 and x < width and y >= 0 and y < heigth and z >= 0 and z < depth:
        return zcopy[z][y][x]
    else:
        return '.'

def active_neighbors(x, y, z):
    neighbors = []
    offsets = list(product((-1, 0, 1), repeat=3))
    offsets.remove((0,0,0))
    for o in offsets:
        neighbors.append(get_pixel(x + o[0], y + o[1], z + o[2]))
    return neighbors.count('#')

def total_active():
    total = 0
    for z in zlayers:
        for y in z:
            total += y.count('#')
    return total

for line in open(sys.argv[1]).read().splitlines():
    # each row in each layer a separate dq
    dq = deque()
    for c in line:
        # Each pixel is . or #
        dq.append(c)
    z0.append(dq)
zlayers.append(z0)


print_layers()

for rnd in range(1, 7):
    print('round', rnd)
    expand_layers()
    width += 2
    heigth += 2
    depth += 2

    zcopy = deepcopy(zlayers)

    for z in range(depth):
        for y in range(heigth):
            for x in range(width):
                neighbors = active_neighbors(x, y, z)
                # get_pixel gets from zcopy, write to zlayers
                curr = get_pixel(x, y, z)
                if curr == '#':
                    if neighbors < 2 or neighbors > 3:
                        zlayers[z][y][x] = '.'
                else:
                    if neighbors == 3:
                        zlayers[z][y][x] = '#'

    # TODO: remove empty lines/layers at beginning, end bottom and top

    #print_layers()
    print(total_active())

