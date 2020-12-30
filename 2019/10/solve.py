#!/usr/bin/env python3

import sys
from math import sqrt
from math import atan2
from math import pi
from functools import cmp_to_key

# Distance between point (x0, y0) and line (x1, y1), (x2, y2)
# https://en.wikipedia.org/wiki/Distance_from_a_point_to_a_line#Line_defined_by_two_points
def pldist(p0, p1, p2):
    dy = p2[1] - p1[1]
    dx = p2[0] - p1[0]
    a = abs(dy * p0[0] - dx * p0[1] + p2[0] * p1[1] - p2[1] * p1[0])
    b = sqrt(dy * dy + dx * dx)
    return a / b

# Distance between points
def ldist(p0, p1):
    dy = p1[1] - p0[1]
    dx = p1[0] - p0[0]
    return sqrt(dy * dy + dx * dx)

# Direction, just return True/False tuple for x/y dir
def ldir(p0, p1):
    xdir = p1[0] - p0[0] > 0
    ydir = p1[1] - p0[1] > 0
    return((xdir, ydir))

# Only trig fn that works around the whole circle is atan2
def angle(p0, p1):
    return atan2(p1[1] - p0[1], p1[0] - p0[0])

# float rounding makes it dangerous to exactly
# compare two floats. Check if very close instead.
def close_to(a, b):
    if abs(a - b) < 0.001:
        return True
    return False

# Can station see asteroid without obstruction?
def can_see(station, asteroid):
    dists = []
    lda = ldist(station, asteroid)
    d1 = ldir(station, asteroid)
    #print(station, asteroid, lda)
    for p in points:
        if p != station and p != asteroid:
            d2 = ldir(station, p)
            # Cant intersect if d1, d2 not in same direction
            if d1 != d2: 
                continue
            #print(p, ldp, ldp <= lda)
            # can not intersect if p dist > asteroid dist
            ldp = ldist(station, p)
            if ldp <= lda:
                d = pldist(asteroid, station, p)
                dists.append(d)
    if len(dists) == 0:
        return True
    # Should be 0.0 but allow very small number for float rounding
    if close_to(min(dists), 0.0):
        return False
    return True

points  = []
y = 0
for line in sys.stdin:
    line = line.rstrip()
    for x in range(len(line)):
        if line[x] == '#':
            points.append((x, y))
    y += 1
#print(points)


# sort anglepoint tuple on angle
def anglesort(ta1, ta2):
    a1 = ta1[0]
    a2 = ta2[0]
    return a1 - a2

angles = []
nvap = 0

# Use global angles list
# Remove one and return next angle
def vaporize_one(angle, station):
    global nvap
    l = []
    next_angle = 0
    anglen = len(angles)
    for i in range (len(angles)):
        a = angles[i][0]
        if close_to(angle, a):
            l.append(i)
            next_angle = angles[(i + 1) % anglen][0]

    # Vaporize angles[vap]
    if len(l) == 1:
        vap = l[0]
    else:
        dists = []
        for i in l:
            dists.append((ldist(station, angles[i][1]), i))
        minst = min(dists)
        vap = minst[1]
    nvap += 1
    # Search output for 200 for answer
    if nvap == 200:
        sys.stdout.write('--> ')
    print('%d at' % nvap, angles[vap][1])
    del angles[vap]
    return next_angle

# 1 = do both, 2 = do only 2
part = 1
if part == 1:
    see = []
    # For each possible monitoring station
    for station in points:
        na = 0
        for asteroid in points:
            if asteroid != station:
                if can_see(station, asteroid):
                    na += 1
        see.append(na)
    #print(see)
    m = max(see)
    p = points[see.index(m)]
    print(p, m)

# Always do part 2, it's quick

# If part was 1, take answer from 1
# else hardcode station point
if part == 1:
    station = tuple(p)
else:
    station = (11, 13)
# Remove station itself from points
points.remove(station)

# angles = list with angles and points
# a4 = last quadrant, with negative numbers after rotation
a4 = []
for p in points:
    # rotate 90 degrees to simplify sorting
    arot = angle(station, p) + pi / 2
    if arot < 0:
        a4.append((arot, p))
    else:
        angles.append((arot, p))
# sort and move 4th quadrant last
a4 = sorted(a4, key=cmp_to_key(anglesort))
angles = sorted(angles, key=cmp_to_key(anglesort))
angles += a4

# Remove points from angles in clockwise order
next_ang = angles[0][0]
#print(angles)

# Vaporize all the things
while len(angles) > 0:
    next_ang = vaporize_one(next_ang, station)

