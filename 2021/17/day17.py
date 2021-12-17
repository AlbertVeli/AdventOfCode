#!/usr/bin/env python3

import sys
sys.path.insert(0,'../')
from aoc_input import *

if len(sys.argv) != 2:
    print('Usage:', sys.argv[0], '<input.txt>')
    sys.exit(1)

x1, x2, y2, y1 = input_as_line_of_ints(sys.argv[1])
#print(x1, x2, y1, y2)

def within(x, y):
    return x >= x1 and x <= x2 and y <= y1 and y >= y2

def hit(dx, dy):
    x, y = (0, 0)
    maxy = -10000
    while True:
        x += dx
        y += dy
        dy -= 1
        if dx > 0:
            dx -= 1
        if y > maxy:
            maxy = y
        if within(x, y):
            return (True, maxy)
        if x > x2 or y < y2:
            return (False, False)

maxy = 0
p = (0, 0)
hits = []
for dy in range(-200, 200):
    for dx in range(200):
        h, y = hit(dx, dy)
        if h:
            hits.append((dx, dy))
            if y > maxy:
                maxy = y
                p = (dx, dy)

print('part 1:', p, maxy)
print('part 2:', len(hits))
