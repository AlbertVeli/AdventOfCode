#!/usr/bin/env python3

import sys
sys.path.append('../..')
import aoc
import numpy as np

patterns = list(map(str.splitlines, aoc.input_string(sys.argv[1]).split('\n\n')))

# TODO: merge part 1 and part 2 into one file

def find_reflection(pattern):

    height = len(pattern)

    for i in range(1, height):
        # the reflective line can be either
        # a physical row or an imagined line
        # between two consecutive rows
        lower = pattern[: i]
        upper = pattern[i :]
        if i < height - i:
            upper = upper[: i]
        else:
            lower = lower[i - height :]

        # Check if upper and lower differ in exactly one element
        if np.count_nonzero((lower == upper[::-1]) == False) == 1:
            return i

    return 0

def count_reflection(pattern):
    pattern = np.array([list(s) for s in pattern])
    n = find_reflection(pattern) * 100
    if n > 0:
        return n
    return find_reflection(pattern.T)

vals = []
for pattern in patterns:
    print(pattern)
    n = count_reflection(pattern)
    print(n)
    vals.append(n)
print('Part 2:', sum(vals))