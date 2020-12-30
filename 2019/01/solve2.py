#!/usr/bin/env python3

import sys

def calcfuel(f):
    total = 0
    while f > 0:
        f = f // 3 - 2
        if f > 0:
            total += f
    return total

s = 0
for line in sys.stdin:
    s += calcfuel(int(line))

print(s)
