#!/usr/bin/env python3

# Peeked at one of the reddit solutions
# but didn't steal it completely. Just
# used it to see if I got the dicts and
# lists correct in each stage.

import sys

d = {}

all_ingredients = []

lines = open(sys.argv[1]).read().splitlines()
for line in lines:
    i = line.index('(')
    ingredients = line[:i].split()
    all_ingredients.extend(ingredients)
    allergenes = line[i + 1:].replace('contains ', '').replace(')', '').replace(' ', '').split(',')
    for a in allergenes:
        if a in d:
            d[a] &= set(ingredients)
        else:
            d[a] = set(ingredients)

# map allergene -> ingredient
mapped = {}
while d:
    for a, i in list(d.items()):
        if len(i) == 1:
            # Only one ingredient, map to allergene a
            mapped[a] = list(i)[0]
            del d[a]
        else:
            # Remove already mapped ingredients
            d[a] -= set(mapped.values())

counted = {}
for i in all_ingredients:
    if not i in mapped.values():
        if not i in counted:
            counted[i] = all_ingredients.count(i)

# Part 1
print(sum(counted.values()))

# Part 2
d = dict(sorted(mapped.items(), key=lambda item: item[0]))
print(','.join(d.values()))
