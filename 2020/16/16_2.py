#!/usr/bin/env python3

# Very messy

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
        #print(line)
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

ranges = []
for f in fields:
    ranges.append(f[1])
    ranges.append(f[2])

all_tickets = list(tickets)
for t in all_tickets:
    for v in t:
        valid = False
        for r in ranges:
            if v in r:
                valid = True
                break
        if not valid:
            tickets.remove(t)
            break

#print(fields)
#print(tickets)

# valid field indexes for each position
positions = {}

for pos in range(len(fields)):
    positions[pos] = []
    tv = []
    for t in tickets:
        tv.append(t[pos])
    for f in fields:
        valid = True
        for v in tv:
            if (not v in f[1]) and  (not v in f[2]):
                valid = False
                break
        if valid:
            positions[pos].append(fields.index(f))
            #print(tv, 'can be', f)

#print(positions)

# If only one positions possible, remove that index from all other
while True:
    old_positions = dict(positions)
    changed = False
    for p in old_positions:
        if len(old_positions[p]) == 1:
            remove = positions[p][0]
            for p2 in positions:
                if len(positions[p2]) > 1 and remove in positions[p2]:
                    print('remove', remove)
                    changed = True
                    positions[p2].remove(remove)
    if not changed:
        break

#print(positions)

res = 1
for p, fl in positions.items():
    f = fields[fl[0]]
    #print(p, f)
    if f[0].startswith('departure'):
        res *= myticket[p]
        #print(p, res)

print('part 2:', res)
