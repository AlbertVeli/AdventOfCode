#!/usr/bin/env python3

import sys

if len(sys.argv) != 2:
    print('Usage:', sys.argv[0], '<input.txt>')
    sys.exit(1)

def manhattan_distance(x0, y0, x1, y1):
    return abs(x0 - x1) + abs(y0 - y1)

def sign1(diff):
    if diff < 0:
        return -1
    return 1

def new_pos(x0, y0, x1, y1):
    if x0 == x1:
        if y0 - y1 > 1:
            # Down
            return ((x1, y1 + 1))
        elif y1 - y0 > 1:
            # Up
            return ((x1, y1 - 1))
        else:
            return((x1, y1))
    elif y0 == y1:
        if x0 - x1 > 1:
            # Right
            return ((x1 + 1, y1))
        elif x1 - x0 > 1:
            # Left
            return ((x1 - 1, y1))
        else:
            return((x1, y1))
    else:
        # Diagonal
        if manhattan_distance(x0, y0, x1, y1) <= 2:
            return((x1, y1))
        # Need to move, always diagonal
        dx = x0 - x1
        dy = y0 - y1
        return((x1 + sign1(dx), y1 + sign1(dy)))
 

def run_knots(nknots):
    knots = [[0, 0] for _ in range(nknots)]
    visited = set()
    for line in map(str.rstrip, open(sys.argv[1])):
        d, s = line.split(' ')
        s = int(s)
        for _ in range(s):
            # Move head
            knot = knots[0]
            if d == 'D':
                knot[1] += 1
            elif d == 'L':
                knot[0] -= 1
            elif d == 'R':
                knot[0] += 1
            elif d == 'U':
                knot[1] -= 1
            for i in range(1, nknots):
                knots[i] = list(new_pos(knots[i - 1][0], knots[i - 1][1], knots[i][0], knots[i][1]))
            visited.add(tuple(knots[nknots - 1]))
    return len(visited)

# Part 1
print('Part 1:', run_knots(2))

# Part 2
print('Part 2:', run_knots(10))
