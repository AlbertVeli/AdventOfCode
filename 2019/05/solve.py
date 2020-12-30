#!/usr/bin/env python3

# Solution refactored to use Intmachine in ../common
import sys
sys.path.insert(0,'../common')
from intmachine import Intmachine
from collections import deque

prog = []
for i in map(int, open(sys.argv[1]).readline().split(',')):
    prog.append(i)

# Create input/output queue
dqi = deque()
dqo = deque()

# Part 1, append 1. Change to 5 for part 2.
dqi.appendleft(1)

# Create machine and run it
machine = Intmachine('day5', prog, dqi, dqo)

while machine.do_op():
    pass

machine.dump_mem()

# Print output queue
while len(dqo) > 0:
    print(dqo.pop())
