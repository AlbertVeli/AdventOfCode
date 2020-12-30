#!/usr/bin/env python3

import sys
import typing

# Return list of ints from inputs, one integer per line
def read_input(fname: str) -> typing.List[int]:
    return list(map(int, open(fname).read().splitlines()))

a = read_input(sys.argv[1])
builtin = max(a) + 3
a.sort()
a.append(builtin)
j = 0
combs = {}
combs[j] = 1
for j in a:
    combs[j] = 0
    for j2 in range(j - 3, j):
        if j2 in combs:
            combs[j] += combs[j2]

print(combs)
print(combs[builtin])
