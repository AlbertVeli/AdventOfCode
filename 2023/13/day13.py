#!/usr/bin/env python3

import sys
sys.path.append('../..')
import aoc
import numpy as np

patterns = list(map(str.splitlines, aoc.input_string(sys.argv[1]).split('\n\n')))

def is_reflective(pattern, i):
    height = len(pattern)
    # smallest number of rows, upper or lower
    # part of pattern split at row i
    n_rows = sorted([i, height - i])[0]
    lower = pattern[i - n_rows : i]
    upper = pattern[i : i + n_rows]
    # reverse order of upper rows, for comparison
    upper = upper[::-1]
    # This is the only part that differs between
    # part 1 and 2
    if part1:
        diff_wanted = 0
    else:
        diff_wanted = 1
    if np.sum(upper != lower) == diff_wanted:
        return True
    return False

def find_reflection(pattern):

    height = len(pattern)

    for i in range(1, height):
        if is_reflective(pattern, i):
            return i
    return 0

def score_reflection(pattern):
    pattern = np.array([list(s) for s in pattern])
    n = find_reflection(pattern) * 100
    if n > 0:
        return n
    return find_reflection(pattern.T)

part1 = True
vals = []
for pattern in patterns:
    n = score_reflection(pattern)
    vals.append(n)
print('Part 1:', sum(vals))

# part2
part1 = False
vals = []
for pattern in patterns:
    n = score_reflection(pattern)
    vals.append(n)
print('Part 2:', sum(vals))