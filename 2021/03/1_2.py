#!/usr/bin/env python3

import sys
sys.path.insert(0,'../')
from aoc_input import *

if len(sys.argv) != 2:
    print('Usage:', sys.argv[0], '<input.txt>')
    sys.exit(1)
sorg = input_as_lines(sys.argv[1])

l = len(sorg[0])

def bitfiddle(keep_common):
    ss = list(sorg)
    for i in range(l):
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

        scp = list(ss)
        for s in scp:
            # All bit values are unique so it is safe
            # to use ss.remove()
            if s[i] != keep:
                ss.remove(s)
        if len(ss) == 1:
            break

    return ss

ss = bitfiddle(True)
oxy = int(ss[0], 2)

ss = bitfiddle(False)
co2 = int(ss[0], 2)

print(oxy, co2, oxy * co2)
