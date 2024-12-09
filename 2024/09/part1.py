import sys

def calc_checksum(disk_layout):
    return sum(c * i for i, c in enumerate(disk_layout) if isinstance(c, int))

def compact_disk():
    """Compact the disk while maintaining correct IDs."""
    # Read the disk map from the file

    # Construct the initial layout (files and free spaces)
    layout = []
    for i in range(len(disk)):
        if i % 2:
            ch = '.'
        else:
            ch = i // 2
        layout.extend([ch] * int(disk[i]))

    #print(f"Initial Layout: {''.join(map(str, layout))}")

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

    # Calculate checksum
    return calc_checksum(layout)

# Main

with open(sys.argv[1], "r") as f:
    disk = f.read().strip()

print('Part 1:', compact_disk())
