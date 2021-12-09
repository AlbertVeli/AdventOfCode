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
for w in a:
    b.append([int(c) for c in w])

sy = len(b)
sx = len(b[0])

# a = sx * sy 2d array
a = np.array(b)

def is_low(y, x):
    val = a[y][x]
    tpoints = [(y - 1, x), (y + 1, x), (y, x - 1), (y, x + 1)]
    for ty, tx in tpoints:
        if tx < 0 or (tx > sx - 1) or ty < 0 or (ty > sy - 1):
            # Outside grid
            continue

        if val >= a[ty][tx]:
            # Not low point
            return False

    return True

low_points = []
for y in range(sy):
    for x in range(sx):
        if is_low(y, x):
            low_points.append((y, x))

risk = 0
for l in low_points:
    risk += a[l] + 1

# Part 1
print(risk)


# Flood fill
def basin(y, x):
    points = [(y, x)]
    done = []
    while True:
        # Pick point from points that is not in done
        point = False
        for p in points:
            if not p in done:
                point = p
                break
        if not point:
            # Done, all points handled
            return points

        # Check adjacent points
        new_points = []
        y = p[0]
        x = p[1]
        tpoints = [(y - 1, x), (y + 1, x), (y, x - 1), (y, x + 1)]
        for ty, tx in tpoints:
            if tx < 0 or (tx > sx - 1) or ty < 0 or (ty > sy - 1):
                # Outside grid
                continue
            if (not (ty, tx) in points) and a[ty][tx] < 9:
                new_points.append((ty, tx))
        done.append(p)
        points += new_points

lens = []
for y, x in low_points:
    bpoints = basin(y, x)
    lens.append(len(bpoints))

# Part 2
print(np.prod(sorted(lens)[-3:]))
