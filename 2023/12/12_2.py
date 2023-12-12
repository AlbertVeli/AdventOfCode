#!/usr/bin/env python3

# Brute force from part 1 doesn't work
# Use @functools.cache to speed up a
# recursive function that eats one character
# at a time from the input line

import sys
sys.path.append('../..')
import aoc
from itertools import product
import functools

lines = aoc.lines(sys.argv[1])
springs = []
for line in lines:
    line = line.split(' ')
    line[0] = '?'.join([line[0]] * 5)
    line[1] = tuple(aoc.ints(line[1]))
    line[1] = line[1] * 5
    springs.append(line)

# Idea for this recursive function is from my son, William
@functools.cache
def n_arrangements(s, groups_left, group_sz):
    """
    s = what is left of input line
    groups_left = groups left (tuple)
    group_sz = current size of group in consumed line (s)
    """
    # base case for recursion
    if len(s) == 0:
        if len(groups_left) == 0 and group_sz == 0:
            # No groups left, it's a match
            return 1
        elif len(groups_left) == 1 and group_sz == groups_left[0]:
            # 1 group left the same size as current group, match
            return 1
        else:
            # No match
            return 0

    # consumed groups larger than groups left
    if len(groups_left) > 0 and group_sz > groups_left[0]:
        return 0
    # don't expect any more groups but I am in a group
    # I need group therapy
    elif len(groups_left) == 0 and group_sz > 0:
        return 0

    # all good so far
    n = 0

    spring = s[0]

    # If ? is # or if spring is # is the same case
    if spring == '#' or spring == '?':
        n += n_arrangements(s[1:], groups_left, group_sz + 1)

    # If ? is . or if spring is . is the same case
    if spring == '.' or spring == '?':
        if len(groups_left) > 0 and group_sz == groups_left[0]:
            n += n_arrangements(s[1:], groups_left[1:], 0)
        elif group_sz == 0:
            n += n_arrangements(s[1:], groups_left, 0)

    # so above ? will recurse 2 times while . or # will recurse
    # 1 time, each case consuming one input line (s) character

    return n

arrangements = []
for line, counts in springs:
    n = n_arrangements(line, counts, 0)
    print(line, n)
    arrangements.append(n)

print('Part 2:', sum(arrangements))