#!/usr/bin/env python3

import sys

def overlap(a, b):
    return any(a[y][x] == '#' and b[y][x] == '#' for y in range(len(a)) for x in range(len(a[0])))

# Main

with open(sys.argv[1]) as f:
    lines = f.read().splitlines()
# Split blocks on empty lines
blocks = [block.split('\n') for block in '\n'.join(lines).split('\n\n')]

# Lock blocks begin with '#####'
# Key blocks begin with '.....'
locks = []
keys = []
for block in blocks:
    if block[0] == '#####':
        locks.append(block[1:])
    else:
        keys.append(block[1:])

# Count the number of keys that fit in any lock
fits = 0
for lock in locks:
    for key in keys:
        if not overlap(lock, key):
            fits += 1
print('Part 1:', fits)
