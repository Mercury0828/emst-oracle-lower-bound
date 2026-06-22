"""
AuditC Step 1 probe: is O(1) coverage forcing disjoint projections / Ms <= O(n)?

We model 'coverage' of a rectangle R as the number of cells whose EXACT count |P cap R|
differs between the HIGH (heavy) and LOW (sparse) realization, with equal cardinality per cell.
A cell is "covered" by R iff R partially straddles it in a way that the heavy and sparse
counts differ. Key driver: a cell is straddled when an edge of R passes through the cell's
x-extent or y-extent (partial containment), AND the partial counts differ between heavy/sparse.

We test several candidate layouts that are NOT disjoint-projection, asking:
  can we keep max adversarial coverage O(1) while packing cells so that total cell area >> n
  (equivalently many cells share x- or y-projections)?

Each cell: heavy = k x k grid filling [0,s]^2; sparse = horizontal strip of p points.
We use the same machinery idea as c2_coverage but with arbitrary cell origins + sizes.
"""
from __future__ import annotations
import math
import numpy as np


def heavy_pts(origin, s, p):
    k = max(1, int(math.isqrt(p)))
    lo, hi = 0.05 * s, 0.95 * s
    xs = np.linspace(lo, hi, k); ys = np.linspace(lo, hi, k)
    gx, gy = np.meshgrid(xs, ys)
    pts = np.column_stack([gx.ravel(), gy.ravel()])[:k*k]
    return pts + np.array(origin)


def sparse_pts(origin, s, p):
    k = max(1, int(math.isqrt(p)))
    pcount = k * k  # match heavy cardinality exactly
    lo, hi = 0.05 * s, 0.95 * s
    xs = np.linspace(lo, hi, pcount)
    ys = np.full(pcount, 0.5 * s)
    return np.column_stack([xs, ys]) + np.array(origin)


def build(origins, s, p):
    hx, hc, sx, sc = [], [], [], []
    for k, o in enumerate(origins):
        h = heavy_pts(o, s, p); sp = sparse_pts(o, s, p)
        hx.append(h); hc.append(np.full(len(h), k))
        sx.append(sp); sc.append(np.full(len(sp), k))
    return np.vstack(hx), np.concatenate(hc), np.vstack(sx), np.concatenate(sc)


def counts(xy, cell, m, rect):
    x0, x1, y0, y1 = rect
    inside = (xy[:,0] >= x0) & (xy[:,0] <= x1) & (xy[:,1] >= y0) & (xy[:,1] <= y1)
    return np.bincount(cell[inside], minlength=m)


def coverage(pack, m, rect):
    hx, hc, sx, sc = pack
    ch = counts(hx, hc, m, rect); cs = counts(sx, sc, m, rect)
    return int(np.count_nonzero(ch != cs))


def adv_rects(pack, n_snap=20000, seed=7):
    hx, _, sx, _ = pack
    allp = np.vstack([hx, sx])
    xlo, xhi = allp[:,0].min()-1, allp[:,0].max()+1
    ylo, yhi = allp[:,1].min()-1, allp[:,1].max()+1
    xsnap = np.unique(allp[:,0]); ysnap = np.unique(allp[:,1])
    xmid = (xsnap[:-1]+xsnap[1:])/2 if len(xsnap)>1 else xsnap
    ymid = (ysnap[:-1]+ysnap[1:])/2 if len(ysnap)>1 else ysnap
    rects = []
    BIG = 1e12
    # half-planes sweeping all midpoints (single straddling edge)
    for a in xmid: rects.append((-BIG, a, -BIG, BIG))
    for b in ymid: rects.append((-BIG, BIG, -BIG, b))
    # slabs
    for i in range(0, len(xmid)-1):
        rects.append((xmid[i], xmid[min(i+3,len(xmid)-1)], -BIG, BIG))
    # snapped random 4-edge rectangles
    rng = np.random.default_rng(seed)
    ax = np.sort(rng.choice(xmid, size=(n_snap,2)), axis=1)
    ay = np.sort(rng.choice(ymid, size=(n_snap,2)), axis=1)
    for t in range(n_snap):
        rects.append((ax[t,0], ax[t,1], ay[t,0], ay[t,1]))
    return rects


