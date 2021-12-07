#!/usr/bin/env python3

import sys
sys.path.insert(0,'../')
from aoc_input import *
from numpy import inf

if len(sys.argv) != 2:
    print('Usage:', sys.argv[0], '<input.txt>')
    sys.exit(1)

a = input_as_line_of_ints(sys.argv[1])

# Part 1
least = inf
for i in range(min(a), max(a) + 1):
    cost = 0
    for pos in a:
        steps = abs(pos - i)
        cost += steps
    if cost < least:
        least = cost

print(least)

# Part 2
least = inf
for i in range(min(a), max(a) + 1):
    cost = 0
    for pos in a:
        steps = abs(pos - i)
        fuel = steps * (steps + 1) >> 1
        cost += fuel
    if cost < least:
        least = cost

print(least)

