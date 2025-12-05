#!/usr/bin/env python3

import sys

def parse_input(text):
    ranges = []
    singles = []

    # Split into the two blocks
    block1, block2 = text.strip().split('\n\n')

    # Parse ranges (e.g. "3-5")
    for line in block1.splitlines():
        if '-' in line:
            a, b = line.split('-')
            ranges.append((int(a), int(b)))

    # Parse single integers
    for line in block2.splitlines():
        if line.strip():
            singles.append(int(line.strip()))

    return ranges, singles

def merge_ranges(ranges):
    # Sort by start value
    ranges = sorted(ranges, key=lambda x: x[0])

    merged = []
    for start, end in ranges:
        if not merged:
            merged.append((start, end))
            continue

        last_start, last_end = merged[-1]

        # Check overlap
        if start <= last_end and end >= last_start:
            # They overlap: keep the bigger outer interval
            merged[-1] = (min(last_start, start), max(last_end, end))
        else:
            # No overlap
            merged.append((start, end))

    return merged

def within_range(n, ranges):
    for a, b in ranges:
        if a <= n <= b:
            return True
    return False

def size(rng):
    return rng[1] - rng[0] + 1

with open(sys.argv[1], 'r') as f:
    text = f.read().strip()
ranges, singles = parse_input(text)

#print(ranges)
merged = merge_ranges(ranges)
#print(merged)

p1 = 0
for n in singles:
    if within_range(n, merged):
        p1 += 1

print('Part 1:', p1)

p2 = 0
for rng in merged:
    p2 += size(rng)
print('Part 2:', p2)
