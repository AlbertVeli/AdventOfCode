#!/usr/bin/env python3

# I failed at this task, looked at the solution
# megathread on reddit and found one solution with
# pyformlang so I decided to try it out. I never
# used pyformlang before and most of the algorithm
# is from the reddit solution.

from pyformlang.cfg import Production, Variable, Terminal, CFG
import re
import sys

# Variables
vrs = set()
# Productions
prods = set()
# Regexes
ints_re = re.compile(r'([0-9]+)')
rule_re = re.compile(r'^[0-9]')

messages = []
for line in open(sys.argv[1]).read().rstrip().splitlines():
    # rules
    if rule_re.match(line):
        line = line.split(':')
        rule_no = line[0]
        vrs.add(Variable(rule_no))
        if '"' in line[1]:
            # Terminal rule (a or b)
            t = line[1].strip().replace('"', '')
            print('add terminal', rule_no, t)
            prods.add(Production(Variable(rule_no), [Terminal(t)]))
        else:
            # Production rule (with or without |)
            for sub in line[1].split('|'):
                vs = ints_re.findall(sub)
                print('add variables', rule_no, vs)
                prods.add(Production(Variable(rule_no), [Variable(var) for var in vs]))
    else:
        # messages
        messages.append(line)

ta = Terminal('a')
tb = Terminal('b')

cfg = CFG(vrs, {ta, tb}, Variable('0'), prods)
n = 0
for m in messages:
    if cfg.contains(m):
        n += 1
print(n)
