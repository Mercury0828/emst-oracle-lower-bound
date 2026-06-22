"""
Steps 5 & 6: the locality / bulk-parity obstruction, and the "new primitive".

Q5: Is "EMST = sum of O(1)-local terms (internal + adjacent-bridge)" valid in a spread-out
   (disjoint-projection) layout? If so, identical O(1)-cell marginals => no Theta(w) gap.
   We test the LOCALITY directly: in a spread permutation layout, does flipping cell i's
   state (sparse<->heavy) change w(P) by an amount that depends only on cell i (and its O(1)
   neighbors), independent of the states of FAR cells? If the per-cell increment is
   state-of-others-independent, EMST is a sum of local terms => Lipschitz => parity-invisible.

Q6: The "new primitive": a p-point cell whose heavy/sparse EMST gap ~ s sqrt p while EVERY
   axis-aligned rectangle's exact count is class-independent. We've seen monotone-diagonal
   matches 1-D marginals but NOT 2-D counts. Here we quantify HOW count-visible any large-gap
   pair must be: we search over sparse-cell designs for the one MINIMIZING max rectangle
   count-discrepancy vs the heavy grid, subject to a target EMST gap, and report the tradeoff.
"""
from __future__ import annotations
import math
import numpy as np
import sys
sys.path.insert(0, ".")
from emst import emst_weight


def heavy(origin, s, k):
    lo, hi = 0.05*s, 0.95*s
    xs = np.linspace(lo, hi, k); ys = np.linspace(lo, hi, k)
    gx, gy = np.meshgrid(xs, ys)
    return np.column_stack([gx.ravel(), gy.ravel()]) + np.array(origin)

def sparse(origin, s, k):
    lo, hi = 0.05*s, 0.95*s
    xs = np.linspace(lo, hi, k*k); ys = np.full(k*k, 0.5*s)
    return np.column_stack([xs, ys]) + np.array(origin)


def perm_origins(M, s, pitch=1.05, seed=0):
    rng = np.random.default_rng(seed)
    perm = rng.permutation(M)
    return [(i*pitch*s, perm[i]*pitch*s) for i in range(M)]


def build(origins, active, s, k):
    chunks = []
    for idx, o in enumerate(origins):
        chunks.append(heavy(o, s, k) if idx in active else sparse(o, s, k))
    return np.vstack(chunks)


def test_locality():
    """Increment of flipping cell i, measured against MANY random background states of others.
    If EMST were a pure sum of local terms, the increment would be CONSTANT (variance 0)."""
    s = 1.0; k = 5; M = 25
    origins = perm_origins(M, s, seed=2)
    rng = np.random.default_rng(7)
    target = 12  # the cell we flip
    incs = []
    for _ in range(40):
        others = set(i for i in range(M) if i != target and rng.random() < 0.5)
        w_off = emst_weight(build(origins, others, s, k))
        w_on = emst_weight(build(origins, others | {target}, s, k))
        incs.append(w_on - w_off)
    incs = np.array(incs)
    print(f"[locality] flip-increment of cell {target}: mean={incs.mean():.4f} "
          f"std={incs.std():.5f} min={incs.min():.4f} max={incs.max():.4f}")
    print(f"           => increment is {'CONSTANT (local/additive)' if incs.std()<1e-2 else 'state-dependent'} "
          f"in this spread layout")


def count_visibility_tradeoff():
    """For a single cell: heavy = k x k grid. Try several sparse designs spanning the
    EMST-gap range, and for each report the MAX rectangle count-discrepancy vs heavy.
    Tests Step-6 claim: large gap => coarsely count-visible (max discrepancy ~ Theta(p))."""
    s = 1.0
    print("\n[step6] per-cell: design -> EMST_gap/(s sqrt p),  max rect count-discrepancy vs heavy")
    for k in (6, 10):
        p = k*k
        H = heavy((0,0), s, k)
        eh = emst_weight(H)
        designs = {}
        # strip (classic sparse)
        designs['strip'] = sparse((0,0), s, k)
        # monotone diagonal (matches 1D marginals)
        vals = np.linspace(0.05*s, 0.95*s, k)
        xm = np.sort(np.repeat(vals, k)); ym = np.sort(np.repeat(vals, k))
        designs['monotone_diag'] = np.column_stack([xm, ym])
        # sqrt(p)/2 x sqrt(p)/2 denser sub-grid in half the cell (partial spread)
        kk = max(2, k//2)
        xs2 = np.linspace(0.05*s, 0.5*s, kk); ys2 = np.linspace(0.05*s, 0.95*s, (p+kk-1)//kk)
        gx, gy = np.meshgrid(xs2, ys2)
        half = np.column_stack([gx.ravel(), gy.ravel()])[:p]
        designs['half_grid'] = half
        for name, S in designs.items():
            es = emst_weight(S)
            gap = abs(eh - es) / (s*math.sqrt(p))
            # max rectangle count-discrepancy via snapped edges
            allp = np.vstack([H, S])
            xsnap = np.unique(allp[:,0]); ysnap = np.unique(allp[:,1])
            xmid = (xsnap[:-1]+xsnap[1:])/2; ymid = (ysnap[:-1]+ysnap[1:])/2
            rng = np.random.default_rng(0)
            maxd = 0
            ax = np.sort(rng.choice(xmid, (6000,2)), axis=1); ay = np.sort(rng.choice(ymid,(6000,2)),axis=1)
            for t in range(6000):
                a,b,c,d = ax[t,0],ax[t,1],ay[t,0],ay[t,1]
                dh = np.sum((H[:,0]>=a)&(H[:,0]<=b)&(H[:,1]>=c)&(H[:,1]<=d))
                ds = np.sum((S[:,0]>=a)&(S[:,0]<=b)&(S[:,1]>=c)&(S[:,1]<=d))
                maxd = max(maxd, abs(dh-ds))
            print(f"   k={k:2d} p={p:3d}  {name:14s} gap={gap:.3f}  maxcountdiscrep={maxd}  (p={p})")


if __name__ == "__main__":
    test_locality()
    count_visibility_tradeoff()
