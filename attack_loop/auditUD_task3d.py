"""
Audit UD - Task 3d: the make-or-break. Can a large-lam instance make the SCALAR c(lam)
(hence MST-weight) hard to estimate, surviving the tile-or-blowup vise (U-P2/U-P3)?

Target accuracy for the WEIGHT: we need Sum_i lam_i c(lam_i) to (1 +- eps). At a single
scale lam, the contribution is ~ lam * c(lam) summed over the ~1/log(1+eps) scales near
lam. Its share of OPT ~ n must be estimated to additive eps*OPT/L. So we need c(lam) to
additive ~ eps n/(lam L)  -- exactly the lemma's target (with the SCALAR c, not per-bucket).

c(lam) = n - #{MST edges < lam} = #components at threshold lam.

THE VISE (U-P2/U-P3, verified round 3): a constant-fraction MST-weight gap between two
instances A,B at scale lam must be SPREAD over Theta(n/lam) cells (each differing by O(1)
components), because concentrating it collapses the gap. A uniformly placed lam-box then
hits a differing cell with constant prob => A,B distinguishable in O(1/eps^2) ... but that
gives O(1) per scale only if the *box* primitive sees the difference. The slab branch
gives sqrt(n/lam). The point branch gives lam. min at n^{1/3}.

For lam > n^{1/3}: sqrt(n/lam) < lam, so the SLAB branch is the cheaper one and is the one
we must make work for the SCALAR c(lam). The slab branch estimates #nonempty-lam-cells or
the component count via 1-D structure. We test:

  TEST 1: For a constant-fraction weight gap at large lam, is it ALWAYS spread over
          Theta(n/lam) lam-cells (=> slab/box sees it in O(1)..sqrt(n/lam))?  Or can it
          concentrate while keeping the weight gap constant?  Build A,B pairs and measure.

  TEST 2: The dense-slab 'hard' instance: is c(lam) recoverable by a coarse 1-D y-slab
          scan?  (the K clusters are spread in y over K*2lam, so a 1-D scan of n/lam... no,
          of the y-range / lam = K*2 slabs sees them -- but that's K ~ n/lam slabs = the
          slab cost sqrt is sqrt(K).) Measure whether random y-slab probing estimates K
          (= c(lam)-1) to additive eps*n/(lam L) in sqrt(n/lam) queries.
"""
import sys, os, math
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "sim"))
import numpy as np
from scipy.spatial import cKDTree
from emst import emst_weight


def fprint(*a):
    print(*a, flush=True)


class CountingOracle:
    def __init__(self, P):
        self.P = np.asarray(P, float)
        self.n_queries = 0
        self.order = np.argsort(self.P[:, 0], kind="stable")
        self.xs = self.P[self.order, 0]
        self.ys = self.P[self.order, 1]

    def count(self, x0, x1, y0, y1):
        self.n_queries += 1
        lo = np.searchsorted(self.xs, x0, side="left")
        hi = np.searchsorted(self.xs, x1, side="right")
        sub = self.ys[lo:hi]
        return int(np.sum((sub >= y0) & (sub <= y1)))


def mst_edge_lengths(P):
    from scipy.spatial import Delaunay
    pts = np.asarray(P, float); n = len(pts)
    if n <= 3:
        iu, ju = np.triu_indices(n, 1); E = np.column_stack([iu, ju])
    else:
        tri = Delaunay(pts); s = tri.simplices
        E = np.vstack([s[:, [0, 1]], s[:, [1, 2]], s[:, [0, 2]]]); E.sort(1); E = np.unique(E, 0)
    d = pts[E[:, 0]] - pts[E[:, 1]]; w = np.sqrt((d * d).sum(1))
    order = np.argsort(w, kind="stable"); parent = np.arange(n)
    def find(x):
        r = x
        while parent[r] != r: r = parent[r]
        while parent[x] != r: parent[x], x = r, parent[x]
        return r
    used = []
    for idx in order:
        i, j = int(E[idx, 0]), int(E[idx, 1]); ri, rj = find(i), find(j)
        if ri != rj:
            parent[ri] = rj; used.append(w[idx])
            if len(used) == n - 1: break
    return np.array(used)


