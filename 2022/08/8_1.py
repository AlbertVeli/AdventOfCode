#!/usr/bin/env python3

import sys

if len(sys.argv) != 2:
    print('Usage:', sys.argv[0], '<input.txt>')
    sys.exit(1)

lines = open(sys.argv[1]).read().rstrip().split('\n')
width = len(lines)
heigth = len(lines[0])
forest = []
ytab = []
y = 0
for line in lines:
    forest += list(map(int, list(line)))
    ytab.append(y * width)
    y += 1

def visible(x, y):
    xyh = forest[ytab[y] + x]
    # up
    visible = True
    for yy in range(y - 1, 0 - 1, -1):
        h = forest[ytab[yy] + x]
        if h >= xyh:
            visible = False
            break
    if visible:
        return True
    # down
    visible = True
    for yy in range(y + 1, heigth, 1):
        h = forest[ytab[yy] + x]
        if h >= xyh:
            visible = False
            break
    if visible:
        return True
    # left
    visible = True
    for xx in range(x - 1, 0 - 1, -1):
        h = forest[ytab[y] + xx]
        if h >= xyh:
            visible = False
            break
    if visible:
        return True
    # right
    visible = True
    for xx in range(x + 1, width, 1):
        h = forest[ytab[y] + xx]
        if h >= xyh:
            visible = False
            break
    if visible:
        return True

    return False

total = 0
for y in range(width):
    for x in range(heigth):
        if visible(x, y):
            total += 1

print(total)
