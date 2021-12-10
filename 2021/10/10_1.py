#!/usr/bin/env python3

import sys
sys.path.insert(0,'../')
from aoc_input import *

if len(sys.argv) != 2:
    print('Usage:', sys.argv[0], '<input.txt>')
    sys.exit(1)

a = input_as_lines(sys.argv[1])

score = { ')': 3, ']': 57, '}': 1197, '>': 25137 }

def check_line(line):
    #print(line)
    start = tuple('({[<')
    stop = tuple(')}]>')
    map = dict(zip(start, stop))
    queue = []

    for c in line:
        if c in start:
            queue.append(map[c])
        elif c in stop:
            if not queue:
                #print('Queue empty, got', i)
                return 0
            else:
                paren = queue.pop()
                if c != paren:
                    #print('Wrong close', c, paren)
                    return score[c]
    if not queue:
        #print('Balanced')
        return 0

    #print('Unfinished, remaining queue:', queue)
    return 0

sm = 0
for line in a:
    sm += check_line(line)
print(sm)
