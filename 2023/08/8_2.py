#!/usr/bin/env python3

import sys
sys.path.append('../..')
import aoc
import re
import math

lines = aoc.lines(sys.argv[1])

lr = lines[0]
d = dict()
for line in lines[2:]:
    caps = re.findall(r'[A-Z0-9]+', line)
    d[caps[0]] = (caps[1], caps[2])

length = len(lr)

starts = []
for k in d.keys():
    if k[2] == 'A':
        starts.append(k)
ls = len(starts)

# Assume steps until node '..Z' is cyclic.
# Return cycle length.
def cycle_len(node):
    i = 0
    while True:
        t = d[node]
        dir = lr[i % length]
        if dir == 'L':
            node = t[0]
        else:
            node = t[1]
        i = i + 1
        if node[2] == 'Z':
            break
    return i

# Full disclosure, this lcm
# function was generated by bing chat.
# But I could have just googled it, baby.
def lcm(numbers):
    return math.lcm(*numbers)

cycles = []
for i in range(ls):
    cycles.append(cycle_len(starts[i]))

# Answer should be least common multiple of
# all cycles, assuming all steps are cyclic,
# which they seem to be. Thanks, William!
print('Part 2:', lcm(cycles))