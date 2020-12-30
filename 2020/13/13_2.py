#!/usr/bin/env python3

import sys
from functools import reduce

# Crt functions below from stack overflow
def mul_inv(a, b):
    b0 = b
    x0, x1 = 0, 1
    if b == 1: return 1
    while a > 1:
        q = a // b
        a, b = b, a % b
        x0, x1 = x1 - q * x0, x0
    if x1 < 0: x1 += b0
    return x1

def chinese_remainder(n, a):
    sum = 0
    prod = reduce(lambda a, b: a*b, n)
    for n_i, a_i in zip(n, a):
        p = prod // n_i
        sum += a_i * mul_inv(p, n_i) * p
    return sum % prod

# my code
lines = open(sys.argv[1]).read().splitlines()
arr = lines[1].split(',')
busses = []
a = []
for x in arr:
    if x != 'x':
        busses.append(int(x))
        a.append(int(x) - arr.index(x))

print(busses, a)
print(chinese_remainder(busses, a))
