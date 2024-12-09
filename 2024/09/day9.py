import sys
sys.path.append('../..')
import aoc

def calc_checksum(disk_layout):
    return sum(c * i for i, c in enumerate(disk_layout) if isinstance(c, int))

def compact_disk_1(layout):
    """Compact the disk layout by moving files to the leftmost free space."""


    # Compact the disk
    while layout.count('.'):
        # Find the leftmost free space
        pos = layout.index('.')
        # Remove the rightmost file block
        n = layout.pop()
        # Move it to the free space
        layout[pos] = n

        # Remove trailing free space
        while layout and layout[-1] == '.':
            layout.pop()

    #print(f"Compacted Layout: {''.join(map(str, layout))}")

    return calc_checksum(layout)

def find_free_space(layout, file_length):
    """
    Find the first free space large enough to store a file of the given length.
    """
    start = None
    count = 0

    for i, block in enumerate(layout):
        if block == '.':
            if start is None:
                start = i
            count += 1
            if count >= file_length:
                return start  # Found a suitable span
        else:
            # Reset if we encounter a non-free space
            start = None
            count = 0

    return None  # No suitable span found

# Main

disk = aoc.input_string(sys.argv[1])
with open(sys.argv[1], "r") as f:
    disk = f.read().strip()

# Construct the initial layout (files and free spaces)
layout = []
for i in range(len(disk)):
    if i % 2:
        ch = '.'
    else:
        ch = i // 2
    layout.extend([ch] * int(disk[i]))

initial_layout = layout.copy()

print(f"Initial Layout: {''.join(map(str, layout))}")

print('Part 1:', compact_disk_1(layout))

# Part 2

layout = initial_layout

# Test find_free_space
file_length = 3
free_space_start = find_free_space(layout, file_length)
print(f"First free space large enough for file of length {file_length}: {free_space_start}")

# TODO: Implement the rest of Part 2
