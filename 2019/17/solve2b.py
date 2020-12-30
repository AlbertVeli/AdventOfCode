#!/usr/bin/env python3

# Use output from solve2a.py, manually
# sorted into groups A, B and C. See group.txt.
data = ''
# Main routine
data += 'A,A,B,C,C,A,B,C,A,B\n'
# Function A
data += 'L,12,L,12,R,12\n'
# Function B
data += 'L,8,L,8,R,12,L,8,L,8\n'
# Function C
data += 'L,10,R,8,R,12\n'
# Continuous video feed
data += 'n\n'

import numpy as np
from collections import deque
# Use intmachine from ../common
import sys
sys.path.insert(0,'../common')
from intmachine import Intmachine

# Read program from input.txt
with open('input.txt') as f:
    line = f.readline()
prog = []
for i in map(int, line.split(',')):
    prog.append(i)

# Create queues
queues = []
for _ in range(2):
    dq = deque()
    queues.append(dq)

# Create and connect machines
m = Intmachine('d17', prog, queues[0], queues[1])
m.reset()

# Push all data to input queue
for c in data:
    m.push(ord(c))

# Write 2 to position 0
m.poke(0, 2)

while m.do_op():
    # Write data as it becomes available.
    # But don't write last value in queue.
    while len(m.oq) > 1:
        sys.stdout.write(chr(m.pop()))

# Write anything left in output queue
while len(m.oq) > 1:
    sys.stdout.write(chr(m.pop()))
print(m.pop())
