#!/usr/bin/env python3
import sys

def bits(mask, bit):
    a = ''
    done = False
    a = []
    i = -1
    while not done:
        try:
            i = mask.index(bit, i + 1)
            a.append(i)
        except:
            done = True
    return a

def apply_mask(mask, val):
    r = list('{0:036b}'.format(val))
    # zero-mask
    for i in bits(mask, '0'):
        r[i] = '0'
    # one-mask
    for i in bits(mask, '1'):
        r[i] = '1'
    r = ''.join(r)
    return int(r, 2)

mask = 'X'*36
mem = {}
for line in open(sys.argv[1]).read().splitlines():
    sp = line.split()
    ins = sp[0]
    op = sp[2]
    if ins.startswith('mask'):
        mask = sp[2]
    elif ins.startswith('mem'):
        val = int(sp[2])
        new_val = apply_mask(mask, val)
        m = int(ins[4:].replace(']', ''))
        mem[m] = new_val

print(sum(mem.values()))
