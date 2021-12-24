#!/usr/bin/env python3

from z3 import *

# From input.txt
abcs = [
   (1, 14, 12),
   (1, 15, 7),
   (1, 12, 1),
   (1, 11, 2),
   (26, -5, 4),
   (1, 14, 15),
   (1, 15, 11),
   (26, -13, 5),
   (26, -16, 3),
   (26, -8, 9),
   (1, 15, 2),
   (26, -8, 3),
   (26, 0, 3),
   (26, -4, 11)
]

"""
def try_list(l):
    for i in range(14):
        # Do block number i
        a, b, c = abcs[i]
        w = l[i]
        x = int((z % 26 + b) != w)
        z = z // a
        if x:
            z = z * 26 + w + c

    return z == 0
"""

def do_part(maximize):
    s = Optimize()
    z = 0
    val = 0

    for i in range(len(abcs)):
        a, b, c = abcs[i]
        w = Int('w{' + str(i) + '}')
        val = val * 10 + w
        s.add(And(w >= 1, w <= 9))
        z = If(z % 26 + b != w, (z / a) * 26 + w + c, z / a)
    s.add(z == 0)

    if maximize:
        s.maximize(val)
    else:
        s.minimize(val)

    if s.check() == sat:
        return s.model().eval(val)

    return False

print('Part 1:', do_part(True))
print('Part 2:', do_part(False))
