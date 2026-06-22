"""
Audit UD - Task 3e (clean, robust): the decisive large-lam weight-hardness question.

Goal: a constant-fraction MST-WEIGHT gap AT large lam that is HIDDEN from o(sqrt n)
range-counting => would give classification (C). We try hard to build one and check it
against the tile-or-blowup vise (U-P2/U-P3).

Construction of a genuine constant-fraction large-lam weight gap:
  A: M = n/lam ISOLATED clusters, each a tiny tight blob of 'a' points, placed on a
     diagonal with consecutive spacing 2*lam (so each blob is its own lam-component and
     connects to the rest by a ~2*lam MST edge). w(MST(A)) ~ M*(2lam) = 2n  [constant frac].
  B: HALF the blobs (every other one) are instead placed within lam of their neighbor, so
     they MERGE -> M/2 long edges removed -> w(MST(B)) ~ (M/2)*(2lam) = n. So |wA-wB|/wA ~ 1/2:
     a genuine constant-fraction gap concentrated in the long-edge (large-lam) stratum.

Then the hard-pair test: at box/slab side >= lam, is the A-vs-B difference SPREAD over
Theta(M)=Theta(n/lam) cells (=> a uniform lam-probe distinguishes in O(1/eps^2))?  Or can
it be hidden?  We measure max box-count difference at side >= lam, and the hit probability.
"""
import sys, os, math
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "sim"))
import numpy as np
from scipy.spatial import cKDTree
from emst import emst_weight


def fprint(*a):
    print(*a, flush=True)


def blob(cx, cy, a, lam, rng):
    return np.column_stack([cx + rng.uniform(0, lam * 0.02, a),
                            cy + rng.uniform(0, lam * 0.02, a)])


def build_A(n, lam, a, rng):
    M = max(2, int(round(n / (lam * a))))
    pts = []
    for k in range(M):
        pts.append(blob(k * 2.0 * lam, k * 2.0 * lam, a, lam, rng))
    P = np.vstack(pts)
    return P, M


def build_B(n, lam, a, rng):
    """Every other blob is moved to within ~lam/2 of its predecessor => merges (one fewer
    long edge). Same #points and SAME total per-(>=lam)-region mass as A except the moved
    blob now sits in its neighbor's lam-cell."""
    M = max(2, int(round(n / (lam * a))))
    pts = []
    for k in range(M):
        if k % 2 == 1:
            # merge into previous blob's cell: place within lam/2 of blob k-1
            cx = (k - 1) * 2.0 * lam + lam * 0.4
            cy = (k - 1) * 2.0 * lam + lam * 0.4
        else:
            cx = k * 2.0 * lam
            cy = k * 2.0 * lam
        pts.append(blob(cx, cy, a, lam, rng))
    P = np.vstack(pts)
    return P, M


def box_count_diff(A, B, lam, sizes, n_boxes, rng):
    tA = cKDTree(A); tB = cKDTree(B)
    lo = min(A.min(), B.min()); hi = max(A.max(), B.max())
    out = {}
    for sz in sizes:
        w = sz * lam; md = 0; nz = 0
        for _ in range(n_boxes):
            x0 = rng.uniform(lo - lam, hi); y0 = rng.uniform(lo - lam, hi)
            cA = len(tA.query_ball_point([x0 + w / 2, y0 + w / 2], r=w / 2, p=np.inf))
            cB = len(tB.query_ball_point([x0 + w / 2, y0 + w / 2], r=w / 2, p=np.inf))
            if cA != cB:
                nz += 1
            md = max(md, abs(cA - cB))
        out[sz] = (md, nz / n_boxes)
    return out


def main():
    fprint("=== Task 3e: constant-fraction large-lam weight gap vs the vise ===\n")
    rng = np.random.default_rng(0)
    fprint(f"{'n':>7} {'lam':>5} {'a':>3} {'M':>5} {'wA':>9} {'wB':>9} {'|wA-wB|/wA':>10} "
           f"{'n^1/3':>7}")
    pairs = {}
    for n in [8192, 32768]:
        n13 = n ** (1 / 3)
        lam = int(round(4 * n13))   # lam > n^{1/3}
        a = 2
        A, M = build_A(n, lam, a, rng)
        B, _ = build_B(n, lam, a, rng)
        wA, wB = emst_weight(A), emst_weight(B)
        pairs[n] = (A, B, lam, M)
        fprint(f"{n:>7} {lam:>5} {a:>3} {M:>5} {wA:>9.0f} {wB:>9.0f} "
               f"{abs(wA-wB)/wA:>10.3f} {n13:>7.1f}")

    fprint("\nHard-pair test: at box side >= lam, is the A-vs-B difference present & SPREAD?")
    fprint("(max count-diff per box, and FRACTION of random lam-boxes that see a difference)")
    fprint(f"{'n':>7} {'lam':>5} | side=1lam (maxdiff, hit-frac)  2lam   4lam")
    for n in [8192, 32768]:
        A, B, lam, M = pairs[n]
        d = box_count_diff(A, B, lam, sizes=(1, 2, 4), n_boxes=4000, rng=rng)
        fprint(f"{n:>7} {lam:>5} | "
               f"1lam=({d[1][0]},{d[1][1]:.3f})  2lam=({d[2][0]},{d[2][1]:.3f})  "
               f"4lam=({d[4][0]},{d[4][1]:.3f})")

    fprint("\nREADING:")
    fprint(" - If |wA-wB|/wA is a CONSTANT (~0.3-0.5) => genuine constant-fraction weight gap.")
    fprint(" - If a random lam-box (or 2lam) sees the A-vs-B difference with CONSTANT hit-frac,")
    fprint("   then O(1/eps^2) random lam-boxes distinguish A from B  =>  NOT a hard pair  =>")
    fprint("   the large-lam weight gap is COARSELY recoverable (slab/box) => classification (A/B),")
    fprint("   NOT (C). The vise holds: the gap is forced to spread over Theta(n/lam) cells.")
    fprint(" - To make hit-frac -> 0 you must concentrate the differing blobs into o(n/lam) cells,")
    fprint("   which (each blob worth ~lam) drops the weight gap to o(OPT) => no longer hard.")


if __name__ == "__main__":
    main()
