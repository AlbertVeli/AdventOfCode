#!/usr/bin/env python3

import sys
sys.path.append('../..')
import aoc
import re

lines = aoc.lines(sys.argv[1])
for i, line in enumerate(lines):
    # add border of '.' around it
    lines[i] = '.' + line + '.'
# first and last line of '.'
m = ['.' * len(lines[0])] + lines + ['.' * len(lines[0])]

def adj_coords(x, y, x2):
    coords = []
    # above
    for xx in range(x - 1, x2 + 1):
        coords.append((xx, y - 1))
    # left, right
    coords.append((x - 1, y))
    coords.append((x2, y))
    # below
    for xx in range(x - 1, x2 + 1):
        coords.append((xx, y + 1))
    return coords

# return True if all adjacent coordinates are '.'
def adj_dots(x, y, x2):
    for xx, yy in adj_coords(x, y, x2):
        if m[yy][xx] != '.':
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
    adjnums = []
    for xx, yy in adj_coords(x, y, x + 1):
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