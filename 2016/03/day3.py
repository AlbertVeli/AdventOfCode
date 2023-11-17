#!/usr/bin/env python3

import sys
sys.path.append('../..')
import aoc

def valid(triangle):
    a, b, c = sorted(triangle)
    if a == b == c or a + b <= c:
        return False
    return True

triangles = aoc.lines_of_ints(sys.argv[1])
valids = list(map(valid, triangles))
print('part 1:', valids.count(True))

# Part 2, transpose the input in a strange way
transposed = []
# The zip expression transposes an array
for column in [list(group) for group in zip(*triangles)]:
    # Loop and split column list into sublists of length 3
    for sublist in [column[i:i+3] for i in range(0, len(column), 3)]:
        transposed.append(sublist)

print('part 2:', list(map(valid, transposed)).count(True))