#!/usr/bin/env python3

from PIL import Image
from collections import deque
# Use intmachine from ../common
import sys
sys.path.insert(0,'../common')
from intmachine import Intmachine

# up, right, down, left
dirs = ((0, -1), (1, 0), (0, 1), (-1, 0))
dirchange = (-1, 1)
curdir = 0
rx = 0
ry = 0
# (x, y)
paintcoords = []
# color
paintcols = []

# i = 0 or 1, second output from robot
def change_dir(i):
    global curdir
    curdir = (curdir + dirchange[i]) % 4

def paint(x, y, c):
    if (x, y) in paintcoords:
        i = paintcoords.index((x, y))
        paintcols[i] = c
    else:
        paintcoords.append((x, y))
        paintcols.append(c)

# Color c, dirchange d, outputs from robot
def paint_move(c, d):
    global rx, ry
    #print('DBG: painting %d,%d col %d; turn %d' % (rx, ry, c, d))
    paint(rx, ry, c)
    change_dir(d)
    dr = dirs[curdir]
    #print('DBG: dir is now %d' % (curdir), dr)
    rx += dr[0]
    ry += dr[1]

#n = 0
def color(x, y):
    global n
    if (x, y) in paintcoords:
        i = paintcoords.index((x, y))
        c = paintcols[i]
    else:
        # Initial color = 0 (black)
        c = 0
    #n += 1
    #print('%d: (%d,%d) color %d' % (n, x, y, c), m.finished_nice())
    return c


# Read program from stdin
prog = []
for i in map(int, input('').split(',')):
    prog.append(i)

# Create queues, 0 for input, 1 for output
queues = []
for _ in range(2):
    dq = deque()
    queues.append(dq)

# Create and connect machine
m = Intmachine('d11', prog, queues[0], queues[1])

queues[0].clear()
m.reset()

# Part 2, put color 1 at rx, ry before start.
# For part 1, comment out 2 rows below.
paintcoords.append((rx, ry))
paintcols.append(1)

running = True
while running:
    # push input
    c = color(rx, ry)
    m.push(c)
    while len(m.oq) < 2 and running:
        running = m.do_op()
    # Got two outputs
    if len(m.oq) == 2:
        c = m.pop()
        d = m.pop()
        paint_move(c, d)

# part 1
print(len(paintcoords))

# get dimensions
minx = 10000
maxx = -10000
miny = 10000
maxy = -10000
for t in paintcoords:
    x = t[0]
    y = t[1]
    if x < minx:
        minx = x
    if x > maxx:
        maxx = x
    if y < miny:
        miny = y
    if y > maxy:
        maxy = y
#print(minx, maxx, miny, maxy)

# Create PIL Image
w = maxx - minx + 1
h = maxy - miny + 1
colors = [(0, 0, 0), (255, 255, 255)]
im = Image.new('RGB', (w, h))
for y in range(h):
    offs = y * w
    yy = y + miny
    for x in range(w):
        xx = x + minx
        if (xx, yy) in paintcoords:
            i = paintcoords.index((xx, yy))
            c = colors[paintcols[i]]
        else:
            c = colors[0]
        im.putpixel((x, y), c)
im.save('out.png')
