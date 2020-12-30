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

def energy():
    tot = 0
    for row in range(4):
        tot += abs(pos[row : row + 1]).sum() * abs(vel[row : row + 1]).sum()
    return tot

def dump_moons():
    print(pos)
    print(vel)

# steps is 10 for ex1.txt, 100 for ex2.txt and 1000 for input.txt
steps = 1000
for ts in range(steps):
    do_ts()

print('After %d steps:' % (ts + 1))
dump_moons()
print(energy())

