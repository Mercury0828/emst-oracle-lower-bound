"""
Audit B (round 2): the SEED-REUSE probabilistic accounting.

Decisive question: when the final estimate SUMS/integrates over T thresholds using
the SAME pool of uniform seeds (with independent traversal randomness per threshold),
does the summed estimator stay (1 +/- eps) -- or does correlation across thresholds
blow up its variance relative to using FRESH seeds per threshold?

We model the abstract structure that the reuse argument relies on:
  - There is a per-threshold estimator hat_g(t) that is a function of a SHARED pool
    of s uniform seeds q_1..q_s ~ Unif(Q) and per-(seed,threshold) independent
    traversal noise.
  - The final answer is a SUM over thresholds:  hat_S = sum_t hat_g(t) * dt.

The cleanest exact instance: the death-time / multiset estimator itself.
For a fixed graph H with MST edge weights w_1..w_{K-1}, define for a uniform random
vertex q its death time tau(q). Round-1 identity: {tau(q): q != r} ~ uniform over the
MST edge weights (one per non-root vertex, ignoring zeros). The clipped statistic at
threshold t is  X_t(q) = min{tau(q), t}.  And

   A_t = sum_e min{w_e, t} = K * E_q[X_t(q)]          (multiset identity)
   w(MST) = sum_e w_e = A_inf = integral_0^inf (c(t)-1) dt.

Crucially  w(MST) = sum_e w_e = lim A_t, and also for the TAIL decomposition
   B_L = sum_{w_e>L}(w_e-L),   w(MST)=A_L + B_L.

The reuse estimator for w(MST) via thresholds is:
   hat_w = (K/s) * sum_{j=1}^{s} tau(q_j)       (one shot, no threshold sum needed)
but Pro's pipeline instead estimates A_L (clipped) and B_L separately and across a
GEOMETRIC LADDER of L values (T = O(log Delta) thresholds), REUSING the same s seeds.

KEY POINT we test:
   With shared seeds, hat_g(t1) and hat_g(t2) are POSITIVELY correlated (same q_j).
   Summing T correlated per-threshold estimators:
       Var[sum_t hat_g(t)] = sum_{t,t'} Cov(hat_g(t),hat_g(t')).
   If the per-threshold estimators were independent (fresh seeds) the cross terms
   vanish and Var = sum_t Var(hat_g(t)).  Question: does the reuse Var blow up by a
   factor up to T (worst case all-correlated)?  We measure the ratio
       Var_reuse(sum) / Var_fresh(sum).

We compare:
   (R) REUSE:  draw ONE pool of s seeds, evaluate hat_g(t) for all t on that pool.
   (F) FRESH:  draw an INDEPENDENT pool of s seeds for EACH threshold t.
Both use the SAME total per-threshold sample budget s.  (Fresh uses s*T total uniform
seeds; reuse uses s total -- that's the whole point/cost saving.)
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


def make_instance(n, L, rng):
    """Serpentine L-connected chain + dense islands at L,2L,4L,...  (Pro's adversary)."""
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
    return np.vstack([base] + isl)


def integrated_estimator(w, thresholds, seed_taus):
    """
    Estimate w(MST) = sum_e w_e via a threshold ladder using the death-time multiset.
    The multiset {tau(q)} EQUALS {w_e} (round-1 identity), so a uniform seed's tau is a
    uniform MST edge weight. We estimate, on the SAME seeds, the survival counts at each
    threshold and integrate:
        w(MST) = integral_0^inf (c(t)-1) dt = sum_e w_e.
    Per-threshold survival fraction est:  phat(t) = mean_j 1[tau(q_j) > t].
    Then (K-1)*phat(t) estimates c(t)-1, and integral of (c(t)-1) dt over the ladder
    (Riemann/trapezoid) estimates w(MST). seed_taus = array of tau values for the pool.
    """
    K = len(w) + 1  # vertices ~ edges+1
    th = np.asarray(thresholds)
    # survival fraction at each threshold from the (shared or fresh) seed taus
    # seed_taus may be a list-of-arrays (fresh: one array per threshold) or single array (reuse)
    if isinstance(seed_taus, list):
        surv = np.array([np.mean(seed_taus[i] > th[i]) for i in range(len(th))])
    else:
        surv = np.array([np.mean(seed_taus > t) for t in th])
    counts = (K - 1) * surv               # est of c(t)-1  (since E[1[tau>t]] = (#w_e>t)/(K-1)... see note)
    # integrate counts dt via trapezoid on [0, th_max]
    return np.trapezoid(counts, th)


# Note on the identity: for K-1 edges and a uniform seed among the K-1 non-root vertices,
# P[tau > t] = (#edges > t)/(K-1) = (c(t)-1)/(K-1). So (K-1)*P[tau>t] = c(t)-1. Exact.

def run(n, L, eps_budget, s_pool, n_mc, rng):
    P = make_instance(n, L, rng)
    w = mst_edge_weights(P)
    K = len(w) + 1
    W = w.sum()
    wmax = w.max()
    # threshold ladder: geometric from small to wmax, T = O(log) thresholds
    th = np.unique(np.concatenate([[0.0], np.geomspace(L * 0.1, wmax * 1.01, 40)]))
    th = np.sort(th)
    T = len(th)

    # the "edge weight" each uniform vertex carries == a uniform draw from w (round-1 identity)
    def draw_taus(size):
        return rng.choice(w, size=size, replace=True)

    est_reuse = np.empty(n_mc)
    est_fresh = np.empty(n_mc)
    for it in range(n_mc):
        # REUSE: one pool, same taus used at every threshold
        pool = draw_taus(s_pool)
        est_reuse[it] = integrated_estimator(w, th, pool)
        # FRESH: independent pool per threshold
        fresh = [draw_taus(s_pool) for _ in range(T)]
        est_fresh[it] = integrated_estimator(w, th, fresh)

    def stats(e):
        return e.mean(), e.std(), (np.abs(e - W) / W <= eps_budget).mean()
    mr, sr, pr = stats(est_reuse)
    mf, sf, pf = stats(est_fresh)
    print(f"n={n} K={K} W={W:.1f} wmax={wmax:.1f} T={T} s_pool={s_pool} (fresh uses s*T={s_pool*T} total seeds)")
    print(f"  REUSE : mean={mr:9.1f} (W={W:.1f})  std={sr:8.2f}  P[(1+/-{eps_budget})W]={pr:.3f}")
    print(f"  FRESH : mean={mf:9.1f} (W={W:.1f})  std={sf:8.2f}  P[(1+/-{eps_budget})W]={pf:.3f}")
    print(f"  Var_reuse/Var_fresh = {(sr**2)/(sf**2):.3f}   (T={T}; reuse uses 1/T the seeds)")
    print()


if __name__ == "__main__":
    rng = np.random.default_rng(2026)
    print("=" * 90)
    print("SEED-REUSE: integrated (summed-over-thresholds) estimator, REUSE vs FRESH pools")
    print("Both use s_pool samples PER THRESHOLD; FRESH pays s_pool*T total uniform seeds,")
    print("REUSE pays only s_pool. We compare bias, std, and (1+/-eps) hit-rate of the SUM.")
    print("=" * 90)
    for n in (600, 1200):
        for s_pool in (30, 100):
            run(n, L=50.0, eps_budget=0.15, s_pool=s_pool, n_mc=3000, rng=rng)