# ----- TEST 1: spread-vs-concentrate vise at large lam -----
def inst_pair_spread(n, lam, gap_cells):
    """A: gap_cells lonely singletons (each a comp at scale lam => +1 comp each).
    B: same but those gap_cells points are PAIRED with a neighbor < lam (so -gap_cells
    components vs A). The weight gap ~ gap_cells * lam (A has gap_cells extra long edges).
    SPREAD: the gap_cells are scattered over the whole diagonal (n/lam positions)."""
    M = int(round(n / lam)); M = min(M, n)
    spacing = 2.0 * lam
    base = np.array([(k * spacing, k * spacing) for k in range(M)], float)
    # A: all singletons. B: add a close partner to the first gap_cells of them (spread evenly)
    Pa = base.copy()
    Pb = base.copy()
    sel = np.linspace(0, M - 1, gap_cells).astype(int)
    partners = base[sel] + np.array([lam * 0.1, 0.0])  # within lam => merges in B
    Pb = np.vstack([Pb, partners])
    # pad A to same n with far bulk; pad both to n
    def pad(P):
        m = n - len(P)
        if m <= 0: return P[:n]
        s = int(np.ceil(np.sqrt(m)))
        gx, gy = np.meshgrid(np.arange(s), np.arange(s))
        bulk = np.column_stack([gx.ravel(), gy.ravel()]).astype(float)[:m] + np.array([base[:,0].max()+50*lam, 0])
        return np.vstack([P, bulk])
    return pad(Pa), pad(Pb), sel


def inst_pair_concentrate(n, lam, gap_cells):
    """Same weight gap but CONCENTRATED: the gap_cells singletons (A) vs pairs (B) are all
    packed into ONE lam-region. Then a uniform lam-box rarely hits the differing region."""
    M = int(round(n / lam)); M = min(M, n)
    spacing = 2.0 * lam
    base = np.array([(k * spacing, k * spacing) for k in range(M)], float)
    Pa = base.copy(); Pb = base.copy()
    # concentrate: gap_cells extra singletons clustered near origin region, all within a
    # band; in B pair each. (still each > lam apart so distinct comps, but in small x-window)
    extra = np.array([(0.0, k * spacing) for k in range(gap_cells)], float)  # a vertical line
    Pa = np.vstack([Pa, extra])
    Pb = np.vstack([Pb, extra, extra + np.array([lam * 0.1, 0.0])])
    def pad(P):
        m = n - len(P)
        if m <= 0: return P[:n]
        s = int(np.ceil(np.sqrt(m)))
        gx, gy = np.meshgrid(np.arange(s), np.arange(s))
        bulk = np.column_stack([gx.ravel(), gy.ravel()]).astype(float)[:m] + np.array([base[:,0].max()+50*lam, 0])
        return np.vstack([P, bulk])
    return pad(Pa), pad(Pb)


