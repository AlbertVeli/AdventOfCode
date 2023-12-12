#!/usr/bin/env python3

import sys
sys.path.append('../..')
import aoc
from itertools import product

lines = aoc.lines(sys.argv[1])
springs = []
for line in lines:
    line = line.split(' ')
    # groups separated by one ore more .
    line[0] = list(filter(None, line[0].split('.')))
    # counts
    line[1] = tuple(aoc.ints(line[1]))
    springs.append(line)

bintochar = { 0: '.', 1: '#' }

def get_group_combinations(s):
    ixs = [i for i, c in enumerate(s) if c == '?']
    n = len(ixs)
    if n == 0:
        return [s]
    combs = []
    for t in product((0, 1), repeat = n):
        # rs = replaced string
        rs = s
        for i, digit in enumerate(t):
            ix = ixs[i]
            rs = rs[:ix] + bintochar[digit] + rs[ix+1:]
        combs.append(rs)
    return combs

def count_hashes(s):
    groups = []
    count = 0
    for c in s:
        if c == '#':
            count += 1
        else:
            if count > 0:
                groups.append(count)
                count = 0
    if count > 0:
        groups.append(count)
    return tuple(groups)

arrangements = []

for groups, counts in springs:
    n = 0
    combs = []
    for g in groups:
        sl = get_group_combinations(g)
        combs.append(sl)
    for comb in product(*combs):
        s = '.'.join(comb)
        t = count_hashes(s)
        if t == counts:
            n += 1
    arrangements.append(n)
    #print(groups, n)
print('Part 1:', sum(arrangements))