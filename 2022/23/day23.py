#!/usr/bin/env python3

import sys

# Globals
elves = set()

#         E       SE      S        SW       W        NW        N       NE
dirs = ((1, 0), (1, 1), (0, 1), (-1, 1), (-1, 0), (-1, -1), (0, -1), (1, -1))
# Middle direction is straight, index 0 and 2 are diagonals
dirs_n = dirs[5:8]
dirs_s = dirs[1:4]
dirs_w = dirs[3:6]
dirs_e = dirs[1], dirs[0], dirs[7]
# Check in this order
dirs_order = (dirs_n, dirs_s, dirs_w, dirs_e)

def max_xy(points):
    return max(p[0] for p in points), max(p[1] for p in points)

def min_xy(points):
    return min(p[0] for p in points), min(p[1] for p in points)

# Print out grid, for debug
def print_grid(points):
    maxx, maxy = max_xy(points)
    minx, miny = min_xy(points)
    empty = 0
    for y in range(miny, maxy + 1):
        for x in range(minx, maxx + 1):
            if (x, y) in points:
                sys.stdout.write('#')
            else:
                empty += 1
                sys.stdout.write('.')
        sys.stdout.write('\n')
    sys.stdout.write('\n')
    #input('press enter to continue')
    return empty

def remove_dupes(dic):
    ''' Remove keys that have dupes in dic '''
    unique_values = set()
    values_to_remove = set()

    for value in dic.values():
        if value in unique_values:
            values_to_remove.add(value)
        else:
            unique_values.add(value)

    keys_to_remove = set()
    for key in dic.keys():
        if dic[key] in values_to_remove:
            keys_to_remove.add(key)

    for key in keys_to_remove:
        dic.pop(key)

# Add (x, y) tuples a and b
def p_add(a, b):
    return (a[0] + b[0], a[1] + b[1])

# Parse input
for y, line in enumerate(open(sys.argv[1]).read().rstrip().split('\n')):
    xs = [i for i, c in enumerate(line) if c == '#']
    #print(y, line, xs)
    for x in xs:
        elves.add((x, y))

# elf: one point
# directions: dirs_n, dirs_s, dirs_w or dirs_e
def can_move(elf, directions):
    for point in [p_add(elf, d) for d in directions]:
        if point in elves:
            return False
    return True

def do_round(rnd):
    try_moves = dict()
    anyone_moved = False
    for elf in elves:
        if can_move(elf, dirs):
            # Can move in all directions
            # is at rest, do nothing
            continue
        for r in range(rnd, rnd + 4):
            d = dirs_order[r % 4]
            if can_move(elf, d):
                # d[1] is straight
                try_moves[elf] = p_add(elf, d[1])
                break
    remove_dupes(try_moves)
    # The moves left in try_moves can move
    for elf, elfnew in try_moves.items():
        anyone_moved = True
        elves.remove(elf)
        elves.add(elfnew)

    return anyone_moved

#print_grid(elves)
for rnd in range(10):
    do_round(rnd)
    #print_grid(elves)

empty = print_grid(elves)
print('Part 1:', empty)

for rnd in range(10, 2000):
    moved = do_round(rnd)
    if not moved:
        break

print('Part 2:', rnd + 1)
