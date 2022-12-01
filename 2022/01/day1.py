#!/usr/bin/env python3

import sys

if len(sys.argv) != 2:
    print('Usage:', sys.argv[0], '<input.txt>')
    sys.exit(1)

totals = []

# Each user is separated by empty line, strip last newline
for user in open(sys.argv[1]).read().rstrip().split('\n\n'):
    # Each value for one user separated by \n, sum them up
    totals.append(sum(map(int, user.split('\n'))))

totals.sort(reverse = True)

print('Part 1:', totals[0])
#print(totals)
print('Part 2:', sum(totals[:3]))
