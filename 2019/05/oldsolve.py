#!/usr/bin/env python3

import sys

arr = []
alen = 0
pc = 0

# Return False if program is finished
def do_op():
    global pc

    # Read modes to m1-m3
    op = arr[pc]
    opm = '{:05d}'.format(op)
    m1 = int(opm[2])
    m2 = int(opm[1])
    m3 = int(opm[0])
    op = int(opm[3:])
    pc += 1


    if op == 99:
        return False

    elif op == 1:
        a, b, c = arr[pc : pc + 3]
        if m1 == 0:
            res = arr[a]
        else:
            res = a
        if m2 == 0:
            res += arr[b]
        else:
            res += b
        arr[c] = res
        pc += 3

    elif op == 2:
        a, b, c = arr[pc : pc + 3]
        if m1 == 0:
            res = arr[a]
        else:
            res = a
        if m2 == 0:
            res *= arr[b]
        else:
            res *= b
        arr[c] = res
        pc += 3

    elif op == 3:
        a = arr[pc]
        i = int(input(''))
        arr[a] = i
        pc += 1

    elif op == 4:
        a = arr[pc]
        if m1 == 0:
            sys.stdout.write(str(arr[a]))
        else:
            sys.stdout.write(str(a))
        pc += 1

    elif op == 5:
        a, b = arr[pc : pc + 2]
        if m1 == 0:
            aa = arr[a]
        else:
            aa = a
        if aa != 0:
            if m2 == 0:
                bb = arr[b]
            else:
                bb = b
            pc = bb
        else:
            pc += 2

    elif op == 6:
        a, b = arr[pc : pc + 2]
        if m1 == 0:
            aa = arr[a]
        else:
            aa = a
        if aa == 0:
            if m2 == 0:
                bb = arr[b]
            else:
                bb = b
            pc = bb
        else:
            pc += 2

    elif op == 7:
        a, b, c = arr[pc : pc + 3]
        if m1 == 0:
            aa = arr[a]
        else:
            aa = a
        if m2 == 0:
            bb = arr[b]
        else:
            bb = b
        if aa < bb:
            arr[c] = 1
        else:
            arr[c] = 0
        pc += 3

    elif op == 8:
        a, b, c = arr[pc : pc + 3]
        if m1 == 0:
            aa = arr[a]
        else:
            aa = a
        if m2 == 0:
            bb = arr[b]
        else:
            bb = b
        if aa == bb:
            arr[c] = 1
        else:
            arr[c] = 0
        pc += 3

    else:
        print('illegal op %d at pos %d' % op, pc)
        return False

    # Input finished, but didn't end with opcode 99
    if pc >= alen:
        return False

    return True


for i in map(int, input('').split(',')):
    arr.append(i)
alen = len(arr)

#print(arr)
while do_op():
    #print(arr)
    pass
