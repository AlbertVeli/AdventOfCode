#!/usr/bin/env python3

import sys
sys.path.insert(0,'../')
from aoc_input import *

if len(sys.argv) != 2:
    print('Usage:', sys.argv[0], '<input.txt>')
    sys.exit(1)
ss_org = input_as_lines(sys.argv[1])

l = len(ss_org[0])

def bitfiddle(keep_common):
    ss = list(ss_org)

    for i in range(l):
        # Count
        zeros = 0
        ones = 0
        for s in ss:
            b = s[i]
            if b == '1':
                ones += 1
            else:
                zeros += 1

        # Keep '1' or '0'?
        if keep_common:
            if zeros > ones:
                keep = '0'
            else:
                keep = '1'
        else:
            if zeros > ones:
                keep = '1'
            else:
                keep = '0'

        # Filter out keepers
        ss = list(filter(lambda x: x[i] == keep, ss))

        if len(ss) == 1:
            break

    return int(ss[0], 2)

oxy = bitfiddle(True)
co2 = bitfiddle(False)

print(oxy, co2, oxy * co2)
