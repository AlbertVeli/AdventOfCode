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

# Try to move forward one step
def try_move_forward():
    global player
    px, py = player
    dx, dy = dirs[pdir]
    if dy == 0:
        # Move horizontally in row py
        ty = py
        row = rows[py]
        startx = row[0]
        tx = (px + dx - startx) % row[1]
    else:
        # Move vertically
        ty = (py + dy) % height
        row = rows[ty]
        startx = row[0]
        tx = px - startx
        while tx < 0 or tx >= row[1]:
            # Wrap around vertically, continue
            # moving in y dir until valid tx
            ty = (ty + dy) % height
            row = rows[ty]
            startx = row[0]
            tx = px - startx

    if row[2][tx] == '#':
        # No movement
        return False

    # Did move forward one step
    player = (startx + tx, ty)
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

while len(moves) > 0:
    do_one_move()

print(player, pdir)
print(1000 * (player[1] + 1) + 4 * (player[0] + 1) + pdir)
