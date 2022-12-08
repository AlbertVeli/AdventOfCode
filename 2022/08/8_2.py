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

def score(x, y):
    xyh = forest[ytab[y] + x]
    # up
    up = 0
    for yy in range(y - 1, 0 - 1, -1):
        up += 1
        h = forest[ytab[yy] + x]
        if h >= xyh:
            break
    # down
    down = 0
    for yy in range(y + 1, heigth, 1):
        down += 1
        h = forest[ytab[yy] + x]
        if h >= xyh:
            break
    # left
    left = 0
    for xx in range(x - 1, 0 - 1, -1):
        left += 1
        h = forest[ytab[y] + xx]
        if h >= xyh:
            break
    # right
    right = 0
    for xx in range(x + 1, width, 1):
        right += 1
        h = forest[ytab[y] + xx]
        if h >= xyh:
            break

    return up * left * right * down

best = 0
for y in range(width):
    for x in range(heigth):
        xyscore = score(x, y)
        if xyscore > best:
            best = xyscore

print(best)
