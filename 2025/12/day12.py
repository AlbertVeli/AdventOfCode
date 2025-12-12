#!/usr/bin/env python3

import sys
from dataclasses import dataclass

@dataclass(frozen=True)
class Variant:
    # rows: tuple of ints, one per row, LSB is x=0
    # w/h: bounding-box size
    rows: tuple
    w: int
    h: int

    def cells(self):
        return sum(r.bit_count() for r in self.rows)

class Shape:
    """
    One present shape with all unique rotations/reflections precomputed.
    Stored as Variants with row bitmasks (fast + compact + immutable).
    """

    def __init__(self, idx, grid):
        self.idx = idx
        self.grid = list(grid)
        self.variants = self._compute_variants()

    @staticmethod
    def _grid_to_points(grid):
        pts = []
        for y, row in enumerate(grid):
            for x, ch in enumerate(row):
                if ch == '#':
                    pts.append((x, y))
        return pts

    @staticmethod
    def _normalize_points(pts):
        pts = list(pts)
        minx = min(x for x, _ in pts)
        miny = min(y for _, y in pts)
        shifted = [(x - minx, y - miny) for x, y in pts]
        maxx = max(x for x, _ in shifted)
        maxy = max(y for _, y in shifted)
        w = maxx + 1
        h = maxy + 1
        return tuple(sorted(shifted)), w, h

    # Instance method
    def placements(self, W, H):
        """
        Return all placements that fit inside a W x H region.

        Each placement is:
          (y, placed_rows)

        where placed_rows is a tuple of ints (row bitmasks already shifted by x).
        This is ready for collision checks like:

            for dy, prow in enumerate(placed_rows):
                if board[y+dy] & prow: collision
        """
        out = []
        for v in self.variants:
            if v.w > W or v.h > H:
                continue
            max_x = W - v.w
            max_y = H - v.h

            shifted_by_x = [None] * (max_x + 1)
            for x in range(max_x + 1):
                shifted_by_x[x] = tuple(r << x for r in v.rows)

            for y in range(max_y + 1):
                for x in range(max_x + 1):
                    out.append((y, shifted_by_x[x]))
        return out


    @classmethod
    def _points_to_variant(cls, pts):
        norm_pts, w, h = cls._normalize_points(pts)
        rows = [0] * h
        for x, y in norm_pts:
            rows[y] |= (1 << x)
        return Variant(rows=tuple(rows), w=w, h=h)

    @classmethod
    def _rot90(cls, pts):
        pts = list(pts)
        _, w, _ = cls._normalize_points(pts)
        # (x,y) -> (y, w-1-x)
        return [(y, w - 1 - x) for x, y in pts]

    @classmethod
    def _flip_x(cls, pts):
        pts = list(pts)
        _, w, _ = cls._normalize_points(pts)
        # (x,y) -> (w-1-x, y)
        return [(w - 1 - x, y) for x, y in pts]

    def _compute_variants(self):
        base_pts = self._grid_to_points(self.grid)

        seen = set()
        out = []

        def add(pts):
            v = self._points_to_variant(pts)
            key = (v.w, v.h, v.rows)
            if key not in seen:
                seen.add(key)
                out.append(v)

        pts = base_pts
        for _ in range(4):
            add(pts)
            add(self._flip_x(pts))
            pts = self._rot90(pts)

        return tuple(out)

    def __repr__(self):
        dims = sorted({(v.w, v.h) for v in self.variants})
        return 'Shape(idx=%s, variants=%d, sizes=%s)' % (self.idx, len(self.variants), dims)


def parse_input(path):
    with open(path, 'r', encoding='utf-8') as f:
        lines = [ln.rstrip('\n') for ln in f]

    raw_shapes = {}
    regions = []

    i = 0
    # Shapes section
    while i < len(lines):
        ln = lines[i].strip()
        if not ln:
            i += 1
            continue
        if 'x' in ln and ':' in ln:
            break  # regions start
        if ln.endswith(':') and ln[:-1].isdigit():
            idx = int(ln[:-1])
            i += 1
            block = []
            while i < len(lines) and lines[i].strip():
                block.append(lines[i].strip())
                i += 1
            raw_shapes[idx] = block
        i += 1

    # Regions section
    while i < len(lines):
        ln = lines[i].strip()
        i += 1
        if not ln:
            continue
        dim, rest = ln.split(':', 1)
        w_s, h_s = dim.lower().split('x')
        W, H = int(w_s), int(h_s)
        counts = [int(x) for x in rest.split()]
        regions.append((W, H, counts))

    shapes = {idx: Shape(idx, grid) for idx, grid in raw_shapes.items()}
    return shapes, regions

def count_regions_part1(shapes, regions):
    # occupied cells per shape (invariant under transforms)
    cells = {}
    for i in shapes:
        cells[i] = shapes[i].variants[0].cells()

    ok = 0
    for W, H, counts in regions:
        n_presents = sum(counts)
        min_area = sum(counts[i] * cells[i] for i in range(len(counts)))

        if min_area > W * H:
            continue  # impossible
        if (W // 3) * (H // 3) >= n_presents:
            ok += 1   # guaranteed possible (each gets its own 3x3)
        else:
            print('Should not happen, in case we get here the puzzle is much harder')
            pass

    return ok

# It turned out all the computing of variants and placements
# was unnecessary for part 1, the real input because of the
# way the real input data was created. It could have been much
# harder if the shapes could intersect in more complex ways.
shapes, regions = parse_input(sys.argv[1])
print(count_regions_part1(shapes, regions))
