#!/usr/bin/env python3

import sys
sys.path.append('../..')
import aoc

l = aoc.line_of_letterints(sys.argv[1])

x = 0
y = 0
dirs = [(0, -1), (1, 0), (0, 1), (-1, 0)]
curdir = 0

visited = [(0, 0)]
twice = None

for turn, dist in l:
    if turn == 'R':
        curdir += 1
    else:
        curdir -= 1
    curdir %= 4

    for _ in range(dist):    
        x += dirs[curdir][0]
        y += dirs[curdir][1]
        if twice:
            continue
        if not (x, y) in visited:
            visited.append((x, y))
        else:
            twice = (x, y)

print('part 1:', str(abs(x) + abs(y)))
print('part 2:', str(abs(twice[0]) + abs(twice[1])))