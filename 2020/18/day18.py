#!/usr/bin/env python3

# Call calc < input.txt > result.txt to get result.txt
# Modify calc.y for part1/part2. See comment in calc.y.
# Run make to build calc from calc.l and calc.y

import sys

result = 0
for line in open('result.txt').read().splitlines():
    result += int(line.split()[1])
print(result)
