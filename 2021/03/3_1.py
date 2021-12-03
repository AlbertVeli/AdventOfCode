#!/usr/bin/env python3

import sys
sys.path.insert(0,'../')
from aoc_input import *

if len(sys.argv) != 2:
    print('Usage:', sys.argv[0], '<input.txt>')
    sys.exit(1)
ss = input_as_lines(sys.argv[1])

l = len(ss[0])
# Xor mask to invert l bits
mask = int('1' * l, 2)

gamma = []
for i in range(l):
    zeros = 0
    ones = 0
    for s in ss:
        b = s[i]
        if b == '1':
            ones += 1
        else:
            zeros += 1
    if ones > zeros:
        gamma.append('1')
    else:
        gamma.append('0')

g = int(''.join(gamma), 2)
# Epsilon rate = bitwise inverse of gamma rate
e = g ^ mask
print(g, e, g * e)
