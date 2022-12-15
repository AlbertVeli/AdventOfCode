#!/usr/bin/env python3

import sys
import re

xs = set()
ys = set()
lines = open(sys.argv[1]).read().rstrip().split('\n')
sensors = []
beacons = []
for line in lines:
    sx, sy, bx, by = list(map(int, re.findall(r'([-]?\d+)', line)))
    xs.add(sx)
    xs.add(bx)
    ys.add(sy)
    ys.add(by)
    sensors.append((sx, sy))
    beacons.append((bx, by))

minx  = min(xs)
maxx = max(xs)
miny = min(ys)
maxy = max(ys)

# return range where manhattan distance
# between sensor i and beacon i covers row
# list of size 0, 1 or 2 (split range)
def manhattan_row(i, row):
    sx, sy = sensors[i]
    bx, by = beacons[i]
    dist = abs(sx - bx) + abs(sy - by)
    disty = abs(row - sy)
    distx = dist - disty

    if distx < 0:
        # manhattan diamont doesn't touch row
        #print('no', sensors[i], beacons[i], [])
        return []

    # manhattan diamont from sx - distx to sx + distx
    min_col = sx - distx
    max_col = sx + distx
    if by != row:
        #print(sensors[i], beacons[i], [(min_col, max_col)])
        return [(min_col, max_col)]

    # split range, beacon is at row
    ranges = []
    #print('beacon at', bx)
    # range 1, min_col - (bx - 1)
    x1 = bx - 1
    if x1 - min_col >= 0:
        #print('range 1', sensors[i], beacons[i], (min_col, x1))
        ranges.append((min_col, x1))
    # range 2, bx + 1 - (max_col)
    x2 = bx + 1
    if max_col - x2 >= 0:
        #print('range 2', sensors[i], beacons[i], (x2, max_col))
        ranges.append((x2, max_col))
    return ranges

impossible = set()

# Would be more efficient to save all the ranges here
# instead of every x-coordinate
def add_impossible(r):
    x1, x2 = r
    for x in range(x1, x2 + 1):
        impossible.add(x)

for i in range(len(sensors)):
    ranges = manhattan_row(i, 2000000)
    print(sensors[i], beacons[i], ranges)
    for r in ranges:
        add_impossible(r)

print('Part 1:', len(impossible))
