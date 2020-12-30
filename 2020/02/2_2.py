#!/usr/bin/env python3

import sys
import typing

# Return list of [(min, max), char, password]
def read_input(fname: str) -> typing.List[typing.List]:
    r = []
    for line in open(fname).read().splitlines():
        a = line.split()
        a[0] = tuple(map(int, a[0].split('-')))
        a[1] = a[1].replace(':', '')
        r.append(a)
    return r

if len(sys.argv) != 2:
    print('Usage:', sys.argv[0], '<input.txt>')
    sys.exit(1)

a = read_input(sys.argv[1])

valid = 0

for mm, c, s in a:
    #print(mm, c, s,)
    cnt = 0
    for i in mm:
        if s[i - 1] == c:
            cnt += 1
    if cnt == 1:
        valid += 1

print(valid)
