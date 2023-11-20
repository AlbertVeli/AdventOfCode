#!/usr/bin/env python3

import sys
sys.path.append('../..')
import aoc
from collections import Counter

lines = aoc.lines(sys.argv[1])
# Create a matrix as a list of sublists
# [['e', 'e', 'd', 'a', 'd', 'n'], ['d', 'r', 'v', 't', 'e', 'e'], ...]
matrix = [list(x) for x in lines]
# transpose matrix
t_m = [list(group) for group in zip(*matrix)]

# count the most common letter
# if two are equal sort in alphabetical order
# key = lambda x: (-x[1], x[0]) gives sorting order
# of the tuple values, most common count first -x[1]
# then alphabetical order for equal count x[0]
sys.stdout.write('part 1: ')
for column in t_m:
    c = Counter(column)
    letter = sorted(c.most_common(), key=lambda x: (-x[1], x[0]))[0][0]
    sys.stdout.write(letter)
sys.stdout.write('\n')

sys.stdout.write('part 2: ')
for column in t_m:
    c = Counter(column)
    letter = sorted(c.most_common(), key=lambda x: (x[1], x[0]))[0][0]
    sys.stdout.write(letter)
sys.stdout.write('\n')