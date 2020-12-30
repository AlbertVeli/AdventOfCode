#!/usr/bin/env python3

import sys
from itertools import combinations
import numpy as np

positions = []
velocities = []

for line in sys.stdin:
    line = line.rstrip().replace('<', '').replace('>', '').split(',')
    x = int(line[0].split('=')[1])
    y = int(line[1].split('=')[1])
    z = int(line[2].split('=')[1])
    positions.append([x, y, z])
    velocities.append([0, 0, 0])

# Use numpy arrays for faster operations array ops
pos = np.array(positions, dtype = np.int64)
vel = np.array(velocities, dtype = np.int64)

def gravity(ra, rb, va, vb):
    sa = np.sign(rb - ra)
    sb = np.sign(ra - rb)
    va += sa
    vb += sb

def do_ts():
    global pos, vel
    # update velocity by applying gravity
    for p in combinations(range(4), 2):
        ma = p[0]
        ra = pos[ma : ma + 1][0]
        va = vel[ma : ma + 1][0]
        mb = p[1]
        rb = pos[mb : mb + 1][0]
        vb = vel[mb : mb + 1][0]
        gravity(ra, rb, va, vb)

    # update position by applying velocity
    pos += vel

def column(i):
    return list(pos[:,i]) + list(vel[:,i])

# x,y,z repeat individually.
# Assume first repeated is initial state.
done = [False] * 3
xstart = column(0)
ystart = column(1)
zstart = column(2)
finished = [0, 0, 0]

# Increase if it doesnt work
steps = 300000
for ts in range(steps):
    do_ts()

    if not done[0]:
        x = column(0)
        if x == xstart:
            done[0] = True
            finished[0] = ts + 1

    if not done[1]:
        y = column(1)
        if y == ystart:
            done[1] = True
            finished[1] = ts + 1

    if not done[2]:
        z = column(2)
        if z == zstart:
            done[2] = True
            finished[2] = ts + 1

    if not False in done:
        break

i = finished
print('Axis repeat individually after', i, 'steps')

# All three will repeat after "least common multiplier"
# of the three intervals.
print(np.lcm(np.lcm(i[0], i[1]), i[2]))

