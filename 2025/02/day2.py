#!/usr/bin/env python3

import sys

def is_invalid_id(n):
    s = str(n)
    if len(s) % 2 != 0:
        return False
    half = len(s) // 2
    return s[:half] == s[half:]

def is_invalid_id_2(n):
    s = str(n)
    L = len(s)

    for period_len in range(1, L // 2 + 1):
        if L % period_len != 0:
            # not divisible
            continue

        repeats = L // period_len
        if repeats < 2:
            continue

        pattern = s[:period_len]
        if pattern * repeats == s:
            return True

    return False

filename = sys.argv[1] if len(sys.argv) > 1 else 'input.txt'
with open(filename, 'r') as f:
    line = f.read().strip()

ranges = []
for part in line.split(','):
    a, b = part.split('-')
    ranges.append((int(a), int(b)))

o1 = 0
o2 = 0
for r1, r2 in ranges:
    for n in range(r1, r2 + 1):
        if is_invalid_id(n):
            o1 += n
        if is_invalid_id_2(n):
            o2 += n

print('Part 1:', o1)
print('Part 2:', o2)
