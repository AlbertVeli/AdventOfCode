#!/usr/bin/env python3

import sys
sys.path.append('../..')
import aoc
import re

lines = aoc.char_matrix(sys.argv[1])
for i, line in enumerate(lines):
    # add border of '.' around it
    lines[i] = '.' + ''.join(line) + '.'
# first and last line of '.'
m = ['.' * len(lines[0])] + lines + ['.' * len(lines[0])]

def adj_dots(x, y, x2):
    # TODO: Create list of coordinates
    # to check instead. Break this out
    # into a separate function and call
    # it from adj_dots and adj_nums.
    # Line above
    yy = y - 1
    for c in m[yy][x - 1 : x2 + 1]:
        if c != '.':
            return False
    # Left
    if m[y][x - 1] != '.' or m[y][x2] != '.':
        return False
    # Line below
    yy = y + 1
    for c in m[yy][x - 1 : x2 + 1]:
        if c != '.':
            return False

    return True

# Find number tuple at x, y in nums
def num(x, y):
    for xx, yy, x2 in nums:
        if y == yy and x >= xx and x < x2:
            return (xx, yy, x2)
    return False

# Find exactly 2 adjacent numbers
def adj_nums(x, y):
    # TODO: Make list of coordinates to
    # check and just do the
    # adjnums.append() in one place
    adjnums = []
    # Line above
    yy = y - 1
    for xx in range(x - 1, x + 2):
        if m[yy][xx].isdigit():
            n = num(xx, yy)
            if not n in adjnums:
                adjnums.append(n)
    # Left
    if m[y][x - 1].isdigit():
        n = num(x - 1, y)
        if not n in adjnums:
            adjnums.append(n)
    # Right
    if m[y][x + 1].isdigit():
        n = num(x + 1, y)
        if not n in adjnums:
            adjnums.append(n)

    # Line below
    yy = y + 1
    for xx in range(x - 1, x + 2):
        if m[yy][xx].isdigit():
            n = num(xx, yy)
            if not n in adjnums:
                adjnums.append(n)
    if len(adjnums) == 2:
        r = 1
        for xx, yy, x2 in adjnums:
            n = int(m[yy][xx : x2])
            r *= n
        return r
    return 0

nums = []
# search for integers in each line
sm = 0
for y, line in enumerate(m):
    for match in re.finditer (r'\d+', line):
        x = match.start()
        x2 = match.end()
        n = int(line[x : x2])
        # save number positions for part 2
        nums.append((x, y, x2))
        # part 1
        if not adj_dots(x, y, x2):
            sm += n

print('Part 1:', sm)

# part 2
sm = 0
for y, line in enumerate(m):
    pos = 0
    x = 0
    while x > -1:
        x = line.find('*', pos)
        if x >= 0:
            sm += adj_nums(x, y)
            pos = x + 1

print('Part 2:', sm)