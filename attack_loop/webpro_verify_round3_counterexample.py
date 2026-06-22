"""
DECISIVE TEST of GPT-5.5-Pro's round-3 counterexample (docs/webpro_round3_response.md §3,§7):
does a polylog SHARED-POOL death-time estimator of w(MST(Q)) miss a constant fraction (the rare
satellites), refuting the round-2 seed-reuse closure?

Q = dense h-spaced grid (K-s points) + s satellites on a ray at spacing D=K (each ~D from the rest).
By the (verified) multiset identity, a uniform vertex's death-time tau(v) is a uniform draw from the
MST-edge-weight multiset {w_e} U {0}. So the death-time estimator with r sampled vertices is
  hat W_Q = (K/r) * sum of r uniform draws from {w_e}U{0}.
With r=polylog the s long satellite edges (~D) are missed w.p. (1-s/K)^r -> 1, so hat W_Q ~ K*h,
missing the Theta(s*D) satellite mass = a constant fraction of W_Q. Fresh r=sqrt(K) catches them.

Run: sim/.venv/Scripts/python.exe attack_loop/webpro_verify_round3_counterexample.py
"""
import math, sys, os
import numpy as np
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'sim'))
from scipy.spatial import Delaunay


def mst_edge_weights(points):
    pts = np.asarray(points, float); n = len(pts)
    if n <= 1:
        return np.array([])
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


def build_Q(s):
    """K=s^2 support points: (K-s) on an h-spaced grid + s satellites at spacing D=K."""
    K = s * s; h = float(s); D = float(s * s)
    nA = K - s; side = int(math.isqrt(nA)); nA = side * side
    gx, gy = np.meshgrid(np.arange(side), np.arange(side))
    A = np.column_stack([gx.ravel(), gy.ravel()]).astype(float) * h
    x0 = A[:, 0].max() + D
    sat = np.array([[x0 + j * D, 0.0] for j in range(K - nA)])   # exactly K-nA satellites
    Q = np.vstack([A, sat])
    return Q, K, h, D, len(sat)


def estimator(weights, K, r, trials, rng):
    """hat W_Q = (K/r) * sum of r uniform draws from the tau-multiset {weights}U{0}."""
    pool = np.concatenate([weights, [0.0]])      # K values (K-1 edges + root 0)
    ests = np.empty(trials)
    for t in range(trials):
        draws = rng.choice(pool, size=r, replace=True)
        ests[t] = (K / r) * draws.sum()
    return ests


def per_run_error(weights, K, r, trials, rng):
    """A SINGLE pool of r samples is used ONCE. Report the typical per-run relative error
    (std/mean over independent single-pool runs) and the fraction of runs outside (1 +- 0.1)."""
    ests = estimator(weights, K, r, trials, rng)
    WQ = float(weights.sum())
    rel = ests / WQ
    return rel.mean(), rel.std(), float(np.mean(np.abs(rel - 1) > 0.1))


if __name__ == "__main__":
    rng = np.random.default_rng(3)
    print("Per-RUN relative error of the death-time estimator of w(MST(Q)) (a single seed pool, used once).")
    print("Pro's claim: polylog seeds are INSUFFICIENT (rare high-value satellites) -> large per-run error;")
    print("you need ~sqrt(K) samples. (At small K, polylog ~ sqrt(K), so the gap only opens up as K grows.)\n")
    print(f"{'s':>5} {'K':>8} {'sat/W_Q':>8} {'sqrtK':>6} {'r_poly':>7} || "
          f"{'poly:mean':>9} {'poly:std':>9} {'poly:%>10%err':>13} || {'sqrtK:std':>9} || {'10*sqrtK:std':>12}")
    for s in [64, 128, 256, 500]:
        Q, K, h, D, nsat = build_Q(s)
        w = mst_edge_weights(Q)
        WQ = float(w.sum()); sat = float(w[w > D / 2].sum())
        r_poly = math.ceil(20 * math.log(K)); r_sqrt = int(round(math.sqrt(K)))
        pm, ps, pfrac = per_run_error(w, K, r_poly, 600, rng)
        _, ss, _ = per_run_error(w, K, r_sqrt, 600, rng)
        _, s10, _ = per_run_error(w, K, 10 * r_sqrt, 600, rng)
        print(f"{s:>5} {K:>8} {sat/WQ:>8.3f} {r_sqrt:>6} {r_poly:>7} || "
              f"{pm:>9.3f} {ps:>9.3f} {pfrac:>13.2f} || {ss:>9.3f} || {s10:>12.3f}")
    print("\nReading: 'poly:std' = per-run relative error with polylog seeds; 'poly:%>10%err' = fraction of")
    print("single runs off by >10%. If these stay LARGE (and don't shrink) while 'sqrtK'/'10*sqrtK' std")
    print("shrink, Pro is RIGHT: polylog seed-reuse cannot estimate w(MST(Q)) to (1+-eps); ~sqrt(K)+ needed.")
