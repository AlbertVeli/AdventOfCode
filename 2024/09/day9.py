#!/usr/bin/env python3

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

# Functions for part 2

def find_free_space(length):
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
            if count >= length:
                return start  # Found a suitable span
        else:
            # Reset if we encounter a non-free space
            start = None
            count = 0

    return None  # No suitable span found


def find_last_file():
    """
    Find the ID of the last file in the layout.
    Returns the file ID and its starting index and length.
    """
    for i in range(len(layout) - 1, -1, -1):  # Traverse from right to left
        if isinstance(layout[i], int):  # Found a file block
            file_id = layout[i]
            start = layout.index(file_id)  # Find the first occurrence
            length = layout.count(file_id)  # Count the number of blocks
            return file_id, start, length
    return None, None, None  # No files found

def cleanup_layout_after_move(length):
    """
    Truncate the layout by removing `length` elements from the end,
    and then remove trailing '.' elements.
    """
    global layout
    # Truncate the layout
    layout = layout[:-length]

    # Remove trailing free spaces
    while layout and layout[-1] == ".":
        layout.pop()

    return layout

def move_files_in_order():
    """
    Attempt to move files starting from the last file to the first.
    Stops when all files have been processed, and no file can be moved.
    """
    global layout

    # Traverse file IDs in descending order
    file_ids = sorted(set(block for block in layout if isinstance(block, int)), reverse=True)

    for file_id in file_ids:
        # Find file start and length
        start = layout.index(file_id)
        length = layout.count(file_id)

        # Find a free space large enough for this file
        free_space_start = find_free_space(length)
        if free_space_start is not None and free_space_start < start:
            # Move the file
            layout[start:start + length] = ["."] * length
            layout[free_space_start:free_space_start + length] = [file_id] * length

    # Remove trailing free spaces
    while layout and layout[-1] == ".":
        layout.pop()

# Main

disk = aoc.input_string(sys.argv[1])

# Construct the initial layout
layout = []
for i in range(len(disk)):
    if i % 2:
        ch = '.'
    else:
        ch = i // 2
    layout.extend([ch] * int(disk[i]))

initial_layout = layout.copy()
print('Part 1:', compact_disk_1(layout))


# Part 2

#print(f"Initial Layout: {''.join(map(str, layout))}")

layout = initial_layout

move_files_in_order()

#print(f"Layout: {''.join(map(str, layout))}")
print('Part 2:', calc_checksum(layout))
