#!/usr/bin/env python3

import sys
sys.path.append('../..')
import aoc

# For visualization and debugging
def print_matrix(matrix, pos):
    # Clear screen
    print("\033[2J\033[H", end="")
    for y, row in enumerate(matrix):
        line = ''.join('@' if (x, y) == pos else cell for x, cell in enumerate(row))
        print(line)
    print()  # Add a blank line for separation
    input('Press Enter to continue...')

def find_coord(char):
    for y, row in enumerate(a):
        for x, cell in enumerate(row):
            if cell == char:
                return x, y
    return None

def get_char(x, y):
    return a[y][x]

def put_char(pos, c):
    x, y = pos
    a[y][x] = c

def walk_one_step(pos, curdir):
    x, y = pos

    dy, dx = directions[curdir]
    next_x, next_y = x + dx, y + dy

    # Check if outside grid
    if not (0 <= next_y < rows and 0 <= next_x < cols):
        return None, curdir

    next_char = get_char(next_x, next_y)
    if next_char == '.':
        # Walk straight
        return (next_x, next_y), curdir
    else:
        # Turn 90 degrees right
        new_direction = (curdir + 1) % 4
        return pos, new_direction

def simulate(obstruction, start):
    pos = start
    curdir = 0
    # visited in this simulation, with direction
    visited = set()

    put_char(obstruction, 'O')

    while pos is not None:
        #print_matrix(a, pos)
        if (pos, curdir) in visited:
            # Loop detected
            put_char(obstruction, '.')
            return 1

        visited.add((pos, curdir))
        pos, curdir = walk_one_step(pos, curdir)

    # No loop detected
    put_char(obstruction, '.')
    return 0

# --- Main ---

# globals
a = aoc.char_matrix(sys.argv[1])
rows, cols = len(a), len(a[0])
start = find_coord('^')
put_char(start, '.')
# up, right, down, left
directions = [(-1, 0), (0, 1), (1, 0), (0, -1)]

# part 1
visited = set()
visited.add(start)
pos = start
curdir = 0
while pos is not None:
    pos, curdir = walk_one_step(pos, curdir)
    if pos is not None:
        visited.add(pos)
        #print_matrix(a, pos)
print('Part 1:', len(visited))

# part 2
loops = 0
# Simulate with obstruction at each visited point
for obs in visited:
    if obs == start:
        continue
    loops += simulate(obs, start)
print('Part 2:', loops)
