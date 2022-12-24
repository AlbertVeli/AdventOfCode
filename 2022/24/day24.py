#!/usr/bin/env python3

import sys

# Add (x, y) tuples a and b
def p_add(a, b):
    return (a[0] + b[0], a[1] + b[1])

def has_blizzard(t):
    x, y = t
    for d in dirs.keys():
        if (x, y, d) in blizzards:
            return True
    return False

def move_blizzards():
    global blizzards, free
    moves = set()
    removes = set()
    for x, y, d in blizzards:
        newb = p_add((x, y), dirs[d])
        bx = (newb[0] - 1) % (width - 2) + 1
        by = (newb[1] - 1) % (height - 2) + 1
        # Delete old position, add new position
        removes.add((x, y, d))
        moves.add((bx, by, d))
    for x, y, d in removes:
        blizzards.remove((x, y, d))
    for x, y, d in moves:
        blizzards.add((x, y, d))

    # Rebuild free after move
    free = set()
    for y in range(height):
        for x in range(width):
            if (x, y) in walls:
                continue
            elif has_blizzard((x, y)):
                continue
            else:
                free.add((x, y))

def find_blizzard(t):
    found = ''
    x, y = t
    for d in dirs.keys():
        if (x, y, d) in blizzards:
            if len(found) > 0:
                if not found.isdigit():
                    found = '2'
                else:
                    found = str(int(found) + 1)
            else:
                found = d
    return found

def print_grid():
    for y in range(height):
        for x in range(width):
            if (x, y) in players:
                sys.stdout.write('E')
            elif (x, y) in free:
                sys.stdout.write('.')
            elif (x, y) in walls:
                sys.stdout.write('#')
            else:
                b = find_blizzard((x, y))
                sys.stdout.write(b)
        sys.stdout.write('\n')
    sys.stdout.write('\n')
    input('press enter to continue')

def move_players(players):
    new_players = set()
    for p in players:
        if p in free:
            # one option is to stay
            new_players.add(p)
        for dp in dirs.values():
            # or move n, s, e or w
            np = p_add(p, dp)
            if np in free:
                new_players.add(np)
    return new_players

def move_from_to(start, end):
    # possible player positions this minute
    players = set()
    players.add(start)
    for rnd in range(10000):
        move_blizzards()
        players = move_players(players)
        #print_grid()
        if end in players:
            break
    return rnd + 1


# Main

blizzards = set()
free = set()
walls = set()
for y, line in enumerate(open(sys.argv[1]).read().rstrip().split('\n')):
    width = len(line)
    for x, c in enumerate(line):
        if c == '#':
            walls.add((x, y))
        elif c == '.':
            free.add((x, y))
        else:
            # Must be a blizzard
            blizzards.add((x, y, c))

height = y + 1

dirs = { '^' : ( 0, -1), 'v' : ( 0,  1), '<' : (-1, 0), '>' : ( 1, 0) }

# Start and end positions
s = (1, 0)
e = (width - 2, height - 1)
p1 = move_from_to(s, e)
print('Part 1:', p1)
p2 = move_from_to(e, s)
p3 = move_from_to(s, e)
print('Part 2:', p1 + p2 + p3)
