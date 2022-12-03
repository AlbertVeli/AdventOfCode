#!/usr/bin/env python3

import sys

if len(sys.argv) != 2:
    print('Usage:', sys.argv[0], '<input.txt>')
    sys.exit(1)

def val(c):
    if c.isupper():
        return 27 + ord(c) - ord('A')
    return 1 + ord(c) - ord('a')

for s in open(sys.argv[1]).read().rstrip().split('\n\n'):
    a = s.split('\n')

total = 0
for i in range(0, len(a), 3):
    c = list(set(a[i + 0]).intersection(a[i + 1]).intersection(a[i + 2]))[0]
    total += val(c)

print(total)
