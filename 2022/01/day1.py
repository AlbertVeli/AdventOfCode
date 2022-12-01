#!/usr/bin/env python3

import sys

if len(sys.argv) != 2:
    print('Usage:', sys.argv[0], '<input.txt>')
    sys.exit(1)

totals = []
total = 0

for line in open(sys.argv[1]):
    line = line.rstrip()
    if len(line) > 0:
        n = int(line, 10)
        total += n
    else:
        totals.append(total)
        total = 0
totals.append(total)

totals = sorted(totals)[::-1]
totals = totals[:3]

print('Part 1:', totals[0])
#print(totals)
print('Part 2:', sum(totals))
