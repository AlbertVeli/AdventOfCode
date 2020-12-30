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

def dir(x, y, dx, dy, arr):
    r = 0
    xx = x + dx
    yy = y + dy
    while xx < width and yy < heigth and xx >= 0 and yy >= 0:
        i = get_pixel(xx, yy, arr)
        if i == 1:
            # occupied
            r +=1
            break
        elif i == 0:
            # empty
            break
        xx += dx
        yy += dy
    return r

def see(x, y, arr):
    r = 0
    # right
    r += dir(x, y, 1, 0, arr)
    # left
    r += dir(x, y, -1, 0, arr)
    # up
    r += dir(x, y, 0, -1, arr)
    # down
    r += dir(x, y, 0, 1, arr)
    # down right
    r += dir(x, y, 1, 1, arr)
    # down left
    r += dir(x, y, -1, 1, arr)
    # up right
    r += dir(x, y, 1, -1, arr)
    # up left
    r += dir(x, y, -1, -1, arr)

    return r

def do_rules(org, rnd):
    r = array.array('b')
    for y in range(heigth):
        for x in range(width):
            seat = get_pixel(x, y, org)
            if seat < 0:
                r.append(seat)
                #sys.stdout.write('.')
            else:
                occ = see(x, y, org)
                #sys.stdout.write(str(occ))
                if seat == 0 and occ == 0:
                    seat = 1
                if seat == 1 and occ >= 5:
                    seat = 0
                r.append(seat)
        #sys.stdout.write('\n')
    return r

old_a = array.array('b', a)
rnd = 0
while True:
    print('round', rnd)
    print_a(old_a)
    new_a = do_rules(old_a, rnd)
    #if rnd == 1:
    #    break
    if new_a == old_a:
        break
    old_a = array.array('b', new_a)
    rnd += 1

print(rnd)
print(old_a.count(1))
