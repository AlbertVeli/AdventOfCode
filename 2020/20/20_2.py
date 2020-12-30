#!/usr/bin/env python3

# Finally done!
# This took me a whole day to get working.
# And I didn't start until after day 25 was
# finished and I saw that part 2 of day 25 was
# to have all earlier 49 stars. Including this
# one which was by far the hardest one.

import sys
import re
from math import sqrt

# Name -> index in edge array
#edge_ix = {'n': 0, 'e': 1, 's': 2, 'w': 3, 'rev_n': 4, 'rev_e': 5, 'rev_s': 6, 'rev_w': 7}

class Tile:
    def __init__(self, tile_id, tile_lines):
        self.id = tile_id
        self.lines = list(tile_lines)
        self.shared_edges = []
        self.calc_edges()

    def __str__(self):
        s = self.id + '\n'
        for line in self.lines:
            s = s + line.replace('0', '.').replace('1', '#') + '\n'
        return s

    def calc_edges(self):
        east = ''
        west = ''
        for i in range(10):
            west += self.lines[i][0]
            east += self.lines[i][9]
        self.edges = []
        # Normal
        self.edges.append(int(self.lines[0], 2))
        self.edges.append(int(east, 2))
        self.edges.append(int(self.lines[9], 2))
        self.edges.append(int(west, 2))
        # Flipped
        self.edges.append(int(self.lines[0][::-1], 2))
        self.edges.append(int(east[::-1], 2))
        self.edges.append(int(self.lines[9][::-1], 2))
        self.edges.append(int(west[::-1], 2))

    def rotate(self):
        # the ''.join line is borrowed from another solution
        self.lines = list(''.join(x[::-1]) for x in zip(*self.lines))
        rot_edges = []
        for ix, neighbour in self.shared_edges:
            rot_edges.append(((ix + 1) % 4, neighbour))
        self.shared_edges = rot_edges
        self.calc_edges()

    def flip_y(self):
        self.lines = list(reversed(self.lines))
        flipped_edges = []
        for ix, neighbour in self.shared_edges:
            if ix % 2 == 0:
                flipped_edges.append(((ix + 2) % 4, neighbour))
            else:
                flipped_edges.append((ix, neighbour))
        self.shared_edges = flipped_edges
        self.calc_edges()

    def flip_x(self):
        lines = []
        for line in self.lines:
            lines.append(line[::-1])
        self.lines = lines
        flipped_edges = []
        for ix, neighbour in self.shared_edges:
            if ix % 2 == 1:
                flipped_edges.append(((ix + 2) % 4, neighbour))
            else:
                flipped_edges.append((ix, neighbour))
        self.shared_edges = flipped_edges
        self.calc_edges()


    # This is the key to placement
    # 1) Rotate until neighbor_id is in neighbor_dir direction
    # 2) If edges don't match, flip in y-direction if
    #    neighbor_dir is odd, else x-direction
    # 3) (optional) double check that edges match
    def xform(self, neighbor_id, neighbor_dir):
        while self.get_neighbour(neighbor_dir) != neighbor_id:
            #print('rotate', self.get_neighbour(neighbor_dir), neighbor_id)
            self.rotate()
        neighbors_dir = (neighbor_dir - 2) % 4
        if tiles[neighbor_id].edges[neighbors_dir] != self.edges[neighbor_dir]:
            if neighbor_dir % 2 == 1:
                self.flip_y()
            else:
                self.flip_x()
            #print('edges differ, flip, equal?', tiles[neighbor_id].edges[neighbors_dir] == self.edges[neighbor_dir])


    # Any rotation
    def shares_edge(self, tile2):
        for e in self.edges:
            if e in tile2.edges:
                # Save neighbour id
                ix = self.edges.index(e)
                self.shared_edges.append((ix, tile2.id))
                return True
        return False

    def get_neighbour(self, direction):
        for ix, neighbour_id in self.shared_edges:
            if ix == direction:
                return neighbour_id
        return False

tile_re = re.compile(r'Tile ([0-9]+):')
tiles = {}

for line in open(sys.argv[1]).read().splitlines():
    if len(line) == 0:
        # Tile finished
        tiles[tile_id] = Tile(tile_id, tile_lines)
        continue
    num = tile_re.findall(line)
    if num:
        # New tile
        tile_id = num[0]
        tile_lines = []
    else:
        # Tile line
        tile_lines.append(line.replace('.', '0').replace('#', '1'))

width = int(sqrt(len(tiles)))
heigth = width

