#!/usr/bin/env python3

import sys
# notgameboy.py in ../common
sys.path.insert(0,'../common')
from notgameboy import Notgameboy

prog = []

# Read program to list of tuples (instr, int operand)
for line in open(sys.argv[1]).read().splitlines():
    line = line.rstrip().split()
    prog.append((line[0], int(line[1])))

gb = Notgameboy(prog)

# part 1
while True:
    gb.do_op()
    if gb.loop:
        break
print(gb.acc)

# part 2
def change(i):
    global prcopy
    # change one nop -> jmp or jmp -> nop
    while True:
        if prcopy[i][0] == 'jmp':
            prcopy[i] = ('nop', prog[i][1])
            break
        if prcopy[i][0] == 'nop':
            prcopy[i] = ('jmp', prog[i][1])
            break
        i += 1
    #print('changed', i, prcopy[i])
    return i + 1

i = 0
while True:
    prcopy = list(prog)
    i = change(i)
    gb = Notgameboy(prcopy)
    while True:
        gb.do_op()
        if gb.loop:
            break
        elif gb.finished:
            print(gb.acc)
            sys.exit(0)

