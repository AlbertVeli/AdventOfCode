#!/usr/bin/env python3

import sys
import typing
from itertools import combinations

if len(sys.argv) != 3:
    print('Usage:', sys.argv[0], '<input.txt>', 'preamble (5 or 25)')
    sys.exit(1)

# Return list of ints from inputs, one integer per line
def read_input(fname: str) -> typing.List[int]:
    return list(map(int, open(fname).read().splitlines()))

a = read_input(sys.argv[1])
preamble = int(sys.argv[2])

# part 1
for curri in range(preamble, len(a)):
    curr = a[curri]
    i = curri - preamble
    found = False
    for i1, i2 in combinations(a[i: i+preamble], 2):
        if i1 + i2 == curr:
            #print(curr, '=', i1, '+', i2)
            found = True
    if not found:
        err = curr
        break

print('part 1:', err)

# part 2
for n in range(2, len(a) - 1):
    for curri in range(len(a) - (n - 1)):
        curr = a[curri : curri + n]
        if sum(curr) == err:
            print('part 2,', n, ':', curr)
            print(min(curr), '+', max(curr), '=', min(curr) + max(curr))
            sys.exit(0)
