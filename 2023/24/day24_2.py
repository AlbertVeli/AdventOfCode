#!/usr/bin/env python3

import sys
sys.path.append('../..')
import aoc
# pip install z3-solver
import z3

lines = []
for line in aoc.lines(sys.argv[1]):
    x, y, z, dx, dy, dz = aoc.ints(line)
    lines.append((x, y, z, dx, dy, dz))

# Had to check reddit to get a hint that z3
# can be used to solve this automagically
# Merry Christmas!

# Update. My son tells me it can be proven that
# if a line exists that intersects all 300 lines
# then if you can find a line that intersects 3 of
# them, that line must also intersect the rest.
# But the Z3 solution below find a solution using
# all 300 lines.

#length = len(lines)
# Try just 3 and see if the result is the same
length = 3

# define z3 variables to use in constraints
# use z3.Int because we only want integer solutions
x = z3.Int('x')
y = z3.Int('y')
z = z3.Int('z')
dx = z3.Int('dx')
dy = z3.Int('dy')
dz = z3.Int('dz')
# collision times, [t0, t1, ...]
ts = [z3.Int(f't{i}') for i in range(length)]

s = z3.Solver()

# Add line equations as constraints to s
# If rock is thrown from (x, y, z) in dir (dx, dy, dz) after
# t (ns) it will be at (x + dx * t, y + dy * t, z + dz * t)
for i in range(length):
    t = ts[i]
    line_x, line_y, line_z, line_dx, line_dy, line_dz = lines[i]
    # search for ONE x, y, z, dx, dy, dz
    # that intercepts ALL lines. Time t can be
    # different for each intersection.
    s.add(x + t * dx == line_x + t * line_dx)
    s.add(y + t * dy == line_y + t * line_dy)
    s.add(z + t * dz == line_z + t * line_dz)
# run z3 solver to find x, y, z, dx, dy, dz
# and collision times to satisfy all constraints
s.check()
model = s.model()
pos = [model[var].as_long() for var in (x, y, z)]
vel = [model[var].as_long() for var in (dx, dy, dz)]
times = [model[var].as_long() for var in ts]
# manually check against example.txt that:
# collision times -> [5, 3, 4, 6, 1]
print(times)
# pos, vel -> [24, 13, 10], [-3, 1, 2]
print(pos, vel)
print('Part 2:', sum(pos))