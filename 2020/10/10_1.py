#!/usr/bin/env python3

import sys
import typing

# Return list of ints from inputs, one integer per line
def read_input(fname: str) -> typing.List[int]:
    return list(map(int, open(fname).read().splitlines()))

a = read_input(sys.argv[1])
builtin = max(a) + 3
a.append(builtin)
j = 0
diffs = {}
while True:
    l = [t for t in a if t > j and t <= j + 3]
    if len(l) == 0:
        break
    j2 = min(l)
    # a = list(l)
    d = j2 - j
    if d in diffs:
        diffs[d] += 1
    else:
        diffs[d] = 1
    print(j, j2, d)
    j = j2
# built in adapter
diffs[3]

print(diffs)
print(diffs[1] * diffs[3])
