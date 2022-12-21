#!/usr/bin/env python3

import sys
import re

exprs = {}

for line in open(sys.argv[1]).read().rstrip().split('\n'):
    l, r = line.split(': ')
    exprs[l] = r

while True:
    # check if we have root
    rvals = re.findall('[a-z]{4}', exprs['root'])
    if len(rvals) == 0:
        break
    # Else do one round of replacements
    rexprs = exprs.copy()
    for l, r in exprs.items():
        #print(l, '= ', r)
        rvals = re.findall('[a-z]{4}', r)
        if len(rvals) == 0:
            # r is a single number or number operator number
            # remove l from rexprs
            rval = rexprs.pop(l)
            # assert rval == r
            # In case it is an operation, eval it
            if len(rval.split(' ')) > 1:
                rval = str(eval(rval))
            # loop through rexprs
            # and replace mentions of l
            # with rval in items
            for rl, rr in rexprs.items():
                rrvals = re.findall('[a-z]{4}', rr)
                if l in rrvals:
                    rr = rr.replace(l, rval)
                    rexprs[rl] = rr
    exprs = rexprs.copy()

print(exprs)
print(eval(exprs['root']))
