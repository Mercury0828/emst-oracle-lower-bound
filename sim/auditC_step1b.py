"""
Step 1b: For each candidate layout, measure not just coverage but the PACKING DENSITY:
  - total cell area = m * s^2
  - bounding-box area = W * H of the domain
  - density = m*s^2 / bbox_area  (Ms <= O(n) <=> density <= O(1) when bbox ~ n)
Also report the max x-projection multiplicity (how many cells share any vertical line)
and max y-projection multiplicity. Disjoint-projection => both = 1.

The solver's Step-1 claim: O(1) coverage  =>  disjoint projections  =>  Ms <= O(n).
We test: does ANY O(1)-coverage layout have density growing with m (Ms >> n)?
"""
from __future__ import annotations
import math
import numpy as np
from auditC_step1 import (max_coverage, layout_grid, layout_permutation,
                          layout_random_xy, layout_blocks_of_permutations,
                          layout_hierarchical)


def projection_multiplicity(origins, s):
    """Max number of cells whose x-interval [ox, ox+s] overlaps a common vertical line,
    and same for y. A sweep-line max-overlap count."""
    def max_overlap(intervals):
        events = []
        for a, b in intervals:
            events.append((a, 1)); events.append((b, -1))
        events.sort(key=lambda e: (e[0], -e[1]))
        cur = best = 0
        for _, d in events:
            cur += d; best = max(best, cur)
        return best
    xint = [(o[0], o[0]+s) for o in origins]
    yint = [(o[1], o[1]+s) for o in origins]
    return max_overlap(xint), max_overlap(yint)


def density(origins, s):
    o = np.array(origins)
    W = (o[:,0].max()+s) - o[:,0].min()
    H = (o[:,1].max()+s) - o[:,1].min()
    bbox = W * H
    total_cell_area = len(origins) * s * s
    return total_cell_area / bbox, bbox, total_cell_area


def report(name, origins, s, p=16):
    mc = max_coverage(origins, s, p, n_snap=8000)
    xm, ym = projection_multiplicity(origins, s)
    dens, bbox, tca = density(origins, s)
    print(f"{name:34s} m={len(origins):4d} maxcov={mc:3d} "
          f"xproj_mult={xm:3d} yproj_mult={ym:3d} density={dens:.3f}")


if __name__ == "__main__":
    print("layout                              m   maxcov  xproj  yproj  density")
    for side in (6, 10):
        o, s = layout_grid(side); report("grid", o, s)
    for m in (64, 144):
        o, s = layout_permutation(m, seed=1); report("permutation", o, s)
    for m in (64, 144):
        span = math.sqrt(m)*1.05
        o, s = layout_random_xy(m, span, seed=2); report("random_xy", o, s)
    for B in (2, 4, 8):
        o, s = layout_blocks_of_permutations(B, 8, gap=2, seed=3)
        report(f"blocks(B={B})", o, s)
    for levels, branch in [(2,4),(3,3),(3,4)]:
        o, s = layout_hierarchical(levels, branch)
        report(f"hierarchical(L={levels},b={branch})", o, s)
