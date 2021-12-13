#!/usr/bin/env python3

import sys
sys.path.insert(0,'../')
from aoc_input import *
import re
import numpy as np

if len(sys.argv) != 2:
    print('Usage:', sys.argv[0], '<input.txt>')
    sys.exit(1)

a = input_as_lines(sys.argv[1])

folds = []
coords = []
maxx = -1
maxy = -1
for s in a:
    if s.startswith('fold'):
        f, si = re.findall(r'fold along ([xy])=(\d+)', s)[0]
        folds.append((f, int(si)))
    else:
        try:
            x, y = re.findall(r'(\d+),(\d+)', s)[0]
        except:
            continue
        x = int(x)
        y = int(y)
        coords.append((y, x))
        if x > maxx:
            maxx = x
        if y > maxy:
            maxy = y

b = [[False] * (maxx + 1)] * (maxy + 1)
sy = len(b)
sx = len(b[0])
a = np.array(b, dtype = bool)
for y, x in coords:
    a[y][x] = True

def foldy(row):
    global a
    for y2 in range(row + 1, sy):
        y1 = row - (y2 - row)
        a[y1] |= a[y2]
    a = a[0:row]

def foldx(col):
    global a
    for x2 in range(col + 1, sx):
        x1 = col - (x2 - col)
        a[:,x1] |= a[:,x2]
    a = a[:,0:col]

f = folds[0]
if f[0] == 'x':
    foldx(f[1])
else:
    foldy(f[1])
print(np.count_nonzero(a == True))
