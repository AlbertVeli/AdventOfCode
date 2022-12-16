#!/usr/bin/env python3

import sys
import re

def get_new_paths(path, opened_valves):
    new_paths = []
    valve = path[-1]

    # travel to any neighbor
    for neigh in valves[valve]:
        new_paths.append((path + [neigh], opened_valves.copy()))

    # or stay and release pressure
    if flowrates[valve] > 0 and valve not in opened_valves:
        ovc = opened_valves.copy()
        ovc.add(valve)
        new_paths.append((path, ovc))

    return new_paths

def do_one_minute(states):
    new_states = []
    for p_tot, paths, opened_valves in states:
        v_me = paths[0][-1]
        v_elephant = paths[1][-1]

        # add pressure released this minute to p_tot
        for ov in opened_valves:
            p_tot += flowrates[ov]

        for path_me, opened_me in get_new_paths(paths[0], opened_valves):
            for path_elephant, opened_elephant in get_new_paths(paths[1], opened_me):
                new_states.append((p_tot, (path_me, path_elephant), opened_elephant))

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

# Like part 1, but with two paths
# One for me and one for the elephant
states = [(0, (['AA'], ['AA']), set())]

for minute in range(1, 26 + 1):
    states = do_one_minute(states)
    if len(states) > 5000:
        # prune worst states (least released pressure)
        states.sort(reverse = True)
        states = states[:5000]

# should be sorted already
print(states[0])
