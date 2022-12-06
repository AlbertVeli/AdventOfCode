#!/usr/bin/env python3

import sys

if len(sys.argv) != 2:
    print('Usage:', sys.argv[0], '<input.txt>')
    sys.exit(1)

# Find index of first n unique items in lst
def find_unique_n(lst, n):
    for i in range(n - 1, len(lst)):
        if len(set(lst[i - (n - 1) : i + 1])) == n:
            return i + 1
    return False

a = list(open(sys.argv[1]).read().rstrip())
print('Part 1:', find_unique_n(a, 4))
print('Part 2:', find_unique_n(a, 14))
