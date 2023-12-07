#!/usr/bin/env python3

import sys
sys.path.append('../..')
import aoc

line = aoc.input_string(sys.argv[1])
linelen = len(line)
halflen = linelen // 2
matches = []
for i in range(len(line)):
    c1 = line[i]
    i2 = (i + 1) % linelen
    c2 = line[i2]
    if c1 == c2:
        matches.append(int(c1))
print('Part 1:', sum(matches))

matches = []
for i in range(len(line)):
    c1 = line[i]
    i2 = (i + halflen) % linelen
    c2 = line[i2]
    if c1 == c2:
        matches.append(int(c1))
print('Part 2:', sum(matches))
