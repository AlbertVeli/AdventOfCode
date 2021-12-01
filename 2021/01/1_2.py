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
l = len(a)

for i in range(l - 2):
    summa = 0
    for j in range(i, i + 3):
        summa += a[j]
    if summa > prev:
        increase += 1
    prev = summa

print(increase)
