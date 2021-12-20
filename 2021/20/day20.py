#!/usr/bin/env python3

import sys
import numpy as np

if len(sys.argv) != 2:
    print('Usage:', sys.argv[0], '<input.txt>')
    sys.exit(1)

a = []
first = True
for s in open(sys.argv[1]).readlines():
    s = s.rstrip()
    if len(s) > 0:
        l = list(map(lambda x: 1 if x == '#' else 0, list(s)))
        if first:
            first = False
            algo = l
        else:
            a.append(l)

a = np.array(a)

def pad(a, val):
    l = [val] * a.shape[1]
    a = np.vstack([l, a, l])
    l = []
    for _ in range(a.shape[0]):
        l.append([val])
    a = np.hstack([l, a, l])
    return a

def faltning(a, x, y):
    l = []
    for i in range(3):
        l += list(map(str, (a[y-1+i,x-1:x+2])))
    algoix = int(''.join(l), 2)
    return algo[algoix]

def step(a, val):
    # pad two
    a = pad(np.array(a), val)
    a = pad(np.array(a), val)
    sy, sx = a.shape
    newa = np.array(a)
    for y in range(1, sy - 1):
        for x in range(1, sx - 1):
            newa[y][x] = faltning(a, x, y)
    # remove outer border
    return newa[1 : sy - 1, 1 : sx - 1]

def print_a(a):
    for y in range(a.shape[0]):
        for x in range(a.shape[1]):
            c = '.' if a[y][x] == 0 else '#'
            sys.stdout.write(c)
        sys.stdout.write('\n')


# pad alternating between algo[0] and algo[-1]
pads = [algo[0], algo[-1]]
# for example to work set both to 0
if pads[0] == 0:
    pads[1] = 0
padi = 1
steps = 50
#print_a(a)
for i in range(steps):
    a = step(a, pads[padi])
    if i == 1:
        print('part 1:', len(np.where(a == 1)[0]))
    elif i == 49:
        print('part 2:', len(np.where(a == 1)[0]))
    # alternate between 0 and 1
    padi = 1 - padi
