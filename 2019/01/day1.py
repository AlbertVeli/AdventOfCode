#!/usr/bin/env python3

import sys

ints = list(map(int, open(sys.argv[1])))

# Part 1
print(sum(map(lambda x: x // 3 - 2, ints)))

# Part 2
def calcfuel(f):
    total = 0
    while f > 0:
        f = f // 3 - 2
        if f > 0:
            total += f
    return total

print(sum(map(calcfuel, ints)))
