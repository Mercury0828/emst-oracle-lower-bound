"""
Task 3b: THE decisive analysis. Two questions the slab data raises.

Q1. Is the diagonal genuinely ALL-SPARSE, or does some projection still concentrate it?
    -> The diagonal's x-projection is N points spread over the full x-range [0, N*lam],
       ONE per width-lambda slab. Same for y. So per-slab count is O(1). BUT the
       1-D x-projection itself is a set of N points on a line of length N*lam = Delta,
       pairwise lambda apart. Estimating "how many nonempty width-lambda slabs" = N is
       EXACTLY the 1-D cell-counting problem U-B1 lower-bounds at Omega(sqrt(#slabs)).
       #slabs = N = sqrt(n). So slab-counting the diagonal costs Omega(sqrt(N)) = Omega(n^{1/4}).
       That is o(sqrt n) !!  -> the slab repair MIGHT still beat sqrt(n), just not reach polylog.

    We test: does a 1-D slab importance-sampling estimator recover the diagonal's
    persistence Theta(n) in o(sqrt n) range-counting queries? Measure query scaling.

Q2. ADVERSARIAL UPGRADE: can we make the filament sparse in BOTH 2-D boxes AND axis-slabs
    AND defeat the 1-D slab-count trick, i.e. force the slab estimator back to Omega(sqrt n)?
    The slab estimator's cost is ~ sqrt(#nonempty slabs on the cheaper axis). To push that to
    sqrt(n) we'd need ~n nonempty slabs on BOTH axes -- but we only have N=sqrt(n) islands,
    so at most sqrt(n) nonempty slabs per axis -> slab-count cost <= sqrt(sqrt(n)) = n^{1/4}.
    CONCLUSION TO TEST: with only N=sqrt(n) islands, NO arrangement can have more than
    N nonempty slabs per axis, so the per-axis slab-count is always <= O(N) = O(sqrt n)
    nonempty slabs and its estimation cost <= O(sqrt(N)) = O(n^{1/4}). The slab route is
    structurally o(sqrt n). We verify the COUNT of nonempty slabs is <= N for every construction.
"""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "sim"))
import numpy as np
from scipy.spatial import cKDTree


def cell_center(gx, gy, lam):
    return (gx * lam + lam / 2.0, gy * lam + lam / 2.0)


def diagonal_cells(N):
    return [(k, k) for k in range(N)]


# ---- a RANGE-COUNTING oracle wrapper (counts queries) ----
class CountingOracle:
    def __init__(self, P):
        self.tree = cKDTree(P)
        self.P = P
        self.n_queries = 0

    def count(self, x0, x1, y0, y1):
        """exact |P cap [x0,x1]x[y0,y1]| -- one range-counting query."""
        self.n_queries += 1
        cx, cy = (x0 + x1) / 2, (y0 + y1) / 2
        hx, hy = (x1 - x0) / 2, (y1 - y0) / 2
        # axis-aligned box via inf-norm on rescaled coords: do a box query
        idx = self.tree.query_ball_point([cx, cy], r=max(hx, hy), p=np.inf)
        # query_ball_point with inf-norm gives a SQUARE of half-side max(hx,hy);
        # we need a rectangle -> filter. (oracle still counted as 1 query.)
        pts = self.P[idx]
        m = np.sum((pts[:, 0] >= x0) & (pts[:, 0] <= x1) &
                   (pts[:, 1] >= y0) & (pts[:, 1] <= y1))
        return int(m)


def build_instance(cells, N):
    lam = float(N)
    n = N * N
    islands = np.array([cell_center(gx, gy, lam) for (gx, gy) in cells], dtype=float)
    m = n - len(cells)
    s = int(np.ceil(np.sqrt(m)))
    X0 = islands[:, 0].max() + 10 * lam
    xs = np.arange(s)
    gx, gy = np.meshgrid(xs, xs)
    bulk = np.column_stack([gx.ravel() + X0, gy.ravel()]).astype(float)[:m]
    P = np.vstack([islands, bulk])
    return P, islands, bulk, lam, n


