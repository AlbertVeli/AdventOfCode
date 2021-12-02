#!/usr/bin/env python3

import sys
sys.path.insert(0,'../')
from aoc_input import *

if len(sys.argv) != 2:
    print('Usage:', sys.argv[0], '<input.txt>')
    sys.exit(1)

ss = input_as_lines(sys.argv[1])
move = []
for s in ss:
    d, n = s.split()
    move.append((d, int(n)))

x = 0
y = 0

for d, n in move:
    if d == 'forward':
        x += n
    elif d == 'up':
        y -= n
    elif d == 'down':
        y +=n

print(x * y)

