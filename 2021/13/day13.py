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
    try:
        a[:row] |= a[sy-1:row:-1]
    except:
        print('error:', a.shape, 'row', row)
    a = a[:row]

def foldx(col):
    global a
    try:
        a[:,:col] |= a[:,sx-1:col:-1]
    except:
        print('error:', a.shape, 'col', col)
    a = a[:,:col]

def print_a():
    global a
    for ly in a:
        for b in ly:
            if b:
                c = '#'
            else:
                c = '.'
            sys.stdout.write(c)
        sys.stdout.write('\n')

for i in range(len(folds)):
    axis, val = folds[i]
    if axis == 'x':
        foldx(val)
    else:
        foldy(val)
    sy, sx = a.shape
    if i == 0:
        print('part 1:', np.count_nonzero(a == True))
print('part 2:')
print_a()

