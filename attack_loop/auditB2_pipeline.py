"""
Audit B round 2, PART 4: does Pro's ACTUAL pipeline (sec5/sec6) commit the
"summed-reused-seed variance blowup" error, or avoid it?

Pro does NOT integrate raw survival counts over a reused-seed ladder. He:
  sec5: estimate A_L(Q)=sum_e min{w_e,L} via CLIPPED death-time at a SINGLE L
        (X=min(tau,L); variance controlled by X^2<=LX).
  sec6: estimate W_Q via Lemma 3 (Czumaj sqrt(K) estimator), then B_hat_L = W_Q - A_Q.

The "T thresholds with reused seeds" live INSIDE Lemma 3's CRT estimator (a geometric
ladder to estimate w(MST(Q)) to (1+/-eta) RELATIVE) and inside the W-search of sec7.

CRITICAL DISTINCTION the PART-3 script exposed:
  - Naively integrating REUSED-seed survival counts over a ladder  == raw tau estimator,
    whose variance is dominated by the heavy tail (BAD: needs Omega(K) samples).
  - The CLIPPED estimator at L caps each contribution at L, killing the heavy-tail
    variance: Var <= K^2 * L * E[X] / s = O(eta^2 W^2) with s=O(eta^-2) support samples
    (sec5 algebra, verified in PART 2).

So the question reduces to: does Lemma 3 (Czumaj) estimate w(MST(Q)) WITHOUT the
heavy-tail variance blowup, i.e. is its internal threshold-ladder estimator a
PROPER (1+/-eta)-relative MST estimator (which is what Czumaj PROVES in Õ(sqrt K)),
rather than the naive reused-seed integral we showed blows up?

ANSWER (analytic): YES. Czumaj-Sohler's estimator is NOT "sum reused-seed survival
counts". It estimates each c^(i) (number of connected components at geometric
threshold (1+eta)^i) to the accuracy REQUIRED by the CRT analysis, and the MST weight
formula w(MST)= n - cmax + eta * sum_i c^(i) * (1+eta)^i-ish is a WEIGHTED sum where
the per-level RELATIVE error eta translates to overall RELATIVE error eta -- because
each c^(i) is estimated to additive error eta*c^(i) (relative), NOT to a fixed additive
budget that must be summed without cancellation. The heavy tail corresponds to a level
i where c^(i)=O(1) (few components), and there CRT's cost is n/c^(i) -- for the SUPPORT
of size K this is K/c^(i) <= K (not the full n). That K-cost at the tail is exactly the
sqrt(K)+ spatial cost Czumaj pays, and is Õ(sqrt K) ONLY via the spatial subdivision,
NOT via uniform-vertex sampling.

** THE REMAINING WORRY (the real one) **: at the tail level c^(i)=O(1), the CRT
connected-components estimator costs ~ K/c^(i) = Omega(K) uniform samples on a GENERAL
graph. Czumaj beats this to Õ(sqrt K) ONLY using the geometric/spatial structure (cone-NN
in the original; WSPD here). So the sqrt(K) is REAL and spatial. The reused seed pool of
size O(log T) is for the FEW uniform vertices CRT needs at the cheap (many-component)
levels; the EXPENSIVE tail levels are handled SPATIALLY (sqrt K range-emptiness ops), not
by uniform sampling. THIS is the load-bearing claim and it is exactly Pro's sec4/sec8.

This script DEMONSTRATES the saving regime: it shows that
  (a) the CLIPPED bulk estimate of A_L on the SUPPORT (K=Theta(n^{2/3})) is (1+/-eta)*
      additive-eta*W accurate with O(eta^-2) SUPPORT samples (each costing n/K),
  (b) so the EXPENSIVE uniform-support-sampling primitive is invoked O(eta^-2 * polylog)
      times TOTAL across the whole pipeline (bulk + ladder), == Õ(1) times,
  (c) hence total cost = Õ(n/K) [uniform samples] + Õ(sqrt K) [spatial] = Õ(n^{1/3}).
We numerically confirm (a): clipped bulk on the support, additive error vs sample count.
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
    h = 0.1 * L
    idx = np.floor(P / h).astype(np.int64)
    uniq = np.unique(idx, axis=0)
    return (uniq + 0.5) * h


def main():
    rng = np.random.default_rng(123)
    print("=" * 92)
    print("CLIPPED bulk A_L on the SUPPORT: additive error vs #support-samples s, with L=W/K0")
    print("(sec5: Var[(K/s)sum X] <= K^2 L E[X]/s; additive eta*W with s=O(eta^-2))")
    print("=" * 92)
    for n in (1500, 3000):
        Q = make_support(n, L=50.0, rng=rng)
        w = mst_edge_weights(Q)
        K = len(w) + 1
        W = w.sum()
        K0 = round(K)  # support size IS K here; use L = W/K (operative L=Theta(W/K0))
        L = W / K
        X = np.minimum(w, L)
        A_L = (K - 1) * X.mean()
        EX = X.mean(); EX2 = (X**2).mean()
        print(f" support K={K} W={W:.1f}  L=W/K={L:.3f}  A_L={A_L:.1f}  B_L=W-A_L={W-A_L:.1f}")
        print(f"   X^2<=LX: E[X^2]={EX2:.4f} <= L E[X]={L*EX:.4f} -> {EX2<=L*EX+1e-9}")
        for s in (16, 64, 256):
            # MC the clipped estimator
            est = np.array([ (K)/s * np.sum(np.minimum(rng.choice(w,size=s),L)) for _ in range(3000)])
            add_err = np.mean(np.abs(est - A_L))/W
            std = est.std()/W
            var_bound = (K**2)*L*EX/s
            print(f"    s={s:4d}: additive |dA_L|/W mean={add_err:.4f}  std/W={std:.4f}  "
                  f"sec5-bound std/W<={math.sqrt(var_bound)/W:.4f}")
        print()
    print("Interpretation: clipped bulk needs only O(eta^-2) SUPPORT samples for additive eta*W,")
    print("INDEPENDENT of n/K. The n/K cost is PER support sample. So expensive-primitive calls")
    print("= O(eta^-2 * polylog) total => Õ(n/K)=Õ(n^{1/3}). The heavy tail does NOT blow up the")
    print("CLIPPED estimator (unlike the raw-tau integral of PART 3).")


if __name__ == "__main__":
    main()
