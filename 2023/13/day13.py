#!/usr/bin/env python3

import sys
sys.path.append('../..')
import aoc
import numpy as np

patterns = list(map(str.splitlines, aoc.input_string(sys.argv[1]).split('\n\n')))

def is_reflective(pattern, i, part2):
    height = len(pattern)
    # smallest number of rows when pattern
    # is split at row i
    n_rows = sorted([i, height - i])[0]
    lower = pattern[i - n_rows : i]
    upper = pattern[i : i + n_rows]
    # reverse order of upper rows, for comparison
    upper = upper[::-1]
    # This is the only part that differs between
    # part 1 and 2
    if part2:
        diff_wanted = 1
    else:
        diff_wanted = 0
    if np.sum(upper != lower) == diff_wanted:
        return True
    return False

def find_reflection(pattern, part2):

    height = len(pattern)

    for i in range(1, height):
        if is_reflective(pattern, i, part2):
            return i
    return 0

def score_reflection(pattern, part2 = False):
    pattern = np.array([list(s) for s in pattern])
    n = find_reflection(pattern, part2) * 100
    if n > 0:
        return n
    return find_reflection(pattern.T, part2)

vals1 = []
vals2 = []
for pattern in patterns:
    vals1.append(score_reflection(pattern))
    vals2.append(score_reflection(pattern, part2 = True))
print('Part 1:', sum(vals1))
print('Part 2:', sum(vals2))