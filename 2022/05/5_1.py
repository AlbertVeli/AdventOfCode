#!/usr/bin/env python3

import sys
import re
from collections import deque 


if len(sys.argv) != 2:
    print('Usage:', sys.argv[0], '<input.txt>')
    sys.exit(1)

def parseline(line):
    row = []
    for i in range(0, len(line), 4):
        element = line[i:i+3]
        if element.startswith('['):
            row.append(element[1])
        else:
            row.append('')
    return row

moves = []

a1, a2 = open(sys.argv[1]).read().rstrip().split('\n\n')

# Initial stacks
a1 = a1.split('\n')
# Number of stacks is last integer on line after initial stacks
nstacks = tuple(map(int, re.findall(r'(\d+)', a1.pop())))[-1]
stacks = []
for _ in range(nstacks):
    stacks.append(deque())
for line in a1:
    row = parseline(line)
    for i in range(len(row)):
        e = row[i]
        if e != '':
            stacks[i].appendleft(e)

# Moves
a2 = a2.split('\n')
for s in a2:
    moves.append(tuple(map(int, re.findall(r'(\d+)', s))))

# Start moving
for n, src, dst in moves:
    for i in range(n):
        e = stacks[src - 1].pop()
        stacks[dst - 1].append(e)

# Print result
res = ''
for s in stacks:
    res += s[-1]
print(res)
