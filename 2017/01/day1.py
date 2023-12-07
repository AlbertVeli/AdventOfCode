#!/usr/bin/env python3

import sys
sys.path.append('../..')
import aoc

line = aoc.input_string(sys.argv[1])
linelen = len(line)

def run_part(offset):
    matches = []
    for i in range(linelen):
        c1 = line[i]
        i2 = (i + offset) % linelen
        c2 = line[i2]
        if c1 == c2:
            matches.append(int(c1))
    return sum(matches)

print('Part 1:', run_part(1))
print('Part 2:', run_part(linelen // 2))
