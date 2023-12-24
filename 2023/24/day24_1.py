#!/usr/bin/env python3
import sys
sys.path.append('../..')
import aoc
from itertools import combinations

lines = []
for line in aoc.lines(sys.argv[1]):
    x, y, z, dx, dy, dz = aoc.ints(line)
    lines.append(((x, y, z), (dx, dy, dz)))

def intersection_2d(line1, line2, test_area):
    pos1, vel1 = line1
    pos2, vel2 = line2
    x1, y1, _ = pos1
    dx1, dy1, _ = vel1
    x2, y2, _ = pos2
    dx2, dy2, _ = vel2

    if dx1 * dy2 - dy1 * dx2 == 0:
        # No intersection at all
        #print('parallell')
        return False

    # Calculate the point of intersection
    t = ((x2 - x1) * dy2 - (y2 - y1) * dx2) / (dx1 * dy2 - dy1 * dx2)
    int_x = x1 + dx1 * t
    int_y = y1 + dy1 * t

    # Check if the intersection lies in the future or not
    rel_x1 = int_x - x1
    rel_y1 = int_y - y1
    rel_x2 = int_x - x2
    rel_y2 = int_y - y2

    # Lines moving closer together will intersect in the future
    moving_closer1 = (rel_x1 * dx1 + rel_y1 * dy1) >= 0
    moving_closer2 = (rel_x2 * dx2 + rel_y2 * dy2) >= 0
    if moving_closer1 and moving_closer2:
        #print(int_x, int_y, 'is the future ', end='')
        val_min, val_max = test_area
        if (int_x >= val_min) and (int_x <= val_max) and (int_y >= val_min) and (int_y <= val_max):
            #print('inside')
            return True
        else:
            #print('outside')
            return False

    #print(int_x, int_y, 'in the past')
    return False

n = 0
#test_area = (7, 27)
test_area = (200000000000000, 400000000000000)
for line1, line2 in combinations(lines, 2):
    if intersection_2d(line1, line2, test_area):
        n += 1
print('Part 1:', n)