#!/usr/bin/env python3

import sys
sys.path.insert(0,'../common')
from utils import ints

lines = open(sys.argv[1]).read().splitlines()
timestamp = int(lines[0])
times = ints(lines[1])

def find_bus():
    t = timestamp
    while True:
        for bus in times:
            if t % bus == 0:
                return (t, bus)
        t += 1

t, bus = find_bus()
print((t - timestamp) * bus)
