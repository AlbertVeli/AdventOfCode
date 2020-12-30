#!/usr/bin/env python3

import sys

pubkeys = list(map(int, open(sys.argv[1]).read().splitlines()))

n = 20201227

# This is actually the discrete logarithm problem
# 7**x mod n
def crack(pubkey):
    loops = 0
    val = 1
    while val != pubkey:
        val = (val * 7) % n
        loops += 1
    return loops

# Comment out crack2() if you don't have sympy installed
# and call crack() instead in the loop below
from sympy.ntheory.residue_ntheory import discrete_log
def crack2(pubkey):
    return discrete_log(n, pubkey, 7)

privkeys = []
for key in pubkeys:
    loopsize = crack2(key)
    privkeys.append(loopsize)
    print(key, loopsize)

print(pow(pubkeys[0], privkeys[1], n))
print(pow(pubkeys[1], privkeys[0], n))
