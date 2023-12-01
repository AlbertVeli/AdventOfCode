#!/usr/bin/env python3

import sys
sys.path.append('../..')
import aoc
import re

def decompress(s):
    rs = ''
    i = 0
    changed = False
    while True:
        m = pattern.search(s[i:])
        if m:
            offset = m.start()
            rs += s[i : i + offset]
            offset2 = s[i + offset:].find(')')
            repoffs = i + offset + offset2 + 1
            length = int(m.group(1))
            repn = int(m.group(2))
            reps = s[repoffs : repoffs + length]
            for _ in range(repn):
                rs += reps
            i = repoffs + length
            changed = True
        else:
            # No more decompressions, add last part
            rs += s[i:]
            break
    return (rs, changed)

# part 1
pattern = re.compile(r'\((\d+)x(\d+)\)')
line = aoc.input_string(sys.argv[1])
d = decompress(line)
print('Part 1:', len(d[0]))

# part 2, continue to decompress
# this doesn't work on the real input
# the string becomes too long
# TODO: count how long the length would
# become instead and dont actually decompress
while d[1]:
    d = decompress(d[0])
    print(len(d[0]))
print('Part 2:', len(d[0]))