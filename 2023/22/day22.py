#!/usr/bin/env python3
import sys
sys.path.append('../..')
import aoc
from collections import deque

# Each brick is a rectangular prism represented
# by opposite (x, y, z) corners
# I don't know if all these methods will be needed
# but I'll add them anyway, just in case
class Brick:
    def __init__(self, name, x1, y1, z1, x2, y2, z2):
        self.name = name
        # Make sure self.z1 is the lowest z-value
        # to make sorting easier
        if z2 < z1:
            self.x1, self.y1, self.z1 = x2, y2, z2
            self.x2, self.y2, self.z2 = x1, y1, z1
        else:
            self.x1, self.y1, self.z1 = x1, y1, z1
            self.x2, self.y2, self.z2 = x2, y2, z2
        # List of bricks this brick is supported by
        self.supportedby: list['Brick'] = []
        # List of bricks this brick is supporting
        self.supporting: list['Brick'] = []
        self.settled = False

    def add_supported(self, other_brick: 'Brick'):
        self.supportedby.append(other_brick)

    def get_supported(self):
        return self.supportedby
    
    def add_supporting(self, other_brick: 'Brick'):
        self.supporting.append(other_brick)

    def get_supporting(self):
        return self.supporting

    # Try to move brick, return False if
    # brick is settled, True if it was moved.
    def move(self, other_bricks: list['Brick']):
        if self.settled or self.z1 == 1:
            self.settled = True
            return False

        # Try to move
        self.z1 -= 1
        self.z2 -= 1
        intersected = False
        for other_brick in other_bricks:
            if self.intersect(other_brick):
                intersected = True
                self.add_supported(other_brick)
                other_brick.add_supporting(self)
        if intersected:
            # Could not move
            self.z1 += 1
            self.z2 += 1
            self.settled = True
            return False

        # Could move
        return True

    def intersect(self, other_brick: 'Brick'):
        # Check for intersection along any axis
        x_intersect = not (self.x2 < other_brick.x1 or self.x1 > other_brick.x2)
        y_intersect = not (self.y2 < other_brick.y1 or self.y1 > other_brick.y2)
        z_intersect = not (self.z2 < other_brick.z1 or self.z1 > other_brick.z2)
        # If all axes have overlap, there is an intersection
        if x_intersect and y_intersect and z_intersect:
            #print(self,'and',other_brick,'intersects')
            return True
        #print(self,'and',other_brick,'do not intersect')
        return False

    # These two are not needed for today's task, maybe later
    def volume(self):
        length = abs(self.x2 - self.x1)
        width = abs(self.y2 - self.y1)
        height = abs(self.z2 - self.z1)
        return length * width * height

    # Combined volume of two intersecting bricks is:
    # b1.volume) + b2.volume() - b1.intersection_volume(b2)
    def intersection_volume(self, other_brick: 'Brick'):
        x_overlap = max(0, min(self.x2, other_brick.x2) - max(self.x1, other_brick.x1))
        y_overlap = max(0, min(self.y2, other_brick.y2) - max(self.y1, other_brick.y1))
        z_overlap = max(0, min(self.z2, other_brick.z2) - max(self.z1, other_brick.z1))
        intersection_volume = x_overlap * y_overlap * z_overlap
        return intersection_volume

    def is_settled(self):
        if self.z1 == 1 or len(self.supportedby) > 0:
            return True
        return False

    def __str__(self):
        return f'{self.name} {self.x1},{self.y1},{self.z1}~{self.x2},{self.y2},{self.z2}'
    
    def __eq__(self, other: 'Brick'):
        # special case, all instances have unique names and coordinates
        return self.name == other.name

def dump_bricks():
    print('falling')
    for brick in bricks:
        print(brick)
    print('settled')
    for brick in settled_bricks:
        print(brick)
    print('')

bricks = []
# Move brick from bricks to settled_bricks when settled
settled_bricks = []

i = 0
for line in aoc.lines(sys.argv[1]):
    b1, b2 = line.split('~')
    x1, y1, z1 = map(int, b1.split(','))
    x2, y2, z2 = map(int, b2.split(','))
    name = 'b' + str(i)
    brick = Brick(name, x1, y1, z1, x2, y2, z2)
    bricks.append(brick)
    i += 1

# Fall one step, return number of moved bricks
def fall_one_step(bricks: list['Brick'], settled_bricks: list['Brick'], remove):
    new_settled = []
    n_moved = 0
    for brick in bricks:
        if not brick.move(settled_bricks):
            #print(brick,'is settled')
            new_settled.append(brick)
            settled_bricks.append(brick)
            n_moved += 1
    # Remove the new settled bricks from falling bricks
    for brick in new_settled:
        if remove:
            bricks.remove(brick)
    return n_moved

# sort bricks (move the ones with lowest z first)
bricks = sorted(bricks, key=lambda b: b.z1)
while fall_one_step(bricks, settled_bricks, True) > 0:
    # dump_bricks()
    pass

"""
# Should be settled now
# Just for debug
print(len(settled_bricks))
for brick in settled_bricks:
    print(brick, 'supporting: ', end='')
    for b2 in brick.supporting:
        print(b2, end=' ')
    print('')
"""

def can_disintegrate(brick: 'Brick', bricks: list['Brick']):
    if len(brick.supporting) == 0:
        # Supports noone
        return True
    for supbrick in brick.supporting:
        other = False
        # check if any other bricks are supporting supbrick
        for b in bricks:
            if b == brick:
                # dont compare with ourselves
                continue
            if supbrick in b.supporting:
                other = True
                break
        if not other:
            return False
    return True

def n_disintegrate(brick: 'Brick'):
    q = deque()
    removed = [brick]

    for supbrick in brick.get_supporting():
        q.append(supbrick)

    while len(q) > 0:
        curbrick = q.popleft()
        supportedby = curbrick.get_supported()
        supporting = curbrick.get_supporting()

        if all(supbrick in removed for supbrick in supportedby):
            if not curbrick in removed:
                removed.append(curbrick)
            for support in supporting:
                q.append(support)

    return len(removed) - 1

n = 0
for brick in settled_bricks:
    if can_disintegrate(brick, settled_bricks):
        #print(brick,'can disintegrate')
        n += 1
    else:
        #print(brick,'no disintegrate')
        pass

print('Part 1:', n)

n = 0
for brick in settled_bricks:
    # TODO: slight bug here
    # wrong answer for some inputs
    ndis = n_disintegrate(brick)
    #print(ndis)
    n += ndis
print('Part 2:', n)