#!/usr/bin/env python3

import sys
sys.path.insert(0,'../')
from aoc_input import *

if len(sys.argv) != 2:
    print('Usage:', sys.argv[0], '<input.txt>')
    sys.exit(1)

a = input_as_ints(sys.argv[1])

prev = 999999
increase = 0

for i in a:
    if i > prev:
        increase += 1
    prev = i

print(increase)
