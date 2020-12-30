#!/usr/bin/env python3

import sys
import typing
from itertools import combinations

# Return list of ints from inputs, one integer per line
def read_input(fname: str) -> typing.List[int]:
    return list(map(int, open(fname).read().splitlines()))

if len(sys.argv) != 2:
    print('Usage:', sys.argv[0], '<input.txt>')
    sys.exit(1)

a = read_input(sys.argv[1])
for i1, i2 in combinations(a, 2):
    if i1 + i2 == 2020:
        print(i1, i2)
        print(i1 * i2)
