#!/usr/bin/env python3

import sys
import numpy as np

if len(sys.argv) != 2:
    print('Usage:', sys.argv[0], '<input.txt>')
    sys.exit(1)

a = []
for line in open(sys.argv[1]):
    a.append(list(line.rstrip()))
a = np.array(a)
sy, sx = a.shape

# Could probably move without copying a
# but logic is simpler if keeping a copy
def move(a):
    moved = False
    # Move right
    a_org = np.array(a)
    for y in range(sy):
        ny = y
        for x in range(sx):
            if a_org[y][x] != '>':
                continue
            nx = (x + 1) % sx
            if a_org[ny][nx] == '.':
                a[ny][nx] = '>'
                a[y][x] = '.'
                moved = True
    # Move down
    a_org = np.array(a)
    for y in range(sy):
        ny = (y + 1) % sy
        for x in range(sx):
            nx = x
            if a_org[y][x] != 'v':
                continue
            if a_org[ny][nx] == '.':
                a[ny][nx] = 'v'
                a[y][x] = '.'
                moved = True
    return moved

moves = 0
while move(a):
    moves += 1

#print(a)
print(moves + 1)
