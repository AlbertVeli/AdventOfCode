#!/usr/bin/env python3

# My solution from part 1 was too slow for part 2
# can't keep entire list in memory, use dictionary instead

import sys

inp = list(map(int, open(sys.argv[1]).readline().rstrip().split(',')))
last = {}
for i in inp:
    last[i] = inp.index(i)
#print(last)
prev = inp[-1]
for turn in range(len(inp), 30000000):
    try:
        last_turn = last[prev]
    except:
        number = 0
    else:
        number = turn - last_turn - 1
    last[prev] = turn - 1
    prev = number
print(number)
