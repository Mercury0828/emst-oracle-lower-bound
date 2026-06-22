"""
Step 6 hard probe: the 'new primitive'. Search for an equal-cardinality (heavy, sparse) pair
in a side-s cell that simultaneously has
   (A) large EMST gap  ~ s sqrt p, and
   (B) SMALL max axis-aligned rectangle count-discrepancy (ideally O(1), at least o(sqrt p)).
If (A)&(B) co-achievable -> the primitive exists -> the obstruction has a hole.
If every large-gap pair has discrepancy >= Omega(sqrt p) -> primitive looks impossible.

We try increasingly clever 'sparse' designs against heavy = k x k grid (gap target ~ s sqrt p
means sparse must be ~1D / low-EMST). We also try a RANDOMIZED sparse to see if averaging helps
the marginal-match while keeping low EMST. And we test the converse: a low-discrepancy pair's gap.
"""
from __future__ import annotations
import math
import numpy as np
import sys
sys.path.insert(0, ".")
from emst import emst_weight


def heavy(s, k):
    lo, hi = 0.05*s, 0.95*s
    xs = np.linspace(lo, hi, k); ys = np.linspace(lo, hi, k)
    gx, gy = np.meshgrid(xs, ys)
    return np.column_stack([gx.ravel(), gy.ravel()])


def max_rect_discrepancy(H, S, n_snap=8000, seed=0):
    allp = np.vstack([H, S])
    xs = np.unique(allp[:,0]); ys = np.unique(allp[:,1])
    xmid = (xs[:-1]+xs[1:])/2 if len(xs)>1 else xs
    ymid = (ys[:-1]+ys[1:])/2 if len(ys)>1 else ys
    rng = np.random.default_rng(seed)
    ax = np.sort(rng.choice(xmid,(n_snap,2)),axis=1); ay = np.sort(rng.choice(ymid,(n_snap,2)),axis=1)
    md = 0
    for t in range(n_snap):
        a,b,c,d = ax[t,0],ax[t,1],ay[t,0],ay[t,1]
        dh = np.sum((H[:,0]>=a)&(H[:,0]<=b)&(H[:,1]>=c)&(H[:,1]<=d))
        ds = np.sum((S[:,0]>=a)&(S[:,0]<=b)&(S[:,1]>=c)&(S[:,1]<=d))
        md = max(md, abs(dh-ds))
    return md


def designs(s, k):
    p = k*k
    lo, hi = 0.05*s, 0.95*s
    out = {}
    # strip
    out['strip'] = np.column_stack([np.linspace(lo,hi,p), np.full(p,0.5*s)])
    # monotone diagonal (matches 1D marginals)
    vals = np.linspace(lo,hi,k)
    out['monotone_diag'] = np.column_stack([np.sort(np.repeat(vals,k)), np.sort(np.repeat(vals,k))])
    # 'staircase blocks': sqrt(p) short vertical strips spread in x (try to mimic heavy x-spread
    #  while staying low EMST). Each column has k points stacked -> EMST ~ s per column * k cols? high.
    cols = []
    for i,xv in enumerate(np.linspace(lo,hi,k)):
        cols.append(np.column_stack([np.full(k,xv), np.linspace(lo,hi,k)]))
    out['full_grid_is_heavy_skip'] = None  # placeholder
    del out['full_grid_is_heavy_skip']
    # 'thin double strip' two rows
    half=p//2
    out['two_strips'] = np.vstack([
        np.column_stack([np.linspace(lo,hi,half), np.full(half,0.4*s)]),
        np.column_stack([np.linspace(lo,hi,p-half), np.full(p-half,0.6*s)]),
    ])
    # 'L-shape': spread along x AND a little y -> partial marginal match, lower discrepancy?
    out['Lshape'] = np.vstack([
        np.column_stack([np.linspace(lo,hi,k), np.full(k,lo)]),
        np.column_stack([np.full(p-k,lo), np.linspace(lo,hi,p-k)]),
    ])
    return out


if __name__ == "__main__":
    s = 1.0
    print(" k   p    design          EMST_gap/(s*sqrt(p))   max_rect_discrep   discrep/sqrt(p)")
    for k in (6, 10, 14):
        p = k*k
        H = heavy(s, k); eh = emst_weight(H)
        for name, S in designs(s, k).items():
            es = emst_weight(S)
            gap = abs(eh-es)/(s*math.sqrt(p))
            md = max_rect_discrepancy(H, S)
            print(f" {k:2d} {p:4d}  {name:14s}   {gap:6.3f}                {md:4d}            {md/math.sqrt(p):.3f}")
        print()
