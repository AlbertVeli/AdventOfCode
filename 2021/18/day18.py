#!/usr/bin/env python3

import sys
sys.path.insert(0,'../')
from aoc_input import *
from itertools import permutations

if len(sys.argv) != 2:
    print('Usage:', sys.argv[0], '<input.txt>')
    sys.exit(1)

def flatten(s):
    ret = []
    level = 0
    for c in s:
        if c == '[':
            level += 1
        elif c == ']':
            level -= 1
        elif c == ',':
            continue
        else:
            # single digit
            ret.append((int(c), level))
    return ret

# To explode a pair, the pair's left value is added to the first regular number
# to the left of the exploding pair (if any), and the pair's right value is added
# to the first regular number to the right of the exploding pair (if any).
def explode(n):
    length = len(n)
    for i in range(length):
        lval, depth = n[i]
        if depth > 4:
            rval = n[i + 1][0]
            if i > 0:
                prevval, prevdepth = n[i - 1]
                n[i - 1] = (prevval + lval, prevdepth)
            if i + 2 < length:
                nval, ndepth = n[i + 2]
                n[i + 2] = (nval + rval, ndepth)
            n[i : i + 2] = [(0, depth - 1)]
            # Exploded
            return True
    # Did not explode
    return False

# To split a regular number, replace it with a pair;
# the left element of the pair should be the regular number divided by two and rounded down,
# while the right element of the pair should be the regular number divided by two and rounded up.
# For example, 10 becomes [5,5], 11 becomes [5,6], 12 becomes [6,6], and so on.
def split(n):
    for i in range(len(n)):
        value, depth = n[i]
        if value >= 10:
            # Split
            floor = value // 2
            if value & 1:
                # round up
                ceil = floor + 1
            else:
                ceil = floor
            n[i : i + 1] = (floor, depth + 1), (ceil, depth + 1)
            return True
    return False


def add(l1, l2):
    #print('add', l1, 'and', l2)
    l = []
    for val, level in l1 + l2:
        l.append((val, level + 1))
    while True:
        if not explode(l):
            if not split(l):
                return l

# The magnitude of a pair is 3 times the magnitude of its left element
# plus 2 times the magnitude of its right element.
# The magnitude of a regular number is just that number.
def mag(l):
    while True:
        for i in range(len(l) - 1):
            v1, d1 = l[i]
            v2, d2 = l[i + 1]
            if d1 == d2:
                # depths equal
                l[i : i + 2] = [(3 * v1 + 2 * v2, d2 - 1)]
                break
        else:
            break
    return l[0][0]

def magnitude(l):
    newl = l[0]
    for e in l[1:]:
        # add does the exploding and splitting
        newl = add(newl, e)
    return mag(newl)

a = input_as_lines(sys.argv[1])
fl = []
for line in a:
    fl.append(flatten(line))


print('part 1:', magnitude(fl))

mags = []
for p1, p2 in permutations(fl, 2):
    mags.append(magnitude([p1] + [p2]))

print('part 2:', max(mags))
