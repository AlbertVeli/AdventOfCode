#!/usr/bin/env python3

import sys
sys.path.append('../..')
import aoc

# part 1
a = aoc.lines_of_ints(sys.argv[1])
sm = 0
for l in a:
    s = ''.join(map(str, l))
    s2 = s[0] + s[-1]
    sm += int(s2)

print('Part 1:', sm)

# part 2
numdic = {'one' : 1, 'two' : 2, 'three' : 3, 'four' : 4, 'five' : 5, 'six' : 6, 'seven' : 7, 'eight' : 8, 'nine' : 9}
keys = numdic.keys()
nums = ['1', '2', '3', '4', '5', '6', '7', '8', '9']

def replace_subnums(s):
    """
    Replace subscrings that are in numdic. The keys may overlap.
    """
    result = []
    pos = 0
    while pos < len(s):
        m = None
        for key in keys:
            if s.startswith(key, pos):
                m = key
                break
        if m:
            result.append(str(numdic[m]))
        elif s[pos] in nums:
            result.append(s[pos])
        pos += 1
    return ''.join(result)

a = aoc.lines(sys.argv[1])
sm = 0
for l in a:
    s = replace_subnums(l)
    sm += int(s[0] + s[-1])

print('Part 2:', sm)