# Loop through all tiles and save shared edges
for tile in tiles.values():
    for tile2 in tiles.values():
        if tile.id != tile2.id:
            tile.shares_edge(tile2)
    if len(tile.shared_edges) == 2:
        edges = (tile.shared_edges[0][0], tile.shared_edges[1][0])
        # Start with corner tile that has one neighbour
        # to the east and one to the south
        if 1 in edges and 2 in edges:
            start_id = tile.id

first = True
for _ in range(heigth):
    if first:
        # Place start tile
        #print('Start tile is --', start_id, '--')
        #print(tiles[start_id].shared_edges)
        placed = [start_id]
        prev_id = start_id
        first = False
    else:
        # First tile in line
        prev_id = placed[(len(placed) - width)]
        tile_id = tiles[prev_id].get_neighbour(2)
        tile = tiles[tile_id]
        #print('\nFirst tile is --', tile_id, '--')
        #print('before', tile.shared_edges)
        # First in line above is in direction 0
        tile.xform(prev_id, 0)
        #print('edges', tile.shared_edges)
        placed.append(tile_id)
        prev_id = tile_id

    # Rest of line
    for _ in range(1, width):
        # Place tile east of this one
        tile_id = tiles[prev_id].get_neighbour(1)
        if not tile_id:
            print('Error:', prev_id, 'has no east neighbour')
            sys.exit(1)
        tile = tiles[tile_id]
        #print('East neighbour --', tile_id, '--')
        # Previous tile should be west, 3
        tile.xform(prev_id, 3)
        #print('edges', tile.shared_edges)
        placed.append(tile_id)
        prev_id = tile_id

# Use globals width, heigth and tiles
class Image:
    def __init__(self, placed):
        self.placed = placed
        self.lines = []
        for ty in range(heigth):
            for y in range(1, 9):
                # One line of tiles
                img_line = ''
                for tx in range(width):
                    tile = tiles[placed[tx + ty * width]]
                    line = tile.lines[y].replace('0', '.').replace('1', '#')
                    for x in range(1, 9):
                        c = line[x]
                        img_line += c
                self.lines.append(img_line)

        # Compile monster regexes
        self.rexes = []
        rs = [r'..................#',
              r'#....##....##....###',
              r'.#..#..#..#..#..#']
        for r in rs:
            self.rexes.append(re.compile(r))

    def __str__(self):
        s = ''
        for line in self.lines:
            s += line + '\n'
        return s.rstrip()

    def rotate(self):
        self.lines = list(''.join(x[::-1]) for x in zip(*self.lines))

    def flip_y(self):
        self.lines = list(reversed(self.lines))

    def matches_line(self, line, regno):
        matches = []
        for match in re.finditer(self.rexes[regno], line):
            matches.append(match.start())
        return matches

    def find_monsters(self):
        monsters = 0
        # Middle line is longest
        monster_len = len('#....##....##....###')
        # Middle monster line
        for y in range(1, heigth * 8):
            line = self.lines[y]
            matches1 = self.matches_line(line, 1)
            if len(matches1) > 0:
                for ix in matches1:
                    #print('middle match, line', y, 'index', ix)
                    line0 = self.lines[y - 1][ix : ix + monster_len]
                    matches0 = self.matches_line(line0, 0)
                    if len(matches0) > 0:
                        # Should match at index 0
                        if not 0 in matches0:
                            continue
                        #print('top match')
                        line2 = self.lines[y + 1][ix : ix + monster_len]
                        matches2 = self.matches_line(line2, 2)
                        if len(matches2) > 0:
                            if not 0 in matches2:
                                continue
                            #print('bottom match, monster found!')
                            monsters += 1
        return monsters

im = Image(placed)

monster = """
                  #
#    ##    ##    ###
 #  #  #  #  #  #
 """
monster_hashes = monster.count('#')
image_hashes = 0
for line in im.lines:
    image_hashes += line.count('#')

for i in range(4):
    print('rotation', i)
    #print(im)
    monsters = im.find_monsters()
    if monsters > 0:
        print('\nfound', monsters, 'monsters!')
        print('roughness:', image_hashes - monsters * monster_hashes, '\n')
    im.rotate()

print('flip')
im.flip_y()
for i in range(4):
    print('flipped rotation', i)
    #print(im)
    monsters = im.find_monsters()
    if monsters > 0:
        print('\nfound', monsters, 'monsters!')
        print('roughness:', image_hashes - monsters * monster_hashes, '\n')
    im.rotate()
