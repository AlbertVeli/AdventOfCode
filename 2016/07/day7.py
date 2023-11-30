#!/usr/bin/env python3

import sys
sys.path.append('../..')
import aoc
import re

# Is ix within square brackets?
def is_within(line, ix):
    parens = 0
    for i in range(ix + 1):
        if line[i] == '[':
            parens += 1
        elif line[i] == ']':
            parens -= 1
    if parens == 0:
        return False

    return True

def part1_good(line):
    matches = re.finditer(r'([a-z])(?!\1)([a-z])\2\1', line)
    good = False
    for match in matches:
        ix = match.start()
        if is_within(line, ix):
            good = False
            #print(f'{match.group()} is within brackets')
            break
        else:
            good = True
            #print(f'{match.group()} is outside brackets')
    return good

def part2_good(line):
    regex = r'(?=([a-z])(?!\1)([a-z])\1)'
    matches1 = re.finditer(regex, line)
    for m1 in matches1:
        ix = m1.start()
        if not is_within(line, ix):
            aba = line[ix : ix + 3]
            bab = aba[1] + aba[0] + aba[1]
            for m2 in re.finditer(bab, line):
                ix2 = m2.start()
                if is_within(line, ix2):
                    #print(f'{aba} ({ix}) {bab} ({ix2})')
                    return True
    return False

lines = aoc.lines(sys.argv[1])
good1 = 0
good2 = 0
p2pattern = r'(?=([a-z])(?!\1)([a-z])\1)'
p2regex = re.compile(p2pattern)

for line in lines:
    #print(line)
    if part1_good(line):
        good1 += 1
    if part2_good(line):
        good2 += 1

print(f'part 1: {good1}')
print(f'part 2: {good2}')