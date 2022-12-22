#!/usr/bin/env python3

import sys
import re

rows = []
lines, moves = open(sys.argv[1]).read().rstrip().split('\n\n')
for line in lines.split('\n'):
    # x = index in line of first non-space character which
    # is the x-coordinate for the leftmost tile in row
    x = next(i.start() for i in re.finditer(r'\S', line))
    tiles = list(line.lstrip())
    # (startx, width of row, row tiles array)
    rows.append((x, len(tiles), tiles))

height = len(rows)

# Player start position (x, y)
player = (rows[0][0], 0)

#       right   down    left     up
dirs = ((1, 0), (0, 1), (-1, 0), (0, -1))
pdirs = (('>', 'v', '<', '^'))
pdir = 0

do_print_grid = False

def print_grid():
    if not do_print_grid:
        return
    sys.stdout.write('\n')
    for y in range(len(rows)):
        row = rows[y]
        startx = row[0]
        tiles = row[2]
        sys.stdout.write(' ' * row[0])
        for x in range(row[1]):
            if (startx + x, y) == player:
                sys.stdout.write(pdirs[pdir])
            else:
                sys.stdout.write(tiles[x])
        sys.stdout.write('\n')
    input('press any key to continue')

# edgemagheddon, the only difference to part 1
#      0  50 100
#         g  a
# 0      d.  . b
# 50   c c.e e
# 100 d.  .b
# 150 g.f f
#      a
#
# Just add all edge tiles to this dictionary
# edge[(x, y, rotation)] -> (newx, newy, newrotation)
edges = {}
for i in range(50):
    # a, going up -> a going up
    edges[(100 + i, 0, 3)] = (i, height - 1, 3)
    # a, going down -> a going down
    edges[(i, height - 1, 1)] = (100 + i, 0, 1)
    # b, going right -> b going left
    edges[(149, i, 0)] = (99, 149 - i, 2)
    # b, going right -> b going left
    edges[(99, 100 + i, 0)] = (149, 49 - i, 2)
    # c, going left -> c going down
    edges[(50, 50 + i, 2)] = (i, 100, 1)
    # c, going up -> c going right
    edges[(i, 100, 3)] = (50, 50 + i, 0)
    # d, going left -> d going right
    edges[(50, i, 2)] = (0, 149 - i, 0)
    # d, going left -> d going right
    edges[(0, 100 + i, 2)] = (50, 49 - i, 0)
    # e, going down -> e going left
    edges[(100 + i, 49, 1)] = (99, 50 + i, 2)
    # e, going right -> e going up
    edges[(99, 50 + i, 0)] = (100 + i, 49, 3)
    # f, going down -> f going left
    edges[(50 + i, 149, 1)] = (49, 150 + i, 2)
    # f, going right -> f going up
    edges[(49, 150 + i, 0)] = (50 + i, 149, 3)
    # g, going up -> g going right
    edges[(50 + i, 0, 3)] = (0, 150 + i, 0)
    # g, going left -> g going down
    edges[(0, 150 + i, 2)] = (50 + i, 0, 1)

# Try to move forward one step
def try_move_forward():
    global player, pdir
    px, py = player
    dx, dy = dirs[pdir]
    pedge = (px, py, pdir)
    tdir = pdir
    if pedge in edges:
        # Move over edge
        tx, ty, tdir = edges[pedge]
        row = rows[ty]
        startx = row[0]
        tx = tx - startx
    elif dy == 0:
        # Move horizontally in row py
        ty = py
        row = rows[py]
        startx = row[0]
        tx = px + dx - startx
    else:
        # Move vertically
        ty = py + dy
        row = rows[ty]
        startx = row[0]
        tx = px - startx

    if row[2][tx] == '#':
        # No movement
        return False

    # Did move forward one step
    player = (startx + tx, ty)
    pdir = tdir
    return True

# Move forward i steps or until blocked
def move_forward(i):
    for _ in range(i):
        if not try_move_forward():
            break
        print_grid()

def do_one_move():
    global moves, pdir
    c = moves[0]
    moves = moves[1:]
    if c == 'R':
        pdir = (pdir + 1) % 4
        print_grid()
    elif c == 'L':
        pdir = (pdir - 1) % 4
        print_grid()
    else:
        # number
        s = c
        while True:
            if len(moves) == 0:
                break
            peek = moves[0]
            if peek == 'L' or peek == 'R':
                break
            s = s + peek
            moves = moves[1:]
        move_forward(int(s))

# Do some edge checking, just for debug
# do_print_grid = True
# right, down, left, up
# 0      1     2     3
#states = ((149, 0, 3), (33, 199, 1), (149, 33, 0), (99, 110, 0))
#states = ((50, 99, 2), (10, 100, 3))
#states = ((50, 9, 2), (0, 103, 2))
#states = ((99, 52, 0), (103, 49, 1))
#for state in states:
#    x, y, d = state
#    player = (x, y)
#    pdir = d
#    print_grid()
#    move_forward(1)
#sys.exit(0)

while len(moves) > 0:
    do_one_move()

print(player, pdir)
print(1000 * (player[1] + 1) + 4 * (player[0] + 1) + pdir)
