#!/usr/bin/env python3

import sys

if len(sys.argv) != 2:
    print('Usage:', sys.argv[0], '<input.txt>')
    sys.exit(1)

def sign1(diff):
    if diff < 0:
        return -1
    elif diff > 0:
        return 1
    return 0

# ChatGPT improved version of new_pos
def new_pos(x0, y0, x1, y1):
    # Calculate the manhattan distance
    dist = abs(x0 - x1) + abs(y0 - y1)

    # Check if tail (x1, y1) should move
    if ((x0 == x1 or y0 == y1) and dist > 1) or dist > 2:
        return (x1 + sign1(x0 - x1), y1 + sign1(y0 - y1))
    else:
        return (x1, y1)

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
                h = knots[i - 1]
                t = knots[i]
                pos = list(new_pos(h[0], h[1], t[0], t[1]))
                # Stop moving if this knot didn't move
                if pos == t:
                    break
                else:
                    knots[i] = pos
            visited.add(tuple(knots[nknots - 1]))
    return len(visited)

# Part 1
print('Part 1:', run_knots(2))

# Part 2
print('Part 2:', run_knots(10))