def max_coverage(origins, s, p, n_snap=20000, seed=7):
    m = len(origins)
    pack = build(origins, s, p)
    rects = adv_rects(pack, n_snap=n_snap, seed=seed)
    best = 0
    for r in rects:
        c = coverage(pack, m, r)
        if c > best: best = c
    return best


# ---------- Candidate layouts ----------

def layout_grid(side, pitch=1.05, s=1.0):
    return [(i*pitch*s, j*pitch*s) for j in range(side) for i in range(side)], s

def layout_permutation(m, pitch=1.05, s=1.0, seed=0):
    rng = np.random.default_rng(seed)
    perm = rng.permutation(m)
    return [(k*pitch*s, perm[k]*pitch*s) for k in range(m)], s

def layout_random_xy(m, span, s=1.0, seed=0):
    """Random positions in a span x span box: x and y projections will collide a lot."""
    rng = np.random.default_rng(seed)
    return [(rng.uniform(0, span), rng.uniform(0, span)) for _ in range(m)], s

def layout_blocks_of_permutations(B, perm_size, gap, s=1.0, seed=0):
    """B separated diagonal blocks, each a permutation block of perm_size cells.
    Blocks stacked along the diagonal but SHIFTED so x-projections of different blocks
    overlap (reuse x-range) -> tests whether reusing x-projection across blocks raises coverage."""
    rng = np.random.default_rng(seed)
    origins = []
    for b in range(B):
        perm = rng.permutation(perm_size)
        for k in range(perm_size):
            # all blocks use the SAME x-band [0, perm_size], different y-band
            origins.append((k*1.05*s, (b*(perm_size+gap) + perm[k])*1.05*s))
    return origins, s

def layout_hierarchical(levels, branch, s=1.0):
    """Fractal: a coarse permutation, each cell replaced by a finer permutation, etc.
    At each level cells share projections within their parent block."""
    # build recursively: positions normalized then scaled
    def rec(level, x0, y0, scale):
        if level == 0:
            return [(x0, y0)]
        out = []
        b = branch
        perm = list(range(b))
        # simple identity-ish permutation per block to maximize projection reuse? use staircase
        for k in range(b):
            nx = x0 + k * scale / b
            ny = y0 + perm[k] * scale / b
            out += rec(level-1, nx, ny, scale/b)
        return out
    return rec(levels, 0.0, 0.0, float(branch**levels)), s


if __name__ == "__main__":
    p = 16
    print("=== grid (baseline, expect ~sqrt(m)) ===")
    for side in (4, 6, 8, 10, 12):
        m = side*side
        o, s = layout_grid(side)
        print(f"m={m:4d}  maxcov={max_coverage(o, s, p)}")

    print("\n=== permutation (disjoint projections, expect O(1)) ===")
    for m in (16, 36, 64, 100, 144, 196):
        o, s = layout_permutation(m, seed=1)
        print(f"m={m:4d}  maxcov={max_coverage(o, s, p)}")

    print("\n=== random_xy in box of side ~sqrt(m) (projections collide) ===")
    for m in (16, 36, 64, 100, 144):
        span = math.sqrt(m) * 1.05
        o, s = layout_random_xy(m, span, seed=2)
        print(f"m={m:4d}  span={span:.1f}  maxcov={max_coverage(o, s, p)}")

    print("\n=== blocks of permutations (reuse x-band across blocks) ===")
    for B in (2, 4, 8):
        for ps in (8, 16):
            o, s = layout_blocks_of_permutations(B, ps, gap=2, seed=3)
            print(f"B={B} perm_size={ps} m={len(o):4d}  maxcov={max_coverage(o, s, p)}")

    print("\n=== hierarchical/fractal (projection reuse within blocks) ===")
    for levels, branch in [(2,4),(3,3),(2,6),(3,4)]:
        o, s = layout_hierarchical(levels, branch)
        print(f"levels={levels} branch={branch} m={len(o):4d}  maxcov={max_coverage(o, s, p)}")
