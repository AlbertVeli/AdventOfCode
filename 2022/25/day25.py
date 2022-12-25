#!/usr/bin/env python3

import sys

snafu = {'0': 0, '1': 1, '2': 2, '-': -1, '=': -2}

def s2d(s):
    s = s[::-1]
    ret = 0
    for i, c in enumerate(s):
        v = 5 ** i
        ret += snafu[c] * v
    return ret

def d2s(n):
    ret = []
    # remainder 3, 4 is -2, -1
    ud = {3 : '=', 4: '-'}
 
    while n > 0:
        d = n % 5
        if d < 3:
            # 0 - 2 is same as decimal
            c = str(d)
        else:
            # 3 or 4, this is the tricky part
            # add d to n left
            # and add snafu digit for -1 or -2
            n += d
            c = ud[d]

        ret.append(c)

        # done with this digit
        n = n // 5
    
    # return reversed string
    ret = ret[::-1]
    return ''.join(ret)

da = []
for line in open(sys.argv[1]).read().rstrip().split('\n'):
    da.append(s2d(line))

dec = sum(da)
print(dec)
print('Part 1:', d2s(dec))
