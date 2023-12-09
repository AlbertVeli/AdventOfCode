#!/usr/bin/env python3

import sys
sys.path.append('../..')
import aoc
import copy

a = aoc.lines_of_ints(sys.argv[1])

# Return list of differences of nums.
# One shorter than nums.
def get_diff(nums):
    l = []
    for i in range(len(nums) - 1):
        l.append(nums[i + 1] - nums[i])
    return (l, all(e == 0 for e in l))

# Get last number according to algorithm
# in task text (first number for part 2).
def get_last(nums, part2):
    l, z = get_diff(nums)
    ls = [copy.deepcopy(nums)]
    ls.append(l)
    while not z:
        l, z = get_diff(l)
        ls.append(l)
    ll = len(ls)
    ls[ll - 1].append(0)
    for i in range(ll - 2, -1, -1):
        if part2:
            ls[i].insert(0, ls[i][0] - ls[i + 1][0])
        else:
            ls[i].append(ls[i + 1][-1] + ls[i][-1])

    if part2:
        return ls[0][0]

    return ls[0][-1]

lasts = []
lasts2 = []
for i in range(len(a)):
    lasts.append(get_last(a[i], False))
    lasts2.append(get_last(a[i], True))

print('Part 1:', sum(lasts))
print('Part 2:', sum(lasts2))