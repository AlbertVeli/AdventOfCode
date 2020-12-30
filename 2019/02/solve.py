#!/usr/bin/env python3

import sys

# Tip: look at day 7, intcode.py for a general intcode machine.

arr = list(map(int, open(sys.argv[1]).readline().split(',')))

arr[1] = 12
arr[2] = 2

pc = 0
op = 0
while op != 99:
    op = arr[pc]
    if op == 99:
        #print(arr)
        print(arr[0])
        sys.exit(0)
    pc += 1
    a, b, c = arr[pc : pc + 3]
    pc += 3
    if op == 1:
        res = arr[a] + arr[b]
    elif op == 2:
        res = arr[a] * arr[b]
    else:
        print('illegal op %d at pos %d' % op, pc - 4)
        exit(1)
    arr[c] = res
