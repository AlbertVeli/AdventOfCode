#!/usr/bin/env python3

import sys
import re
from sympy import sympify

exprs = {}

for line in open(sys.argv[1]).read().rstrip().split('\n'):
    l, r = line.split(': ')
    # ignore humn
    if l != 'humn':
        exprs[l] = r

root = exprs.pop('root').split(' ')
root = [root[0], root[2]]

while True:
    # Set to true if at least one replacement
    replaced = False
    rexprs = exprs.copy()

    for l, r in exprs.items():
        if l in root:
            continue
        #print(l, '= ', r)
        rvals = re.findall('[a-z]{4}', r)
        lenrvals = len(rvals)
        if lenrvals == 0:
            replaced = True
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

    if replaced == False:
        # No new replacements, cant simplify any more
        break

# Now do the same but replace if humn is on right side
while True:
    replaced = False
    rexprs = exprs.copy()

    for l, r in exprs.items():
        #print(l, '= ', r)
        if l in root:
            continue
        if 'humn' in r:
            # Replace all l with r
            rexprs.pop(l)
            for rl, rr in rexprs.items():
                if l in rr:
                    replaced = True
                    rr = rr.replace(l, '(' + r + ')')
                    rr = str(sympify(rr))
                    rexprs[rl] = rr

    exprs = rexprs.copy()
    if not replaced:
        break

print('root:', root[0], '=', root[1])
vals = []
for l, r in exprs.items():
    r = str(sympify(r))
    print(l, '=', r)
    vals.append(r)
print('solve this with wolfram alpha')
s = vals[0] + ' = ' + vals[1]
print(s.replace('humn', 'x'))
