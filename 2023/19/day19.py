#!/usr/bin/env python3

import sys
sys.path.append('../..')
import aoc

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

def next_target(target, part):
    # x, m, a, s are used by eval(cond)
    x, m, a, s = part
    conds, elsetarget = workflows[target]
    for cond, condtarget in conds:
        if eval(cond):
            return condtarget
    return elsetarget

def do_part(part):
    target = 'in'
    #print(part, ': ', end='')
    while target != 'R' and target != 'A':
        #print(target, ' -> ', end='')
        target = next_target(target, part)
    #print(target)
    return target

accepted = []
for part in parts:
    target = do_part(part)
    if target == 'A':
        accepted.append(part)

print('Part 1:', sum([sum(part) for part in accepted]))