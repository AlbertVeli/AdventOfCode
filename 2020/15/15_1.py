#!/usr/bin/env python3

import sys
from collections import deque

inp = list(map(int, open(sys.argv[1]).readline().rstrip().split(',')))
dq = deque()
for i in inp:
    dq.appendleft(i)
turn = len(dq)
last = dq[0]

while turn < 2020:
    try:
        last = dq.index(last, 1)
    except:
        last = 0
    dq.appendleft(last)
    turn += 1
print(dq[0])
