#!/usr/bin/env python3

import sys
sys.path.insert(0,'../')
from aoc_input import *
import numpy as np

if len(sys.argv) != 2:
    print('Usage:', sys.argv[0], '<input.txt>')
    sys.exit(1)

a = input_as_lines(sys.argv[1])
lines = []
for line in a:
    x1, y1, x2, y2 = map(int, re.findall(r'([-+]?\d+)', line))
    lines.append([x1, y1, x2, y2])

def draw_diagonal(x1, y1, x2, y2):
    if x2 < x1:
        tmpx = x1
        tmpy = y1
        x1 = x2
        y1 = y2
        x2 = tmpx
        y2 = tmpy
    y = y1
    if y2 > y1:
        ydir = 1
    else:
        ydir = -1
    for x in range(x1, x2 + 1):
        board[y][x] += 1
        y += ydir

def draw_line(x1, y1, x2, y2):
    if x2 < x1:
        tmp = x1
        x1 = x2
        x2 = tmp
    if y2 < y1:
        tmp = y1
        y1 = y2
        y2 = tmp
    for x in range(x1, x2 + 1):
        for y in range(y1, y2 + 1):
            board[y][x] += 1

# part 1
zeros = [ [0] * 1000 for _ in range(1000)]
board = np.array(zeros, int)

for i in range(len(lines)):
    x1, y1, x2, y2 = lines[i]
    if x1 == x2 or y1 == y2:
        draw_line(x1, y1, x2, y2)

# Print it out for debugging
for y in range(10):
    for x in range(10):
        sys.stdout.write(str(board[y][x]))
        sys.stdout.write(' ')
    print('')
print('part 1:', np.count_nonzero(board > 1))

# part 2
board = np.array(zeros, int)

for i in range(len(lines)):
    x1, y1, x2, y2 = lines[i]
    if x1 != x2 and y1 != y2:
        draw_diagonal(x1, y1, x2, y2)
    else:
        draw_line(x1, y1, x2, y2)
print('part 2:', np.count_nonzero(board > 1))
