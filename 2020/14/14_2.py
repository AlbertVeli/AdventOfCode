#!/usr/bin/env python3
import sys
from itertools import product

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
    # one-mask
    for i in bits(mask, '1'):
        r[i] = '1'
    # x-mask
    xa = bits(mask, 'X')
    p = list(product('01', repeat=len(xa)))
    ret = []
    for i in range(len(p)):
        a = list(r)
        t = p[i]
        for bit in range(len(xa)):
            a[xa[bit]] = t[bit]
        ret.append(int(''.join(a)))
    return ret

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
        m = int(ins[4:].replace(']', ''))
        mlist = apply_mask(mask, m)
        for m in mlist:
            mem[m] = val

print(sum(mem.values()))
