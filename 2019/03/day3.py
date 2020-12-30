#!/usr/bin/env python3

import sys

# Use array instead of list, much faster lookups
import array

dirs = { 'R': (1, 0),
         'L': (-1, 0),
         'U': (0, -1),
         'D': (0, 1) }

l1 = []
l2 = []

with open(sys.argv[1]) as f:
    for s in f.readline().split(','):
        l1.append((dirs[s[0]], int(s[1:])))
    for s in f.readline().split(','):
        l2.append((dirs[s[0]], int(s[1:])))

minx = 0
miny = 0
maxx = 0
maxy = 0

def minmax(line):
    global minx, maxx, miny, maxy
    x = 0
    y = 0
    for m, l in line:
        x += m[0] * l
        y += m[1] * l
        if x < minx:
            minx = x
        if x > maxx:
            maxx = x
        if y < miny:
            miny = y
        if y > maxy:
            maxy = y

minmax(l1)
minmax(l2)
w = maxx - minx + 1
h = maxy - miny + 1
ox = 0 - minx
oy = 0 - miny
isections = []

board = array.array('B', [0] * w * h)

# ytab for board lookup speedup
ytab = array.array('L')
for y in range(h):
    ytab.append(y * w)

def addline1(line):
    x = ox
    y = oy
    for m, l in line:
        dx = m[0]
        dy = m[1]
        for _ in range(l):
            x += m[0]
            y += m[1]
            board[ytab[y] + x] += 1

# Just need to check for intersections second time.
# No need to update board.
def addline2(line):
    x = ox
    y = oy
    for m, l in line:
        dx = m[0]
        dy = m[1]
        for _ in range(l):
            x += m[0]
            y += m[1]
            val = board[ytab[y] + x]
            if val == 1:
                isections.append((x, y))
                # Could update board here

addline1(l1)
addline2(l2)

# first star
d = []
for x, y in isections:
    d.append(abs(ox - x) + abs(oy - y))
print(min(d))

# second star
def isteps(line):
    x = ox
    y = oy
    sa = [0] * len(isections)
    steps = 0
    for m, l in line:
        dx = m[0]
        dy = m[1]
        for _ in range(l):
            x += m[0]
            y += m[1]
            steps += 1
            if (x, y) in isections:
                i = isections.index((x, y))
                sa[i] = steps
    return sa

s1 = isteps(l1)
s2 = isteps(l2)
#print(s1)
#print(s2)
sums = [x + y for x, y in zip(s1, s2)]
print(min(sums))
