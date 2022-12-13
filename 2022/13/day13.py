#!/usr/bin/env python3

import sys
from functools import cmp_to_key

# Refactor of listcmp for use with sort
# Return:
#   -1 if in order
#    0 if equal
#    1 if not in order
def listcmp(left, right):
    # Compare each item in left
    # with corresponding item in right
    for i in range(len(left)):
        if len(right) < i + 1:
            # Right side ran out of items
            return 1
        l = left[i]
        r = right[i]
        if type(l) == int and type(r) == int:
            # Both are integers
            if l < r:
                return -1
            if l > r:
                return 1
        else:
            # Recursively call listcmp()
            if type(l) == int:
                l = [l]
            if type(r) == int:
                r = [r]
            res = listcmp(l, r)
            if res != 0:
                return res
    if len(left) < len(right):
        # Left side ran out of items
        return -1
    else:
        # No decision could be made
        return 0

# Part 1
a = open(sys.argv[1]).read().rstrip().split('\n\n')
ordered = []
for i, pair in enumerate(a):
    l1, l2 = pair.split('\n')
    l1 = eval(l1)
    l2 = eval(l2)
    res = listcmp(l1, l2)
    if res == -1:
        ordered.append(i + 1)
print('Part 1:', sum(ordered))

# Part 2
packets = [[[2]], [[6]]]
a = open(sys.argv[1]).read().rstrip().split('\n\n')
for pair in a:
    l1, l2 = pair.split('\n')
    packets.append(eval(l1))
    packets.append(eval(l2))
packets.sort(key = cmp_to_key(listcmp))
dividers = []
for i, p in enumerate(packets):
    if p == [[2]] or p == [[6]]:
        dividers.append(i + 1)
print('Part 2:', dividers[0] * dividers[1])
