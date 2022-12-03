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
for s in a:
    h = len(s) // 2
    s = list(s)
    h1 = s[:h]
    h2 = s[h:]
    c = list(set(h1).intersection(h2))[0]
    total += val(c)

print(total)
