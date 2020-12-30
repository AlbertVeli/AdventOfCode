#!/usr/bin/env python3

from itertools import permutations
from collections import deque
# intmachine is in ../common
import sys
sys.path.insert(0,'../common')
from intmachine import Intmachine

# Read program from stdin
prog = []
for i in map(int, input('').split(',')):
    prog.append(i)

# Create queues
queues = []
for _ in range(5):
    dq = deque()
    queues.append(dq)

# Create and connect machines
machines = []
for i in range(5):
    m = Intmachine('m' + str(i), prog, queues[i], queues[(i + 1) % 5])
    machines.append(m)

# task 1
# l = list(range(5))
# task 2
phases = list(range(5,10))

maxsig = 0
maxphase = 0
for phase in permutations(phases):
    for i in range(5):
        # Reset qs and machines for new run
        queues[i].clear()
        machines[i].reset()
        # Push phases to input queues
        queues[i].appendleft(phase[i])
    # Push startvalue 0 into first input queue
    queues[0].appendleft(0)

    # Run one op round robin on each machine
    # If starving for input, skip and continue, see intcode.py
    running = []
    for i in range(5):
        running.append(True)
    one_running = True
    while one_running:
        one_running = False
        for i in range(5):
            if running[i]:
                running[i] = machines[i].do_op()
                one_running = running[i]

    # print last output
    sig = queues[0].pop()
    if sig > maxsig:
        maxsig = sig
        maxphase = list(phase)

print(maxsig, maxphase)
