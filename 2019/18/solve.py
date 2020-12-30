#!/usr/bin/env python3

# Wtf. After 2 days of trying I went to reddit again
# to see how other people implemented this.

# Numpy is so not necessary here, but
# I'm using AoC to learn numpy now.
import numpy as np
import sys
import string
from collections import deque

# Return list of (y, x) positions for tiles with value tile
def get_yx_list(tile):
    res = np.where(board == tile)
    return list(zip(res[0], res[1]))

lower = string.ascii_lowercase
upper = string.ascii_uppercase

# Read input into numpy 2d array (board)
with open(sys.argv[1]) as f:
    lines = f.read().rstrip().split('\n')
width = len(lines[0])
heigth = len(lines)
board = np.array([list(line) for line in lines])

# Save robot pos and put . on board
robots = get_yx_list('@')
for robot in robots:
    board[robot] = '.'

# To stdout
def dump_board():
    np.savetxt(sys.stdout.buffer, board, fmt='%c', delimiter = '')

# pos = (y, x) tuple
def get_tile_at(pos):
    return board[pos]

# Initial keys and doors
ikeys = {}
idoors = {}
# Save keys and doors positions
for y in range(1, heigth - 1):
    row = board[y]
    for x in range(1, width - 1):
        c = row[x]
        if c in lower:
            ikeys[c] = (y, x)
        elif c in upper:
            idoors[c] = (y, x)

# y, x notation for easier access into board from pos
moves = { 'up'  : np.array([-1, 0], dtype = np.int),
        'down'  : np.array([ 1, 0], dtype = np.int),
        'left'  : np.array([ 0,-1], dtype = np.int),
        'right' : np.array([ 0, 1], dtype = np.int) }

dirs = [ 'up', 'down', 'left', 'right' ]

# Get position one step in movedir
def get_move_pos(pos, movedir):
    change = moves[movedir]
    return tuple(np.array(pos, dtype = np.int) + change)

# Keys, distances and positions reachable by one robot.
# Bundle of keys contains keys already collected
# (corresponding doors can be passed).
def reachable_keys(robotpos, bundle_of_keys):
    # bfs = queue of positions to visit
    bfs = deque([robotpos])
    # distances from robot
    dists = { robotpos: 0 }
    # (distance, (position)) tuples
    reachablekeys = {}
    while bfs:
        pos = bfs.pop()
        for movedir in dirs:
            newpos = get_move_pos(pos, movedir)
            tile = get_tile_at(newpos)
            if tile == '#':
                continue
            if newpos in dists:
                continue
            dists[newpos] = dists[pos] + 1
            if tile in idoors and tile.lower() not in bundle_of_keys:
                # Hit a door that we don't have the key to
                continue
            if (tile in ikeys) and (not tile in bundle_of_keys):
                # Found a new key
                reachablekeys[tile] = (dists[newpos], newpos)
            else:
                # append to bfs of positions to visit
                bfs.appendleft(newpos)
    return reachablekeys

# Part 2
# Keys, distances and positions reachable by all robots
def reachable_by_robots(robots, bundle_of_keys):
    keys = {}
    for i in range(len(robots)):
        robot = robots[i]
        rkeys = reachable_keys(robot, bundle_of_keys)
        for key, val in rkeys.items():
            # Each key can only be reached by one robot
            # val[0] = dist, val[1] = pos
            keys[key] = (val[0], val[1], i)
    return keys

# Ok, here is the recursion magic I borrowed from a reddit post
cache = {}
def min_distance_walk(robots, bundle_of_keys):
    sortedkeys = ''.join(sorted(bundle_of_keys))
    if (robots, sortedkeys) in cache:
        # Without this caching it would take a very long time
        return cache[(robots, sortedkeys)]
    print(sortedkeys, robots)
    keys = reachable_by_robots(robots, bundle_of_keys)
    if len(keys) == 0:
        # recursion end
        res = 0
    else:
        distances = []
        for key, (dist, pos, nrobot) in keys.items():
            new_robots = []
            for i in range(len(robots)):
                robot = robots[i]
                if i == nrobot:
                    new_robots.append(pos)
                else:
                    new_robots.append(robot)
            distances.append(dist + min_distance_walk(tuple(new_robots), bundle_of_keys + key))
        res = min(distances)
    cache[(tuple(robots), sortedkeys)] = res
    return res

#dump_board()
res = min_distance_walk(tuple(robots), '')
print(res)
