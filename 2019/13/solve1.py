#!/usr/bin/env python3

from collections import deque
# Use intmachine from ../common
import sys
sys.path.insert(0,'../common')
from intmachine import Intmachine

# Read program from stdin
prog = []
for i in map(int, input('').split(',')):
    prog.append(i)

# 0 for input, 1 for output
queues = []
for _ in range(2):
    dq = deque()
    queues.append(dq)

# Create and connect machine
m = Intmachine('d13', prog, queues[0], queues[1])

minx = 10000
maxx = 0
miny = 10000
maxy = 0
# part 1, don't play the game, only add blocks
blocks = []
def do_game(x, y, tile):
    global minx, maxx, miny, maxy
    if x < minx:
        minx = x
    if y < miny:
        miny = y
    if x > maxx:
        maxx = x
    if y > maxy:
        maxy = y
    # 0 = empty
    # 1 = wall
    # 2 = block
    # 3 = paddle
    # 4 = ball
    if tile == 2:
        # add block
        if not (x, y) in blocks:
            blocks.append((x, y))

running = True
while running:
    while len(queues[1]) < 3 and running:
        running = m.do_op()
    if running:
        # Got three outputs
        x = m.pop()
        y = m.pop()
        tile = m.pop()
        do_game(x, y, tile)

print(minx, maxx, miny, maxy)
print(len(blocks))
