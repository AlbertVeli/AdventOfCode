#!/usr/bin/env python3

import sys
sys.path.insert(0,'../')
from aoc_input import *
import numpy as np

if len(sys.argv) != 2:
    print('Usage:', sys.argv[0], '<input.txt>')
    sys.exit(1)

a = input_as_lines(sys.argv[1])
b = []
for s in a:
    b.append(list(map(int,list(s))))
sy = len(b)
sx = len(b[0])
a = np.array(b)

flashes = 0

def flashgorithm():
    global a
    global flashes
    ys, xs = np.where(a > 9)
    l = len(ys)
    for i in range(l):
        y = ys[i]
        x = xs[i]
        # flash x,y, 0 marks flashed
        a[y][x] = 0
        # Increase adjacent cells, unless 0
        tcells = [(y - 1, x), (y + 1, x), (y, x - 1), (y, x + 1),
                (y - 1, x - 1), (y + 1, x - 1), (y - 1, x + 1), (y + 1, x + 1)]
        for ty, tx in tcells:
            if tx < 0 or (tx > sx - 1) or ty < 0 or (ty > sy - 1):
                # Outside grid
                continue
            if a[ty][tx] != 0:
                a[ty][tx] += 1
        flashes += 1
    # l = number of cells flashed
    return l

def round():
    global a
    a = a + 1
    # Run flashgorithm until no new flashes
    while True:
        if flashgorithm() == 0:
            break

for i in range(1000):
    round()
    if len(np.where(a == 0)[0]) == sx * sy:
        print('part 2:', i + 1)
        # Done, if i < 100 remove break to
        # get part 1
        break
    if i == 100:
        print('part 1:', flashes)
