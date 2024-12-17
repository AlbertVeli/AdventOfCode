#!/usr/bin/env python3

from z3 import *

# I tried for 2 hours to get z3 to work
# until I finally gazed at my son's solution
# that also used z3 so this is based on how
# he used z3.

opt = Optimize()

# Find start value for A using symbolic variable s
s = BitVec('s', 64)

# Registers
A, B, C = s, 0, 0

# These instructions should result in initial A = 22817223
#instructions = [4,3,7,1,5,3,0,5,4]
instructions = [2,4,1,2,7,5,4,5,0,3,1,7,5,5,3,0]

# Add constraints for each instruction
# These will be different for each instruction list
for x in instructions:
    B = A % 8
    B = B ^ 2
    C = A / (1 << B)
    A = A / 8
    B = B ^ C
    B = B ^ 7
    opt.add((B % 8) == x)

# Add final constraint: A should be 0 at the end
opt.add(A == 0)

# Minimize the starting value
opt.minimize(s)

# Solve
if opt.check() == sat:
    print("Solution found:")
    print(opt.model().eval(s))
else:
    print("No solution found")

