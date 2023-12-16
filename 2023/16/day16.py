#!/usr/bin/env python3

import sys
sys.path.append('../..')
import aoc

grid = aoc.char_matrix(sys.argv[1])
height = len(grid)
width = len(grid[0])

def dump_grid():
    for y, row in enumerate(grid):
        for x, c in enumerate(row):
            if (x, y) in visited:
                sys.stdout.write('#')
            else:
                sys.stdout.write(c)
        print('')

# Add two tuples element-wise
def add_pos_dir(pos, dir):
    return tuple(map(sum, zip(pos, dir)))

# Reflection direction
reflection_dirs = {
    ('/', (1, 0)): (0, -1),
    ('/', (-1, 0)): (0, 1),
    ('/', (0, 1)): (-1, 0),
    ('/', (0, -1)): (1, 0),
    ('\\', (1, 0)): (0, 1),
    ('\\', (-1, 0)): (0, -1),
    ('\\', (0, 1)): (1, 0),
    ('\\', (0, -1)): (-1, 0)
}

def onboard(pos):
    x, y = pos
    if x < 0 or x > width - 1 or y < 0 or y > height - 1:
        return False
    return True

def already_visited(p):
    pos, dir = p
    if pos in visited and dir in visited[pos]:
        return True
    return False

def pos_visited(pos, dir):
    if pos in visited:
        vpos = visited[pos]
        if dir in vpos:
            # pos, dir already in visited
            True
        else:
            # We have visited pos but not in dir
            vpos.append(dir)
    else:
        visited[pos] = [dir]

    return False

# Fire a phaser from pos in dir
def fire_phaser(p):
    pos, dir = p

    # Check if pos, dir is already visited.
    # This also adds pos, dir to visited.
    if pos_visited(pos, dir):
        return False

    x, y = pos
    try:
        c = grid[y][x]
    except:
        print(p, pos, width, height)

    # calc new dir
    if c == '/' or c == '\\':
        dir = reflection_dirs[(c, dir)]
    elif c == '|':
        if dir[1] == 0:
            # horizontal movement, split phaser beam
            # keep one in pos, dir and if there is
            # a second, add it to new_phasers
            dir1 = (0, -1)
            dir2 = (0, 1)
            pos1 = add_pos_dir(pos, dir1)
            pos2 = add_pos_dir(pos, dir2)
            if onboard(pos1):
                dir = dir1
                if onboard(pos2):
                    # Handle new beam later
                    new_phasers.append((pos2, dir2))
            else:
                # first split beam not onboard
                dir = dir2
                if not onboard(pos2):
                    # both split beams off board, this can
                    # not happen if height > 2
                    print('Should not get here', c, pos, dir)
    elif c == '-':
        if dir[0] == 0:
            # vertical movement, split phaser beam
            dir1 = (-1, 0)
            dir2 = (1, 0)
            pos1 = add_pos_dir(pos, dir1)
            pos2 = add_pos_dir(pos, dir2)
            if onboard(pos1):
                dir = dir1
                if onboard(pos2):
                    # Handle new phaser beam later
                    new_phasers.append((pos2, dir2))
            else:
                # first split beam not onboard
                dir = dir2
                if not onboard(pos2):
                    # both split beams off board, this can
                    # not happen if width > 2
                    print('Should not get here', c, pos, dir)

    # dir should now be the new direction
    new_pos = add_pos_dir(pos, dir)
    if not onboard(new_pos):
        return False

    return (new_pos, dir)

def sim(phaser_start):
    # used by fire_phaser
    global new_phasers, visited
    visited = {}
    phasers = [phaser_start]

    while len(phasers) > 0:
        new_phasers = []
        removed_phasers = []
        for i, phaser in enumerate(phasers):
            beam = fire_phaser(phaser)
            #print(i, phaser, beam)
            if not beam:
                removed_phasers.append(phaser)
            # TODO: This should already be checked by fire_phaser
            elif (not onboard(beam[0])) or already_visited(beam):
                removed_phasers.append(phaser)
            else:
                # replace with new position
                phasers[i] = beam
        for phaser in new_phasers:
            phasers.append(phaser)
        for phaser in removed_phasers:
            phasers.remove(phaser)

        # Could do animation here
        #dump_grid()
        #input('')

    return len(visited)

# Part 1, phaser at (0, 0) firing right
# For each visited pos, save a list of directions
phaser = ((0, 0), (1, 0))
print('Part 1:', sim(phaser))

# Part 2, fire from all edge positions
scores = []
for x in range(width):
    # Down
    scores.append(sim(((x, 0), (0, 1))))
    # Up
    scores.append(sim(((x, height - 1), (0, -1))))
for y in range(height):
    # Right
    scores.append(sim(((0, y), (1, 0))))
    # Left
    scores.append(sim(((width - 1, y), (-1, 0))))

print('Part 2:', max(scores))