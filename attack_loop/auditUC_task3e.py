"""
Task 3e: reconcile the small-lambda slab cost with U-P2's 2D-box lonely-fraction primitive.

The small-lambda diagonal (Task 3d) made the SLAB-count cost ~ sqrt(n/lambda) -> sqrt(n).
BUT U-P2's primitive is NOT slab-based: it is a 2D lambda-BOX probe estimating the
lonely-FRACTION (fraction of occupied lambda-cells with occupancy 1). Question:

  For the small-lambda diagonal, does the 2D-box lonely-fraction primitive ALSO degrade,
  or does it stay cheap? If 2D boxes stay cheap there, then codex's filament obstruction
  is specifically about the lambda=sqrt(n) regime where 2D boxes are sparse (1/N hit) but
  slabs are cheap (n^{1/4}); and the small-lambda regime where slabs are expensive has
  CHEAP 2D boxes. If so, the TWO primitives are COMPLEMENTARY and cover all lambda.

We measure, for the SAME instance family (diagonal, varying lambda), BOTH:
  - 2D-box lonely hit-rate (U-P2 primitive): P(random lambda-box has occ==1 island) and
    the cost to estimate the lonely-fraction = 1/hit_rate (importance-sampling).
  - slab-count cost ~ sqrt(#nonempty slabs).

If for every lambda, min(2Dbox_cost, slab_cost) = o(sqrt n), the COMBINED primitive
(box for small lambda, slab for large lambda) beats sqrt(n) on the whole diagonal family.
"""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "sim"))
import numpy as np
from scipy.spatial import cKDTree


def build_small_lambda_diagonal(n, lam):
    M = int(round(n/lam)); M = min(M, n)
    islands = np.array([(k*lam+lam/2, k*lam+lam/2) for k in range(M)], dtype=float)
    m = n - M
    if m > 0:
        s = int(np.ceil(np.sqrt(m)))
        X0 = islands[:,0].max()+10*lam
        xs = np.arange(s); gx,gy = np.meshgrid(xs,xs)
        bulk = np.column_stack([gx.ravel()+X0, gy.ravel()]).astype(float)[:m]
        P = np.vstack([islands, bulk])
    else:
        P = islands
    return P, islands, M


def box_hit_rate(P, islands, lam, n_probes=40000, seed=1):
    """U-P2 primitive: random 2D lambda-box over the ISLAND active region; occ==1 hit."""
    rng = np.random.default_rng(seed)
    tree = cKDTree(P)
    ixlo, iylo = islands.min(axis=0); ixhi, iyhi = islands.max(axis=0)
    iset = set(map(tuple, islands.tolist()))
    hits = 0
    for _ in range(n_probes):
        cx = rng.uniform(ixlo, ixhi); cy = rng.uniform(iylo, iyhi)
        idx = tree.query_ball_point([cx, cy], r=lam/2, p=np.inf)
        if len(idx)==1 and tuple(P[idx[0]].tolist()) in iset:
            hits += 1
    return hits/n_probes


def slab_nonempty(islands, lam, axis=0):
    coord = islands[:,axis]; lo,hi = coord.min(), coord.max()
    nb = int(np.ceil((hi-lo)/lam))+2; counts = np.zeros(nb, dtype=int)
    for c in coord: counts[int((c-lo)//lam)] += 1
    return int((counts>0).sum())


def main():
    n = 4096
    sq = np.sqrt(n)
    print(f"=== Task 3e: box vs slab cost across lambda (DIAGONAL, n={n}, sqrt(n)={sq:.1f}) ===\n")
    print(f"{'lam':>6} {'M':>6} | {'boxHit':>8} {'boxCost~1/hit':>13} {'/sqrt(n)':>9} | "
          f"{'#ne_slab':>8} {'slabCost':>9} {'/sqrt(n)':>9} | {'min(b,s)/sqrt(n)':>16}")
    for lam in [2.0, 4.0, 8.0, 16.0, 32.0, 64.0]:
        P, islands, M = build_small_lambda_diagonal(n, lam)
        hit = box_hit_rate(P, islands, lam)
        boxcost = (1.0/hit) if hit>0 else float('inf')
        ne = slab_nonempty(islands, lam, 0)
        slabcost = np.sqrt(ne)
        mb = min(boxcost, slabcost)
        print(f"{lam:>6.0f} {M:>6} | {hit:>8.4f} {boxcost:>13.1f} {boxcost/sq:>9.3f} | "
              f"{ne:>8} {slabcost:>9.1f} {slabcost/sq:>9.3f} | {mb/sq:>16.3f}")

    print()
    print("INTERPRETATION:")
    print(" boxCost ~ 1/hit_rate (importance sampling needs ~1/hit probes to see one lonely island).")
    print(" For the DIAGONAL, the island active region is the bbox [0,M*lam]^2; islands lie on")
    print(" the y=x line, so a random 2D box in that bbox hits an island w.p. ~ (M boxes that")
    print(" contain an island) / (total M^2 boxes tiling the bbox) = M/M^2 = 1/M.")
    print(" So boxCost ~ M = n/lam: LARGE for small lam (1/box-hit ~ M=n/lam).")
    print(" And slabCost ~ sqrt(M) = sqrt(n/lam): also grows as lam shrinks but SLOWER.")
    print(" min(box,slab) = slab = sqrt(n/lam). For lam=polylog this is ~sqrt(n)/polylog ~ sqrt(n).")
    print()
    print(" => On the DIAGONAL, the BEST of {2D-box, slab} is the slab, cost sqrt(n/lam).")
    print("    A small-lam (lam=polylog) diagonal forces BOTH primitives to ~sqrt(n).")
    print("    THIS is the genuine all-sparse obstruction candidate -- NOT codex's lam=sqrt(n).")


if __name__ == "__main__":
    main()
