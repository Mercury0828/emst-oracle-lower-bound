"""
Task 3d (THE crux): the small-lambda many-island filament that pushes the slab route
toward sqrt(n). Build it with exact EMST and measure (i)-(iv) + slab-count #nonempty.

Stratum: choose lambda = n^a with a in (0, 1/2). Islands M = n / lambda (persistence
budget M*lambda = n). Arrange them as a DIAGONAL-like monotone curve so:
  - consecutive ~ lambda apart (no blowup),
  - pairwise >= lambda,
  - both axis-projections spread over the full Delta = M*lambda = n.
Then #nonempty width-lambda slabs per axis = M = n/lambda (each island its own slab if
the diagonal is monotone and islands are lambda apart in each coordinate).
=> slab-count cost ~ sqrt(M) = sqrt(n/lambda) = sqrt(n)/sqrt(lambda).
For lambda = polylog, that's ~ sqrt(n)/polylog ~ sqrt(n)  => slab repair NEARLY fails.

BUT: a critical check. For the persistence to be Sum lambda c = Theta(n) we need the
islands to genuinely persist until scale ~lambda. With M = n/lambda singletons each
pairwise >= lambda, each persists ~lambda, total ~ M*lambda = n.  GOOD.

We MUST also verify the bulk + (n-Delta) bookkeeping: here #islands = M = n/lambda <= n,
and the rest n-M points are bulk. For small lambda, M can approach n (few bulk points).

We test for moderate n whether the DIAGONAL with lambda small (= a few units) gives:
  #nonempty slabs per axis = M  (so slab-count cost = sqrt(M)),
  while box-hit and consecutive-distance still good.
And we directly run the slab estimator and measure queries vs sqrt(n).
"""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "sim"))
import numpy as np
from emst import emst_weight
from scipy.spatial import cKDTree


class CountingOracle:
    def __init__(self, P):
        self.tree = cKDTree(P); self.P = P; self.n_queries = 0
    def count(self, x0, x1, y0, y1):
        self.n_queries += 1
        cx, cy = (x0+x1)/2, (y0+y1)/2
        idx = self.tree.query_ball_point([cx, cy], r=max((x1-x0)/2, (y1-y0)/2), p=np.inf)
        pts = self.P[idx]
        return int(np.sum((pts[:,0]>=x0)&(pts[:,0]<=x1)&(pts[:,1]>=y0)&(pts[:,1]<=y1)))


def build_small_lambda_diagonal(n, lam):
    """
    M = round(n/lam) islands on a monotone diagonal, consecutive offset (lam, lam) so
    pairwise>=lam and each occupies its own width-lam slab on BOTH axes.
    Bulk: remaining points as a dense block far away.
    """
    M = int(round(n / lam))
    M = min(M, n)
    islands = np.array([(k*lam + lam/2, k*lam + lam/2) for k in range(M)], dtype=float)
    m = n - M
    if m > 0:
        s = int(np.ceil(np.sqrt(m)))
        X0 = islands[:,0].max() + 10*lam
        xs = np.arange(s); gx, gy = np.meshgrid(xs, xs)
        bulk = np.column_stack([gx.ravel()+X0, gy.ravel()]).astype(float)[:m]
        P = np.vstack([islands, bulk])
    else:
        P = islands
    return P, islands, lam, M


def slab_nonempty_count(islands, lam, axis):
    coord = islands[:, axis]
    lo, hi = coord.min(), coord.max()
    nb = int(np.ceil((hi-lo)/lam)) + 2
    counts = np.zeros(nb, dtype=int)
    for c in coord:
        counts[int((c-lo)//lam)] += 1
    return int((counts>0).sum()), int(counts.max())


def slab_estimator_queries(oracle, islands, lam, budget, seed=0):
    rng = np.random.default_rng(seed)
    ixlo, iylo = islands.min(axis=0); ixhi, iyhi = islands.max(axis=0)
    lo, hi = ixlo-lam, ixhi+lam
    npos = (hi-lo)/lam
    hits = 0
    for _ in range(budget):
        x0 = rng.uniform(lo, hi)
        cnt = oracle.count(x0, x0+lam, iylo-lam, iyhi+lam)
        if cnt >= 1: hits += 1
    est_ne = hits/budget * npos
    return est_ne * lam, est_ne


def main():
    print("=== Task 3d: small-lambda diagonal -- does slab-count cost approach sqrt(n)? ===")
    n = 4096
    print(f" n = {n}, sqrt(n) = {np.sqrt(n):.1f}\n")
    print(f"{'lam':>6} {'M':>6} {'islMST':>9} {'islMST/n':>8} {'persist~Mlam':>12} "
          f"{'#ne_slab/ax':>11} {'slabcost~sqrt':>13} {'/sqrt(n)':>9} {'minPair/lam':>11}")
    for lam in [2.0, 4.0, 8.0, 16.0, 32.0, 64.0]:
        P, islands, lam_, M = build_small_lambda_diagonal(n, lam)
        imst = emst_weight(islands)
        tree = cKDTree(islands)
        d,_ = tree.query(islands, k=2); minpair = d[:,1].min()
        ne, mx = slab_nonempty_count(islands, lam, 0)
        slabcost = np.sqrt(ne)
        persist = M*lam
        print(f"{lam:>6.0f} {M:>6} {imst:>9.1f} {imst/n:>8.3f} {persist:>12.1f} "
              f"{ne:>11} {slabcost:>13.1f} {slabcost/np.sqrt(n):>9.3f} {minpair/lam:>11.3f}")

    print()
    print("=== run actual slab estimator at the WORST (small lam) and measure queries ===")
    print(f"{'lam':>6} {'M':>6} {'est/true':>9} {'queries':>8} {'sqrt(n)':>8} {'q/sqrt(n)':>10}")
    for lam in [2.0, 4.0, 8.0, 64.0]:
        P, islands, lam_, M = build_small_lambda_diagonal(n, lam)
        oracle = CountingOracle(P)
        ne_true, _ = slab_nonempty_count(islands, lam, 0)
        budget = int(8*np.sqrt(max(ne_true,2))*np.log2(max(ne_true,2)))
        true_persist = M*lam
        est, est_ne = slab_estimator_queries(oracle, islands, lam, budget)
        print(f"{lam:>6.0f} {M:>6} {est/true_persist:>9.3f} {oracle.n_queries:>8} "
              f"{np.sqrt(n):>8.1f} {oracle.n_queries/np.sqrt(n):>10.3f}")

    print()
    print("READING: as lam shrinks, M=n/lam grows, #nonempty slabs -> M -> n/lam,")
    print("slab-count cost sqrt(#ne) = sqrt(n/lam) -> sqrt(n) as lam->O(1).")
    print("So the slab repair's query cost is sqrt(n/lambda): GOOD for large-lambda (codex's")
    print("lam=sqrt(n) gives n^{1/4}), but DEGRADES to ~sqrt(n) for a small-lambda lonely stratum.")


if __name__ == "__main__":
    main()
