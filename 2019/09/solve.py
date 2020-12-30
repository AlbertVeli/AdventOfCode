#!/usr/bin/env python3

from itertools import permutations
from collections import deque
# Use intmachine from ../common
import sys
sys.path.insert(0,'../common')
from intmachine import Intmachine

# Read program from stdin
prog = []
for i in map(int, input('').split(',')):
    prog.append(i)

# Create queues
queues = []
for _ in range(2):
    dq = deque()
    queues.append(dq)

# Create and connect machines
m = Intmachine('d9', prog, queues[0], queues[1])
m.reset()
# push single input
# task 1, push 1
# m.push(1)
# task 2, push 2
m.push(2)
while m.do_op():
    pass

# print output queue
while len(m.oq) > 0:
    print(m.pop())
