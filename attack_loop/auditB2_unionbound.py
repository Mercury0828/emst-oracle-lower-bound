"""
Audit B round 2, PART 3: is "per-threshold marginal iid + union bound" a VALID
substitute for cross-threshold independence, when the FINAL answer SUMS over thresholds
with the SAME reused seeds?

Two DIFFERENT notions of "correct", and the proof needs the RIGHT one:

  (I)  Per-threshold w.h.p. correctness:  for each fixed t,  |hat_c(t) - c(t)| <= err(t)
       with prob >= 1 - 1/(10 T).  Union bound over T thresholds => ALL t correct
       simultaneously w.p. >= 0.9.   THEN deterministically the SUM/integral
       hat_S = sum_t hat_c(t) dt  satisfies  |hat_S - S| <= sum_t err(t) dt.
       This requires NO independence across thresholds -- it is a union bound on a
       deterministic functional of simultaneously-good estimates.

  (II) Variance of the SUM:  Var[sum_t hat_c(t) dt] = sum_{t,t'} Cov dt dt'.
       Reuse makes Cov(hat_c(t),hat_c(t')) > 0 (positive correlation).  If one tried
       to prove (1+/-eps) via Chebyshev on the SUM's variance, the cross-covariances
       matter and reuse could inflate variance by up to factor T.

The proof in sec 4 uses framing (I): "x O(log T) pool + medians => simultaneous
correctness at all thresholds by union bound; cross-threshold independence unnecessary."
So we must check: is (I) actually SUFFICIENT to make the SUM (1+/-eps)?

  KEY: (I) gives |hat_S - S| <= sum_t err(t) dt.  This is an L1 (worst-case additive)
  guarantee, NOT a variance/cancellation guarantee.  It is VALID *iff* the per-threshold
  additive errors err(t) are small enough that their (non-cancelling) SUM is <= eps*W.
  i.e. you need each err(t) dt to be a *charged-against-budget* additive piece whose
  TOTAL is eps*W.  This is exactly how sec 5/6 budget it: each threshold's bulk/tail
  estimate is additive ~eta*G, and they DON'T sum many thresholds of raw c -- they form
  TWO estimates (W_Q via Lemma3, A_L via clipped death-time) and subtract.  The "T
  thresholds" are the geometric LADDER inside Lemma 3 / inside the W-search, each
  individually additive-accurate.

This script STRESS-TESTS framing (I) vs (II) on a worst case for correlation: it builds
a per-threshold estimator with reused seeds and asks whether requiring per-threshold
err(t) (so total additive sum <= eps W) actually needs MORE samples under reuse than
under fresh -- i.e. whether reuse's positive correlation breaks the union-bound budget.

MODEL: estimate, for a K-vertex support graph H_Q, the survival counts at a geometric
ladder of T thresholds via r reused uniform seeds (CRT-style: hat_c(t)-1 = (K-1)*mean_j
1[tau(q_j)>t]).  Compare to fresh r seeds per threshold.  Measure:
   - max over t of |hat_c(t)-c(t)| / (K-1)            (the union-bound L-inf quantity)
   - |sum_t (hat_c(t)-1) dt - sum_t (c(t)-1) dt| / W  (the SUM error == |hat_W - W|/W)
under REUSE and FRESH at the SAME total seed budget B = r*T (fresh) vs r (reuse, but
note reuse only spends r!). To compare apples-to-apples on the SUM error we give REUSE
a budget r and FRESH a budget r (per threshold), i.e. fresh spends r*T total.
"""
import math, sys, os
import numpy as np
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'sim'))
from scipy.spatial import Delaunay


def mst_edge_weights(points):
    pts = np.asarray(points, float); n = len(pts)
    if n <= 3:
        cand = [(i, j) for i in range(n) for j in range(i + 1, n)]
    else:
        tri = Delaunay(pts); E = set()
        for s in tri.simplices:
            for a in range(3):
                for b in range(a + 1, 3):
                    i, j = int(s[a]), int(s[b]); E.add((min(i, j), max(i, j)))
        cand = list(E)
    we = sorted((math.dist(pts[i], pts[j]), i, j) for (i, j) in cand)
    parent = list(range(n))
    def find(x):
        while parent[x] != x:
            parent[x] = parent[parent[x]]; x = parent[x]
        return x
    w = []
    for wt, i, j in we:
        ri, rj = find(i), find(j)
        if ri != rj:
            parent[ri] = rj; w.append(wt)
            if len(w) == n - 1:
                break
    return np.array(w)