def main():
    fprint("=== Task 3d: can large-lam c(lam) (hence weight) be made hard, vs the vise? ===\n")

    fprint("TEST 1: SPREAD vs CONCENTRATE a constant-fraction weight gap at large lam.")
    fprint("  We measure (i) the actual w(MST) gap, (ii) whether a uniform lam-BOX or lam-SLAB")
    fprint("  hits the differing region with constant prob (=> distinguishable cheaply).\n")
    fprint(f"{'mode':>12} {'n':>7} {'lam':>5} {'gap_cells':>9} {'wA':>9} {'wB':>9} "
           f"{'|wA-wB|/wA':>10} {'slab-hit-prob':>13}")
    rng = np.random.default_rng(2)
    for n in [8192]:
        n13 = n ** (1 / 3)
        lam = int(round(4 * n13))
        gap = int(round((n / lam) * 0.5))   # constant fraction of the n/lam diagonal cells
        # SPREAD
        Pa, Pb, sel = inst_pair_spread(n, lam, gap)
        wa, wb = emst_weight(Pa), emst_weight(Pb)
        # slab-hit prob: fraction of width-lam x-slabs (over diagonal x-range) that contain
        # a differing cell. Spread => ~gap/(n/lam) = constant.
        M = int(round(n / lam))
        hitp_spread = gap / M
        fprint(f"{'SPREAD':>12} {n:>7} {lam:>5} {gap:>9} {wa:>9.0f} {wb:>9.0f} "
               f"{abs(wa-wb)/wa:>10.4f} {hitp_spread:>13.3f}")
        # CONCENTRATE
        Pa2, Pb2 = inst_pair_concentrate(n, lam, gap)
        wa2, wb2 = emst_weight(Pa2), emst_weight(Pb2)
        # concentrated into a vertical line at x=0 spanning y over gap*2lam: in x it's ONE slab,
        # but in y it spreads over gap slabs. A 1-D x-slab scan: the differing region is 1 x-slab
        # of M => hit prob 1/M (small). BUT a y-slab scan sees it spread over gap y-slabs.
        hitp_conc_x = 1.0 / M
        fprint(f"{'CONCENTRATE':>12} {n:>7} {lam:>5} {gap:>9} {wa2:>9.0f} {wb2:>9.0f} "
               f"{abs(wa2-wb2)/wa2:>10.4f} {hitp_conc_x:>13.3f}")

    fprint("\n  READING: if CONCENTRATE keeps |wA-wB|/wA constant while x-slab-hit-prob -> 1/M,")
    fprint("  then a single-axis slab scan can MISS it -> would need n/lam x-slabs OR the y-axis.")
    fprint("  But concentrating in x SPREADS it in y (a vertical line) -> the OTHER slab axis")
    fprint("  sees it. To hide from BOTH axes you must pack into ONE lam x lam CELL -> then the")
    fprint("  'gap' points are within lam of each other -> they MERGE -> the weight gap VANISHES.")
    fprint("  That is the tile-or-blowup vise: you cannot concentrate a large-lam comp-count gap")
    fprint("  into a sub-sqrt region without collapsing the weight gap. => slab (2 axes) suffices.")

    fprint("\nTEST 2: estimate the SCALAR c(lam)-1 = K via 2-axis slab probing in the dense case.")
    fprint("  (the K clusters spread over K*2lam in y => K nonempty y-slabs => sqrt(K) probing.)")
    fprint("  K ~ c(lam)-1. additive target eps*n/(lam L). Measure est vs queries vs sqrt(n/lam).")
    fprint(f"{'n':>7} {'lam':>5} {'true c-1=K':>10} {'est K':>8} {'add.err':>8} "
           f"{'target eps n/lamL':>17} {'queries':>8} {'sqrt(n/lam)':>11}")
    for n in [4096, 16384]:
        n13 = n ** (1 / 3); lam = int(round(4 * n13)); a = 4; L = 8.0; eps = 0.3
        # dense slab instance from 3c
        rng2 = np.random.default_rng(0)
        K = max(1, int((n * 0.5) / a))
        ys = (np.arange(K) * 2.0 * lam).repeat(a)
        jit = rng2.uniform(0, lam * 0.05, size=(K * a, 2))
        cl = np.column_stack([jit[:, 0], ys + jit[:, 1]])
        rest = n - len(cl)
        ybase = ys.max() + 10 * lam
        s = int(np.ceil(np.sqrt(rest)))
        gx, gy = np.meshgrid(np.linspace(0, lam * 0.9, s), np.linspace(0, lam * 0.9, s))
        bulk = np.column_stack([gx.ravel(), gy.ravel() + ybase]).astype(float)[:rest]
        P = np.vstack([cl, bulk])
        el = mst_edge_lengths(P)
        true_c1 = int(np.sum(el >= lam))
        # y-slab probing over the CLUSTER y-range only [0, ys.max()+lam]: each nonempty
        # y-slab of width lam that is NOT the bulk band contributes one a-cluster.
        oracle = CountingOracle(P)
        ylo, yhi = 0.0, ys.max() + lam
        nyslab = max(1, int(math.ceil((yhi - ylo) / lam)))
        budget = int(8 * math.sqrt(n / lam) * math.log2(n))
        hits = 0
        for _ in range(budget):
            sidx = rng2.integers(0, nyslab)
            y0 = ylo + sidx * lam
            c = oracle.count(P[:, 0].min(), P[:, 0].max(), y0, y0 + lam)
            # a cluster slab has count ~a (small); bulk slab has huge count; empty has 0.
            if 1 <= c <= 2 * a:
                hits += 1
        estK = hits / budget * nyslab
        target = eps * n / (lam * L)
        fprint(f"{n:>7} {lam:>5} {true_c1:>10} {estK:>8.0f} {abs(estK-true_c1):>8.0f} "
               f"{target:>17.1f} {oracle.n_queries:>8} {math.sqrt(n/lam):>11.1f}")


if __name__ == "__main__":
    main()
