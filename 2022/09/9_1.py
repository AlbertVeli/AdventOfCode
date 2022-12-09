#!/usr/bin/env python3

import sys

if len(sys.argv) != 2:
    print('Usage:', sys.argv[0], '<input.txt>')
    sys.exit(1)


head = [0, 0]
tail = [0, 0]

def move_up():
    global head
    global tail
    hx, hy = head
    ohx, ohy = head
    tx, ty = tail
    hy -= 1
    if ty - ohy > 0:
        # tail moves
        tx = ohx
        ty = ohy
    head = [hx, hy]
    tail = [tx, ty]

def move_down():
    global head
    global tail
    hx, hy = head
    ohx, ohy = head
    tx, ty = tail
    hy += 1
    if ty - ohy < 0:
        # tail moves
        tx = ohx
        ty = ohy
    head = [hx, hy]
    tail = [tx, ty]

def move_left():
    global head
    global tail
    hx, hy = head
    ohx, ohy = head
    tx, ty = tail
    hx -= 1
    if tx - ohx > 0:
        # tail moves
        tx = ohx
        ty = ohy
    head = [hx, hy]
    tail = [tx, ty]

def move_right():
    global head
    global tail
    hx, hy = head
    ohx, ohy = head
    tx, ty = tail
    hx += 1
    if tx - ohx < 0:
        # tail moves
        tx = ohx
        ty = ohy
    head = [hx, hy]
    tail = [tx, ty]

visited = set()
visited.add((tail[0], tail[1]))
for line in map(str.rstrip, open(sys.argv[1])):
    d, s = line.split(' ')
    s = int(s)
    for _ in range(s):
        if d == 'D':
            move_down()
        elif d == 'L':
            move_left()
        elif d == 'R':
            move_right()
        elif d == 'U':
            move_up()
        visited.add((tail[0], tail[1]))
    #print(head, tail)

print(len(visited))