def make_support(n, L, rng):
    """A K=Theta(n^{2/3})-ish SUPPORT graph: snap a point cloud to a grid, take centers.
    We just use the cell-center MST as the 'support' H_Q whose weight we estimate."""
    pts = []
    m = n // 2; step = 0.4 * L; cols = max(2, int(math.isqrt(m)))
    x = y = 0.0; dirn = 1
    for i in range(m):
        pts.append((x, y)); x += dirn * step
        if (i + 1) % cols == 0:
            y += step; dirn *= -1
    base = np.array(pts)
    rest = n - len(base); k_islands = 8; per = max(1, rest // k_islands)
    cx = base[:, 0].max() + 2 * L
    isl = []
    for j in range(k_islands):
        occ = max(1, int(per * (0.3 + 1.4 * rng.random())))
        c = np.array([cx + (1.5 * L) * (2 ** j), (j % 3) * 3 * L])
        isl.append(c + rng.random((occ, 2)) * 0.3)
    P = np.vstack([base] + isl)
    # snap to grid h = 0.1*L to form support Q
    h = 0.1 * L
    idx = np.floor(P / h).astype(np.int64)
    uniq = np.unique(idx, axis=0)
    Q = (uniq + 0.5) * h
    return Q


def run(n, L, r, n_mc, rng):
    Q = make_support(n, L, rng)
    w = mst_edge_weights(Q)         # support MST edge weights
    K = len(w) + 1
    W = w.sum()
    wmax = w.max()
    th = np.geomspace(L * 0.05, wmax * 1.0001, 30)   # T-threshold geometric ladder
    T = len(th)
    # true survival counts c(t)-1
    true_counts = np.array([(w > t).sum() for t in th])
    S_true = np.trapezoid(true_counts, th)   # ~ integral of (c-1) over ladder (a chunk of W)

    def estimate(taus_list_or_arr):
        if isinstance(taus_list_or_arr, list):
            surv = np.array([np.mean(taus_list_or_arr[i] > th[i]) for i in range(T)])
        else:
            surv = np.array([np.mean(taus_list_or_arr > t) for t in th])
        counts = (K - 1) * surv
        Linf = np.max(np.abs(counts - true_counts)) / (K - 1)
        Ssum = np.trapezoid(counts, th)
        return Linf, Ssum

    reuse_Linf = np.empty(n_mc); reuse_Ssum = np.empty(n_mc)
    fresh_Linf = np.empty(n_mc); fresh_Ssum = np.empty(n_mc)
    for it in range(n_mc):
        pool = rng.choice(w, size=r)
        reuse_Linf[it], reuse_Ssum[it] = estimate(pool)
        fresh = [rng.choice(w, size=r) for _ in range(T)]
        fresh_Linf[it], fresh_Ssum[it] = estimate(fresh)

    print(f"n={n} K={K} W={W:.1f} wmax={wmax:.1f} T={T} r={r}")
    print(f"  S_true(ladder integral)={S_true:.1f}")
    print(f"  REUSE: max_t|dc|/(K-1) mean={reuse_Linf.mean():.4f}  "
          f"SUM err/W mean={np.mean(np.abs(reuse_Ssum-S_true))/W:.4f}  "
          f"SUM std/W={reuse_Ssum.std()/W:.4f}")
    print(f"  FRESH: max_t|dc|/(K-1) mean={fresh_Linf.mean():.4f}  "
          f"SUM err/W mean={np.mean(np.abs(fresh_Ssum-S_true))/W:.4f}  "
          f"SUM std/W={fresh_Ssum.std()/W:.4f}")
    print(f"  SUM Var ratio reuse/fresh = {(reuse_Ssum.var())/(fresh_Ssum.var()):.2f}  "
          f"(fresh spent r*T={r*T} seeds, reuse spent r={r})")
    print()


if __name__ == "__main__":
    rng = np.random.default_rng(99)
    print("=" * 92)
    print("UNION-BOUND framing (I) vs SUM-VARIANCE framing (II): reuse vs fresh on the")
    print("ladder-integrated survival-count estimator (a chunk of w(MST)).")
    print("=" * 92)
    for n in (900, 1800):
        for r in (50, 200):
            run(n, L=50.0, r=r, n_mc=4000, rng=rng)
