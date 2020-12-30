#!/usr/bin/env python3

import sys

a = []
grp = []

# lazy loop, input must end with empty line, add manually
for line in open(sys.argv[1]).read().splitlines():
    if len(line) == 0:
        # group done
        a.append(grp)
        grp = []
    else:
        # non empty line, new person
        person = set()
        for c in line:
            person.add(c)
        grp.append(person)

part1 = 0
part2 = 0
for grp in a:
    s1 = set()
    s2 = grp[0]
    for person in grp:
        s1 = s1.union(person)
        s2 = s2.intersection(person)
    part1 += len(s1)
    part2 += len(s2)

print('part1:', part1)
print('part2:', part2)
