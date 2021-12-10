#!/usr/bin/env python3

import sys
sys.path.insert(0,'../')
from aoc_input import *

if len(sys.argv) != 2:
    print('Usage:', sys.argv[0], '<input.txt>')
    sys.exit(1)

a = input_as_lines(sys.argv[1])

score = { ')': 1, ']': 2, '}': 3, '>': 4 }

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
                #print('Queue empty, got', c)
                return 0
            else:
                paren = queue.pop()
                if c != paren:
                    #print('Wrong close', c, paren)
                    return 0
    if not queue:
        #print('Balanced')
        return 0

    #print('Unfinished, remaining queue:', queue)
    sm = 0
    while queue:
        sm = 5 * sm + score[queue.pop()]
    return sm

scores = []
for line in a:
    sc = check_line(line)
    if sc > 0:
        scores.append(sc)
l = len(scores)
#print(l)
scores = sorted(scores)
print(scores[l // 2])
