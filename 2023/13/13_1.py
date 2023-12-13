#!/usr/bin/env python3

import sys
sys.path.append('../..')
import aoc
import numpy as np

patterns = list(map(str.splitlines, aoc.input_string(sys.argv[1]).split('\n\n')))

def find_reflection(pattern):
    height = len(pattern)
    width = len(pattern[0])
    pattern = np.array([list(s) for s in pattern])

    # horizontal
    for y in range(height - 1):
        # Reflective row
        y1 = y - 1
        y2 = y + 1
        if y > 0:
            found = True
            while y1 >= 0 and y2 < height:
                if not np.array_equal(pattern[y1, :], pattern[y2, :]):
                    found = False
                    break
                y1 -= 1
                y2 += 1
            if found:
                return (y + 1) * 100
        # "even" rows
        y1 = y
        y2 = y + 1
        found = True
        while y1 >= 0 and y2 < height:
            if not np.array_equal(pattern[y1, :], pattern[y2, :]):
                found = False
                break
            y1 -= 1
            y2 += 1
        if found:
            return (y + 1) * 100

    # vertical
    for x in range(width - 1):
        # Reflective column
        x1 = x - 1
        x2 = x + 1
        if x > 0:
            found = True
            while x1 >= 0 and x2 < width:
                if not np.array_equal(pattern[:, x1], pattern[:, x2]):
                    found = False
                    break
                x1 -= 1
                x2 += 1
            if found:
                return x + 1
        # "even" columns
        x1 = x
        x2 = x + 1
        found = True
        while x1 >= 0 and x2 < width:
            if not np.array_equal(pattern[:, x1], pattern[:, x2]):
                found = False
                break
            x1 -= 1
            x2 += 1
        if found:
            return x + 1

    # Should not get here
    return 0

vals = []
for pattern in patterns:
    print(pattern)
    n = find_reflection(pattern)
    print(n)
    vals.append(n)
print('Part 1:', sum(vals))
