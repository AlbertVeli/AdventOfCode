#!/usr/bin/env python3

import sys
import re

# Read input and put into dict bagcolor: [(), ()]
# each tuple in value list contains (num, color)
d = dict()
for line in open(sys.argv[1]).read().splitlines():
    ls = line.rstrip().split(',')
    bagcolor = list(map(str, re.findall(r"(^.*) bags contain", ls[0])))[0]
    t = list(map(tuple, re.findall(r"(^.*) bags contain ([0-9]+) (.*) bag[s\.]*", ls[0])))
    if len(t) == 0:
        # contain no other bags
        d[bagcolor] = []
    else:
        # bag holding bag, list of (num, color) tuples
        t = t[0]
        contents = [(int(t[1]), t[2])]
        for s in ls[1:]:
            b = s.strip().split()
            contents.append((int(b[0]), b[1] + ' ' + b[2]))
        d[bagcolor] = contents

#print(d)

# Part 1
def can_hold(bag, mybag):
    for t in d[bag]:
        num = t[0]
        cbag = t[1]
        if cbag == mybag:
            return True
        elif can_hold(cbag, mybag):
            return True
    return False

# Search tree for shiny gold
mybag = 'shiny gold'
r = 0
for bag in d:
    if can_hold(bag, mybag):
        r += 1
print('part 1:', r)

# Part 2
# holds returns number of bags bag holds
def holds(bag):
    r = 0
    #print('holds enter', bag, d[bag])
    for t in d[bag]:
        num = t[0]
        bag = t[1]
        r += num
        r += num * holds(bag)
    #print('holds ret', r)
    return r

print('part 2', holds(mybag))

