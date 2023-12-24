#!/usr/bin/env python3

import sys
sys.path.append('../..')
import aoc
from copy import deepcopy

text = open(sys.argv[1]).read().rstrip().split('\n\n')

# workflows[target] = [(condition, target), ...], else target
workflows = dict()
for line in text[0].split('\n'):
    name, rules = line.split('{')
    rules = rules[:-1].split(',')
    l = []
    for rule in rules:
        if ':' in rule:
            cond, target = rule.split(':')
            l.append((cond, target))
        else:
            # assume else target is always last
            workflows[name] = (l, rule)

# parts = [(x, m, a, s), ...]
parts = []
for line in text[1].split('\n'):
    parts.append(tuple(aoc.ints(line)))

ranges = {}
for rating in ['x', 'm', 'a', 's']:
    # narrow ranges later when we go through workflows
    ranges[rating] = (1, 4000)

def range_sz(ranges):
    sz = 1
    for range_min, range_max in ranges.values():
        sz *= range_max - range_min + 1
    return sz

def get_rating_op_val(cond):
    rating = cond[0]
    op = cond[1]
    val = int(cond[2:])
    return (rating, op, val)

# thanks William for the logic here, kthxbye
def n_ways(ranges, cur_workflow):
    # workflow[0] is list of filters
    # workflow[1] is else target
    conds = cur_workflow[0]

    n = 0

    cur_ranges = deepcopy(ranges)

    for cond, target in conds:
        rating, op, val = get_rating_op_val(cond)

        pass_ranges = deepcopy(cur_ranges)
        old_min, old_max = pass_ranges[rating]

        if op == '>':
            new_min = val + 1
            new_max = old_max
            fail_min = old_min
            fail_max = val
        else:
            # '<'
            new_max = val - 1
            new_min = old_min
            fail_min = val
            fail_max = old_max

        pass_ranges[rating] = (new_min, new_max)

        # n ways if we pass
        if new_min <= old_max:
            if target == 'A':
                n += range_sz(pass_ranges)
            elif target != 'R':
                # more targets
                n += n_ways(pass_ranges, workflows[target])

        # ranges if filter fail
        cur_ranges[rating] = (fail_min, fail_max)

    # n ways if all conds fail
    # else target
    target = cur_workflow[1]
    if target == 'A':
        n += range_sz(cur_ranges)
    elif target != 'R':
        n += n_ways(cur_ranges, workflows[target])

    return n

print(n_ways(ranges, workflows['in']))