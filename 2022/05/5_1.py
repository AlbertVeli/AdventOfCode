#!/usr/bin/env python3

import sys
import re
from collections import deque 


if len(sys.argv) != 2:
    print('Usage:', sys.argv[0], '<input.txt>')
    sys.exit(1)

# TODO: Refactor parsing of input, this is ugly

def parseline(line):
    row = []
    for i in range(0, len(line), 4):
        element = line[i:i+3]
        if element.startswith('['):
            row.append(element[1])
        else:
            row.append('')
    return row

stacking = True
rows = []
moves = []
for line in map(str.rstrip, open(sys.argv[1])):

    if stacking:
        # Build up the stacks
        if line.startswith(' 1'):
            stacking = False
            continue
        rows.append(parseline(line))
    else:
        # Moves
        move = tuple(map(int, re.findall(r'(\d+)', line)))
        if len(move) > 0:
            moves.append(move)
nstacks = max([len(r) for r in rows])
stacks = []
for _ in range(nstacks):
    stacks.append(deque())

for row in rows:
    for i in range(len(row)):
        e = row[i]
        if e != '':
            stacks[i].appendleft(e)

# Start moving

#print(stacks)

for n, src, dst in moves:
    for i in range(n):
        e = stacks[src - 1].pop()
        stacks[dst - 1].append(e)
    #print(stacks)

res = ''
for s in stacks:
    res += s[-1]
print(res)
