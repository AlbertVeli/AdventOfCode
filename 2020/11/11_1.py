#!/usr/bin/env python3

# XXX: This would be more efficient with numpy

import sys
import array

width = 0
heigth = 0

# . = floor    = -1
# L = empty    =  0
# # = occupied =  1

# Use 1-d array of bytes to keep pixels
def read_input(fname):
    global width
    global heigth
    a = array.array('b')
    width = len(open(fname).readline().rstrip())
    for line in open(fname).read().splitlines():
        heigth += 1
        for c in line:
            if c == 'L':
                a.append(0)
            elif c == '.':
                a.append(-1)
            else:
                print('input: bad char', c)
                sys.exit(0)
    return a

a = read_input(sys.argv[1])

# for faster x,y lookup in a
ytab = array.array('I')
for y in range(heigth):
    ytab.append(y * width)

def get_pixel(x, y, arr):
    return arr[ytab[y] + x]

def print_a(a):
    for y in range(heigth):
        for x in range(width):
            i = a[ytab[y] + x]
            if i == -1:
                c = '.'
            elif i == 0:
                c = 'L'
            elif i != 1:
                print('Bad pixel', i, 'at', x, y)
                sys.exit(0)
            else:
                c = '#'
            sys.stdout.write(c)
        sys.stdout.write('\n')

def adj(x, y, arr):
    r = 0
    for yy in range(y - 1, y + 2):
        for xx in range(x - 1, x + 2):
            if (xx >= 0 and xx < width and yy >= 0 and yy < heigth):
                if xx != x or yy != y:
                    i = get_pixel(xx, yy, arr)
                    if i > 0:
                        r += i
    return r

def do_rules(org, rnd):
    r = array.array('b')
    for y in range(heigth):
        for x in range(width):
            seat = get_pixel(x, y, org)
            if seat < 0:
                r.append(seat)
            else:
                occ = adj(x, y, org)
                if seat == 0 and occ == 0:
                    seat = 1
                if seat == 1 and occ >= 4:
                    seat = 0
                r.append(seat)
    return r

old_a = array.array('b', a)
rnd = 0
while True:
    print('round', rnd)
    print_a(old_a)
    new_a = do_rules(old_a, rnd)
    if new_a == old_a:
        break
    old_a = array.array('b', new_a)
    rnd += 1

#print(rnd)
print(old_a.count(1))
