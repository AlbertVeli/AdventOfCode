#!/usr/bin/env python3

import sys
from collections import deque
from copy import deepcopy
from itertools import product

# read input
width = len(open(sys.argv[1]).readline().rstrip())
heigth = width
depth = 1
wdepth = 1

wlayers = deque()
z0 = deque()

def print_layer(rows):
    for i in range(len(rows)):
        print(''.join(rows[i]))

def print_layers():
    wi = 0
    for w in wlayers:
        zi = 0
        for z in w:
            print('w =', wi, 'z =', zi)
            print_layer(z)
            zi += 1
        wi += 1

def empty_layer(w, h):
    z = deque()
    for y in range(h):
        z.append(deque('.' * w))
    return z

def expand_zlayers(zl):
    zl.appendleft(empty_layer(width, heigth))
    zl.append(empty_layer(width, heigth))
    for z in zl:
        z.appendleft(deque('.' * width))
        z.append(deque('.' * width))
        for dq in z:
            dq.appendleft('.')
            dq.append('.')

def empty_zcube():
    z = deque()
    for _ in range(depth):
        z.append(empty_layer(width, heigth))
    return z

def expand_layers():
    wlayers.appendleft(empty_zcube())
    wlayers.append(empty_zcube())
    for w in wlayers:
        expand_zlayers(w)

# get pixel from wcopy (write changes to wlayers)
def get_pixel(x, y, z, w):
    if x >= 0 and x < width and y >= 0 and y < heigth and z >= 0 and z < depth and w >= 0 and w < wdepth:
        return wcopy[w][z][y][x]
    else:
        return '.'

def active_neighbors(x, y, z, w):
    count = 0
    offsets = list(product((-1, 0, 1), repeat=4))
    offsets.remove((0,0,0,0))
    for o in offsets:
        pixel = get_pixel(x + o[0], y + o[1], z + o[2], w + o[3])
        if pixel == '#':
            count += 1
    return count

def total_active():
    total = 0
    for w in wlayers:
        for z in w:
            for y in z:
                total += y.count('#')
    return total

w0 = deque()
for line in open(sys.argv[1]).read().splitlines():
    # each row in each layer a separate dq
    y = deque()
    for c in line:
        # Each pixel is . or #
        y.append(c)
    z0.append(y)
w0.append(z0)
wlayers.append(w0)

print_layers()

for rnd in range(1, 7):
    print('round', rnd)
    expand_layers()
    width += 2
    heigth += 2
    depth += 2
    wdepth += 2

    wcopy = deepcopy(wlayers)

    for w in range(wdepth):
        for z in range(depth):
            for y in range(heigth):
                for x in range(width):
                    neighbors = active_neighbors(x, y, z, w)
                    # get_pixel gets from zcopy, write to zlayers
                    curr = get_pixel(x, y, z, w)
                    if curr == '#':
                        if neighbors < 2 or neighbors > 3:
                            wlayers[w][z][y][x] = '.'
                    else:
                        if neighbors == 3:
                            wlayers[w][z][y][x] = '#'

    #print_layers()
    print(total_active())

