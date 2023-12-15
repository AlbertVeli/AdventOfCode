#!/usr/bin/env python3

import sys
sys.path.append('../..')
import aoc

expressions = aoc.input_string(sys.argv[1]).split(',')

def get_hash(s):
    current_value = 0
    for c in s:
        current_value = (current_value + ord(c)) * 17 % 256
    return current_value

hashes = []
for exp in expressions:
    hashes.append(get_hash(exp))
print('Part 1:', sum(hashes))

boxes = [[] for _ in range(256)]

# Get index of tuple in box with label
# or -1 if it doesn't exist
def label_index(box, label):
    for i, (lbl, val) in enumerate(box):
         if lbl == label:
              return i
    return -1

def do_expression(exp):
    if '-' in exp:
        label = exp[:-1]
        boxindex = get_hash(label)
        box = boxes[boxindex]
        i = label_index(box, label)
        if i != -1:
            # remove tuple at index i
            del box[i]
    elif '=' in exp:
        label, ns = exp.split('=')
        n = int(ns)
        boxindex = get_hash(label)
        box = boxes[boxindex]
        i = label_index(box, label)
        if i == -1:
            box.append((label, n))
        else:
            box[i] = (label, n)
    else:
        print('Shouldn\'t get here,', exp)

def dump_boxes():
    for i, box in enumerate(boxes):
        if len(box) > 0:
            print('box', i, box)

for exp in expressions:
    #print(exp)
    do_expression(exp)
    #dump_boxes()

n = 0
for bi, box in enumerate(boxes):
    if len(box) > 0:
        for ti, t in enumerate(box):
            n += (bi + 1) * (ti + 1) * t[1]
print('Part 2:', n)