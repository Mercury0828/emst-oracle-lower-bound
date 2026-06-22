"""
Task 3g (THE decisive lower-bound test): does the small-lambda filament yield a
constant-factor HARD PAIR indistinguishable in o(sqrt n) range-counting queries?

The slab/box estimators FAIL on the small-lambda diagonal (cost ~sqrt(n)). But failure of
TWO particular primitives is NOT a lower bound. A lower bound needs: two instances A, B with
  - w(MST(A)) and w(MST(B)) differing by a constant factor (so a (1+-eps) estimator must
    distinguish them), AND
  - indistinguishable by any o(sqrt n) range-counting queries (a hitting/measure argument).

We probe the analogue of the round2 'tile-or-blowup vise' for the small-lambda filament:

  A = small-lambda diagonal filament: M=n/lam lonely singletons on y=x, persist lam each,
      Sum persistence ~ M*lam = Theta(n).
  B = SAME M points but PAIRED UP / clustered: place them as M/2 PAIRS (two points lam/10
      apart), pairs still lam apart on the diagonal. Now each pair is a 2-point component
      persisting ~lam, BUT there are only M/2 components -> persistence ~ (M/2)*lam = Theta(n)/2.
      => w(MST(B)) differs from w(MST(A)) by a constant fraction (the lonely term halves).

  The HARD-PAIR question: are A and B indistinguishable in o(sqrt n) queries? The DIFFERENCE
  between A and B is LOCAL (within each lam-cell: 1 point vs 2 points). To detect it a query
  must RESOLVE occupancy 1 vs 2 inside a lam-cell on the diagonal. There are M=n/lam such cells;
  a random localized probe hits a *specific* cell w.p. ~ lam/Delta-ish.

  We test numerically:
   (1) w(MST(A)) vs w(MST(B)) constant-factor gap? (exact EMST)
   (2) Are the coarse-grid signatures of A and B IDENTICAL (same mass everywhere) => coarse
       grid cannot distinguish? (A and B have the SAME number of points in every region down
       to the lam-cell, differing only in WHERE within a cell -> same range counts for any
       box aligned to >= lam.)  If coarse counts identical, distinguishing needs sub-lam probes
       at the right cells => hitting argument => Omega(#cells^{1/2}) = Omega(sqrt(M)) = sqrt(n/lam).
       For lam=polylog: Omega(sqrt(n)/polylog) ~ Omega(sqrt n).  THAT WOULD BE A sqrt(n) LB.

  CRUX CHECK: do A and B actually have the SAME range counts at scale >= lam (the U-B1
  concealment), making them a valid hard pair? We measure max count-difference over many
  random boxes of various sizes.
"""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "sim"))
import numpy as np
from emst import emst_weight
from scipy.spatial import cKDTree


def build_A(n, lam):
    """M = n/lam lonely singletons on y=x, pairwise lam."""
    M = int(round(n/lam)); M = min(M, n)
    islands = np.array([(k*lam+lam/2, k*lam+lam/2) for k in range(M)], dtype=float)
    return islands, M


def build_B(n, lam, M_A):
    """
    Same total #points = M_A, but as PAIRS: M_A/2 pairs, each pair = two points lam/10 apart,
    pairs lam apart on the diagonal. Occupies M_A/2 cells (2 pts each) vs A's M_A cells (1 each).
    To keep SAME #points AND same per-cell mass for the hard pair we instead do:
      A: one point per cell, cells 0..M-1 (M cells).
      B: two points in cell 2j, zero in cell 2j+1, for j=0..M/2-1 (still M points, M/2 occupied cells).
    Then A and B have the SAME total mass but DIFFERENT occupied-cell pattern. The range counts
    of any box spanning >= 2 cells are EQUAL (both contain the same total). Boxes of size < lam
    aligned to a single cell DIFFER (occ 1 vs occ 0/2).
    """
    pts = []
    half = M_A//2
    for j in range(half):
        c = (2*j)*lam  # cell 2j gets two points
        pts.append((c+lam/2-lam/20, c+lam/2-lam/20))
        pts.append((c+lam/2+lam/20, c+lam/2+lam/20))
    pts = np.array(pts, dtype=float)
    return pts


def random_box_count_diff(A, B, lam, n_boxes=3000, sizes=(1,2,4), seed=0):
    """Max |count_A - count_B| over random axis-aligned boxes of side size*lam covering the line."""
    rng = np.random.default_rng(seed)
    tA = cKDTree(A); tB = cKDTree(B)
    lo = min(A.min(), B.min()); hi = max(A.max(), B.max())
    worst = {}
    for sz in sizes:
        w = sz*lam; md = 0
        for _ in range(n_boxes):
            x0 = rng.uniform(lo-lam, hi); y0 = rng.uniform(lo-lam, hi)
            cA = len(tA.query_ball_point([x0+w/2, y0+w/2], r=w/2, p=np.inf))
            cB = len(tB.query_ball_point([x0+w/2, y0+w/2], r=w/2, p=np.inf))
            md = max(md, abs(cA-cB))
        worst[sz] = md
    return worst


def main():
    n = 4096
    print(f"=== Task 3g: small-lambda hard-PAIR test (n={n}, sqrt(n)={np.sqrt(n):.1f}) ===\n")
    print(f"{'lam':>6} {'M':>6} {'w(A)lonely':>11} {'w(B)paired':>11} {'gap':>9} {'gap/w(B)':>9}")
    res = {}
    for lam in [4.0, 8.0, 16.0, 32.0, 64.0]:
        A, M = build_A(n, lam)
        B = build_B(n, lam, M)
        wA = emst_weight(A); wB = emst_weight(B)
        res[lam] = (A, B, M)
        print(f"{lam:>6.0f} {M:>6} {wA:>11.1f} {wB:>11.1f} {wA-wB:>9.1f} {(wA-wB)/wB:>9.3f}")

    print()
    print("=== are A and B indistinguishable by boxes of side >= lam? (count differences) ===")
    print(f"{'lam':>6} | max|cA-cB| at box side 1*lam, 2*lam, 4*lam")
    for lam in [4.0, 8.0, 16.0, 32.0, 64.0]:
        A, B, M = res[lam]
        wdiff = random_box_count_diff(A, B, lam)
        print(f"{lam:>6.0f} | side1lam:{wdiff[1]:>3}  side2lam:{wdiff[2]:>3}  side4lam:{wdiff[4]:>3}")

    print()
    print("READING:")
    print(" If w(A) vs w(B) differ by a CONSTANT fraction (gap/w(B) ~ const), and boxes of")
    print(" side >= lam give |cA-cB| = 0 (counts identical at scale >= lam), then A,B are a")
    print(" valid constant-factor hard pair distinguishable only by sub-lam-resolution probes")
    print(" at the right cells. #cells to resolve = M = n/lam. A localized probe of side ~lam")
    print(" at a uniformly random spot hits a SPECIFIC distinguishing cell w.p. ~ 1/M, and the")
    print(" A vs B difference is SPREAD over M/2 cells, so a hitting/Chernoff argument gives")
    print(" Omega(sqrt(M)) = Omega(sqrt(n/lam)) queries.  For lam=O(polylog): ~Omega(sqrt n).")
    print(" -> THAT would be a genuine sqrt(n) lower bound, contradicting U-P1's optimism.")
    print(" BUT: check side1lam differences -- if they are NONZERO even at side>=lam, the pair")
    print(" is COARSELY distinguishable and NOT hard. The numbers decide.")


if __name__ == "__main__":
    main()
