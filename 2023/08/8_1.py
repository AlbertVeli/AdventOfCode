#!/usr/bin/env python3

import sys
sys.path.append('../..')
import aoc
import re

lines = aoc.lines(sys.argv[1])

lr = lines[0]
d = dict()
for line in lines[2:]:
    strings = re.findall(r'[A-Z0-9]+', line)
    d[strings[0]] = (strings[1], strings[2])

i = 0
length = len(lr)
cur = 'AAA'
while True:
    t = d[cur]
    dir = lr[i % length]
    if dir == 'L':
        cur = t[0]
    else:
        cur = t[1]
    i = i + 1
    if cur == 'ZZZ':
        break

print('Part 1:', i)