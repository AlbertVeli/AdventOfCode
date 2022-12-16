#!/usr/bin/env python3

import sys
import re

def do_one_minute(states):
    new_states = []
    for p_tot, path, opened_valves in states:
        valve = path[-1]

        # add pressure released this minute to p_tot
        for ov in opened_valves:
            p_tot += flowrates[ov]

        # add alternatives, travel to any neighbor
        for neigh in valves[valve]:
            new_states.append((p_tot, path + [neigh], opened_valves.copy()))

        # or stay and release pressure (unless already open)
        if flowrates[valve] > 0 and valve not in opened_valves:
            ovc = opened_valves.copy()
            ovc.add(valve)
            new_states.append((p_tot, path, ovc))

    return new_states


# edges
valves = dict()
flowrates = dict()

lines = open(sys.argv[1]).read().rstrip().split('\n')
for line in lines:
    flowrate = list(map(int, re.findall(r'([-]?\d+)', line)))[0]
    a = list(re.findall(r'([A-Z]{2})', line))
    valves[a[0]] = a[1:]
    flowrates[a[0]] = flowrate

# Couldn't solve this in reasonable time
# borrowed the state structure from reddit
# 
# one state consists of a tuple with:
# - pressure released so far
# - path to current position
# - opened valves
# calculate each new possible state each minute
states = [(0, ['AA'], set())]

for minute in range(1, 30 + 1):
    states = do_one_minute(states)
    if len(states) > 5000:
        # prune worst states (least released pressure)
        states.sort(reverse = True)
        states = states[:5000]

# should be sorted already
print(states[0])
