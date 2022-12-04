#!/usr/bin/env python3

import sys
import re

if len(sys.argv) != 2:
    print('Usage:', sys.argv[0], '<input.txt>')
    sys.exit(1)

subsets = 0
intersections = 0

for line in map(str.rstrip, open(sys.argv[1])):

    # list of integers on one line
    ints = list(map(int, re.findall(r'(\d+)', line)))

    s1 = set(range(ints[0], ints[1] + 1))
    s2 = set(range(ints[2], ints[3] + 1))

    if s1.issubset(s2) or s2.issubset(s1):
        subsets += 1

    if len(set.intersection(s1, s2)) > 0:
        intersections += 1

print(subsets)
print(intersections)

