#!/usr/bin/env python3

import sys

# Tip: look at day 7, intcode.py for a general intcode machine.

prog = list(map(int, open(sys.argv[1]).readline().split(',')))

def run_prog(noun, verb):
    mem = list(prog)
    mem[1] = noun
    mem[2] = verb

    pc = 0
    op = 0
    while op != 99:
        op = mem[pc]
        if op == 99:
            return mem[0]
        pc += 1
        a, b, c = mem[pc : pc + 3]
        pc += 3
        if op == 1:
            res = mem[a] + mem[b]
        elif op == 2:
            res = mem[a] * mem[b]
        else:
            print('illegal op %d at pos %d' % op, pc - 4)
            sys.exit(1)
        mem[c] = res

for noun in range(100):
    for verb in range(100):
        res = run_prog(noun, verb)
        if res == 19690720:
            print(100 * noun + verb)
            sys.exit(0)
