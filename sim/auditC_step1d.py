"""
Step 1d: The real escape hatch for Step 1.

Coverage = #cells whose heavy/sparse swap changes |P cap R|. A straddled cell is only
COVERED if the partial count differs between heavy and sparse. Could a cleverer per-cell
design make MOST straddling edges INVISIBLE (equal partial counts heavy vs sparse for
every vertical/horizontal cut), so that high projection-multiplicity packing still yields
O(1) coverage?

For a cell to be invisible to EVERY axis-aligned partial cut, the heavy and sparse point
sets must have the SAME 1-D marginal (x-marginal AND y-marginal) AND same joint count for
every rectangle. But heavy and sparse must differ in EMST (that's the whole point). Can a
heavy/sparse pair share BOTH x- and y-marginals (so every axis cut is invisible) yet differ
in EMST by Theta(s sqrt p)?  If YES -> Step 1 has a hole: pack densely, straddles invisible.

We TEST: design heavy = sqrt(p) x sqrt(p) grid; sparse = a point set with the SAME x- and
y- marginals (same multiset of x-coords and y-coords) but arranged to be low-EMST (a 'sorted'
/ monotone arrangement). Then measure (a) per-cell coverage under dense packing, (b) EMST gap.
"""
from __future__ import annotations
import math
import numpy as np
import sys
sys.path.insert(0, ".")
from emst import emst_weight


def heavy_grid(k, s):
    lo, hi = 0.05*s, 0.95*s
    xs = np.linspace(lo, hi, k); ys = np.linspace(lo, hi, k)
    gx, gy = np.meshgrid(xs, ys)
    return np.column_stack([gx.ravel(), gy.ravel()])


def sparse_same_marginals_monotone(k, s):
    """Same x-multiset and y-multiset as the k x k grid, but paired MONOTONICALLY:
    sort all points so that x increases with y -> they lie near the diagonal -> low-ish EMST?
    Actually to truly minimize EMST while keeping marginals we want a path. We construct a
    'sorted diagonal staircase' that uses each grid x-value and y-value exactly k times."""
    lo, hi = 0.05*s, 0.95*s
    vals = np.linspace(lo, hi, k)
    xm = np.repeat(vals, k)   # each x-value appears k times
    ym = np.repeat(vals, k)   # each y-value appears k times
    # pair them monotonically: sort xm asc, ym asc -> diagonal cluster (same marginals!)
    xm_sorted = np.sort(xm)
    ym_sorted = np.sort(ym)
    return np.column_stack([xm_sorted, ym_sorted])


def x_marginal(pts, s, nb=50):
    return np.histogram(pts[:,0], bins=nb, range=(0,s))[0]

def y_marginal(pts, s, nb=50):
    return np.histogram(pts[:,1], bins=nb, range=(0,s))[0]


def coverage_single_cell(heavy, sparse, s, n_cuts=400):
    """Max over axis-aligned half-plane / rect cuts of |#heavy in R - #sparse in R|>0 indicator,
    i.e. is the cell covered by SOME cut? Return the max count-difference and #distinguishing cuts."""
    xs = np.linspace(-0.1*s, 1.1*s, n_cuts)
    ys = np.linspace(-0.1*s, 1.1*s, n_cuts)
    maxdiff = 0; ndistinct = 0
    # vertical half-plane cuts x<=a
    for a in xs:
        dh = np.sum(heavy[:,0] <= a); ds = np.sum(sparse[:,0] <= a)
        if dh != ds: ndistinct += 1; maxdiff = max(maxdiff, abs(dh-ds))
    for b in ys:
        dh = np.sum(heavy[:,1] <= b); ds = np.sum(sparse[:,1] <= b)
        if dh != ds: ndistinct += 1; maxdiff = max(maxdiff, abs(dh-ds))
    # random rectangles
    rng = np.random.default_rng(0)
    for _ in range(4000):
        a,bb = sorted(rng.uniform(-0.1*s,1.1*s,2)); c,d = sorted(rng.uniform(-0.1*s,1.1*s,2))
        dh = np.sum((heavy[:,0]>=a)&(heavy[:,0]<=bb)&(heavy[:,1]>=c)&(heavy[:,1]<=d))
        ds = np.sum((sparse[:,0]>=a)&(sparse[:,0]<=bb)&(sparse[:,1]>=c)&(sparse[:,1]<=d))
        if dh != ds: ndistinct += 1; maxdiff = max(maxdiff, abs(dh-ds))
    return maxdiff, ndistinct


if __name__ == "__main__":
    s = 1.0
    print("k    p    emst_heavy   emst_sparse   gap/s/sqrt(p)   xmarg_equal ymarg_equal  maxcountdiff  rect_distinguishable?")
    for k in (4, 6, 8, 12, 16):
        p = k*k
        H = heavy_grid(k, s)
        S = sparse_same_marginals_monotone(k, s)
        eh = emst_weight(H); es = emst_weight(S)
        xeq = np.array_equal(np.sort(H[:,0].round(9)), np.sort(S[:,0].round(9)))
        yeq = np.array_equal(np.sort(H[:,1].round(9)), np.sort(S[:,1].round(9)))
        md, nd = coverage_single_cell(H, S, s)
        gapnorm = abs(eh-es)/(s*math.sqrt(p))
        print(f"{k:2d}  {p:4d}  {eh:9.4f}   {es:9.4f}   {gapnorm:9.4f}      {xeq}      {yeq}      {md:4d}     {nd>0}")
