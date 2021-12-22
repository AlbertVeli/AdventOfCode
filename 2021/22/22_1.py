#!/usr/bin/env python3

import sys
import re
import numpy as np

if len(sys.argv) != 2:
    print('Usage:', sys.argv[0], '<input.txt>')
    sys.exit(1)

cubes = []
for s in open(sys.argv[1]):
    s = s.rstrip()
    if s.startswith('on'):
        val = 1
    else:
        val = 0
    x1, x2, y1, y2, z1, z2 = list(map(int, re.findall(r'([-+]?\d+)', s)))
    if x1 < -50 or x1 > 50:
        break
    # Transpose x,y,z from -50 - 50 to 0 - 100
    cubes.append([val, (x1 + 50, x2 + 50, y1 + 50, y2 + 50, z1 + 50, z2 + 50)])

def set_cube(val, coords):
    x1, x2, y1, y2, z1, z2 = coords
    a[z1 : z2 + 1, y1 : y2 + 1, x1 : x2 + 1] = val

a = np.zeros((101, 101, 101), dtype = bool)
for val, coords in cubes:
    set_cube(val, coords)

print(np.sum(a))