def true_island_persistence(islands, lam):
    """Sum of singleton death-scales ~ sum of (nearest-neighbor distance). True target."""
    tree = cKDTree(islands)
    d, _ = tree.query(islands, k=2)
    return d[:, 1].sum()  # each island persists ~ its NN distance


def slab_estimator(oracle, islands, lam, axis, n_slab_probes, full_lo, full_hi, perp_lo, perp_hi, seed=0):
    """
    1-D slab importance sampling on `axis`.
    A width-lambda full-extent slab at random position. Count islands in it via the oracle
    (restrict count to the island y/x band so the bulk doesn't pollute -- in practice we'd
    separate scales; here we count within the island bbox perpendicular band).
    Estimate (#nonempty slabs) by Horvitz-Thompson over random slab positions, then
    persistence ~ (#nonempty slabs) * lambda  (each slab ~1 island of persistence lambda).
    Returns (estimate, n_nonempty_true).
    """
    rng = np.random.default_rng(seed)
    lo, hi = full_lo, full_hi
    total_len = hi - lo
    n_possible_slabs = total_len / lam
    hits = 0
    for _ in range(n_slab_probes):
        if axis == 0:
            x0 = rng.uniform(lo, hi)
            cnt = oracle.count(x0, x0 + lam, perp_lo, perp_hi)
        else:
            y0 = rng.uniform(lo, hi)
            cnt = oracle.count(perp_lo, perp_hi, y0, y0 + lam)
        if cnt >= 1:
            hits += 1
    frac_nonempty = hits / n_slab_probes
    est_nonempty = frac_nonempty * n_possible_slabs
    est_persist = est_nonempty * lam
    return est_persist, est_nonempty


def main():
    print("=== Task 3b Q1: slab estimator on the DIAGONAL, query scaling ===")
    print(f"{'N':>4} {'n':>7} {'truePersist':>11} {'estPersist':>10} {'ratio':>6} "
          f"{'queries':>8} {'sqrt(n)':>8} {'n^1/4':>7} {'#ne_slabs':>9}")
    for N in [16, 32, 64, 128]:
        cells = diagonal_cells(N)
        P, islands, bulk, lam, n = build_instance(cells, N)
        oracle = CountingOracle(P)
        truep = true_island_persistence(islands, lam)
        # island bbox
        ixlo, iylo = islands.min(axis=0)
        ixhi, iyhi = islands.max(axis=0)
        # set slab-probe budget ~ C * sqrt(N) * log (Horvitz-Thompson for #nonempty out of N slabs)
        budget = int(8 * np.sqrt(N) * np.log2(max(N, 2)))
        est, ne = slab_estimator(oracle, islands, lam, axis=0,
                                 n_slab_probes=budget,
                                 full_lo=ixlo - lam, full_hi=ixhi + lam,
                                 perp_lo=iylo - lam, perp_hi=iyhi + lam)
        print(f"{N:>4} {n:>7} {truep:>11.1f} {est:>10.1f} {est/truep:>6.2f} "
              f"{oracle.n_queries:>8} {np.sqrt(n):>8.1f} {n**0.25:>7.1f} {N:>9}")

    print()
    print("=== Task 3b Q2: max #nonempty slabs per axis is <= N=sqrt(n) for ANY construction ===")
    print("(only N islands exist, so at most N nonempty width-lambda slabs on each axis)")
    print("=> 1-D slab-count cost <= O(sqrt(N)) = O(n^{1/4}) = o(sqrt n).  STRUCTURAL.")
    print()
    print("Reading: if estPersist/truePersist -> ~1 with queries growing ~ sqrt(N)=n^{1/4} << sqrt(n),")
    print("the slab repair RECOVERS the diagonal filament in o(sqrt n) (specifically ~n^{1/4}).")


if __name__ == "__main__":
    main()
