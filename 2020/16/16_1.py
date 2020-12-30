#!/usr/bin/env python3

import sys
import re

a = []
fields = []
myticket = []
tickets = []
state = 0
header = False
for line in open(sys.argv[1]).readlines():
    line = line.rstrip()
    if header:
        print(line)
        header = False
        continue

    if len(line) == 0:
        state += 1
        header = True
        continue

    if state == 0:
        line = line.split(':')
        ranges = re.findall(r"[0-9]+-[0-9]+", line[1])
        s1 = ranges[0].split('-')
        s2 = ranges[1].split('-')
        r1 = range(int(s1[0]), int(s1[1]) + 1)
        r2 = range(int(s2[0]), int(s2[1]) + 1)
        s2 = ranges[1].split('-')
        fields.append((line[0], r1, r2))
    elif state == 1:
        # your ticket:
        myticket = list(map(int, line.split(',')))
    elif state == 2:
        tickets.append(list(map(int, line.split(','))))

# part 1
ranges = []
for f in fields:
    ranges.append(f[1])
    ranges.append(f[2])

invalid = []
for t in tickets:
    for v in t:
        valid = False
        for r in ranges:
            if v in r:
                valid = True
                break
        if not valid:
            invalid.append(v)
            print(v,)
print(sum(invalid))

#print(tickets)
#print(fields)
#print(ranges)
#print(myticket)

