#!/usr/bin/env python3

import sys

s = 0

for line in sys.stdin:
    s += int(line) // 3 - 2

print(s)
