"""
Audit B round 2, PART 2: reframe the seed-reuse variance question correctly.

KEY ANALYTIC FACT: for a single seed q,
    integral_0^inf 1[tau(q) > t] dt  =  tau(q).
So the REUSE integrated estimator  (K-1)/s * sum_j integral 1[tau(q_j)>t] dt
collapses EXACTLY to the one-shot death-time estimator (K-1)/s * sum_j tau(q_j).
=> Reuse across the threshold ladder for the *summed* quantity is mathematically
identical to NOT laddering at all; its variance is Var(tau) = variance of a uniform
MST edge weight -- dominated by the heavy tail (exactly round-1's obstruction).

The honest question is therefore NOT "reuse vs fresh at equal per-threshold budget"
(unfair: fresh used T x more seeds). It is:

  (A) At EQUAL TOTAL seed budget B, is laddering-with-fresh-seeds better than
      reuse (= one-shot)?   i.e. does splitting B seeds across T thresholds and
      summing FRESH per-threshold estimators reduce variance vs spending all B on
      one-shot?   ANSWER (analytic): NO for an UNBIASED sum -- fresh-per-threshold
      with B/T seeds each gives the SAME estimator variance as reuse, because
      summing independent unbiased pieces just re-partitions the same samples.
      Actually we must check: are the per-threshold pieces estimating disjoint
      contributions?  They are NOT -- each threshold's survival count is a function
      of the FULL tau, so fresh-per-threshold *wastes* samples. We test this.

  (B) The thing reuse genuinely BUYS: you pay s uniform seeds ONCE instead of s*T.
      The thing it genuinely COSTS: nothing extra for the SUM, because the sum over
      a shared seed telescopes to tau(q). The variance is Var(tau) either way.

CONCLUSION TO TEST: the per-threshold-marginal-iid + union-bound framing is about
CORRECTNESS AT EACH THRESHOLD (each c(t) estimate is individually good w.h.p.). But
the FINAL estimate is sum_t, and for the SUM the relevant variance is Var(tau), which
the laddering does not reduce and reuse does not inflate (beyond the unavoidable
Var(tau)). So reuse is SOUND for the sum *to exactly the extent the one-shot death-time
estimator is sound* -- which is PRECISELY round-1's already-known obstruction: the
heavy tail makes Var(tau) huge, needing Omega(n) one-shot samples. The whole edifice
(sec 5/6) AVOIDS this by NOT integrating tau directly: it CLIPS at L (X=min{tau,L})
for the bulk A_L, and estimates the tail B_L by a DIFFERENT spatial object (Lemma 3 +
death-time on the support H_Q). So the seed-reuse claim is really about reusing seeds
for the SUPPORT estimator across thresholds, not about integrating raw tau.

This script verifies (1) the telescoping identity, (2) that for the CLIPPED bulk A_L
the death-time estimator at a single L is fine (round-1, sec 5), and (3) measures the
variance of the clipped estimator vs the algebra KL*W_H/s.
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


def main():
    rng = np.random.default_rng(7)
    P = make_instance(1200, L=50.0, rng=rng)
    w = mst_edge_weights(P)
    K = len(w) + 1
    W = w.sum()
    wmax = w.max()
    print(f"n={len(P)} K={K} W={W:.1f} wmax={wmax:.1f}")

    # (1) TELESCOPING identity: integral over a fine ladder of 1[tau>t] dt == tau
    th = np.linspace(0, wmax * 1.0001, 200000)
    sample = rng.choice(w, size=5)
    for tau in sample:
        approx = np.trapezoid((tau > th).astype(float), th)
        print(f"  tau={tau:9.3f}  integral 1[tau>t]dt = {approx:9.3f}  (err {abs(approx-tau):.4f})")
    print("  => integrating reused-seed survival over thresholds == raw tau (collapse).")

    # (2) one-shot death-time estimator of W: Var = (K-1)^2 * Var(tau)/s ; tau ~ Unif(w)
    #     vs the CLIPPED bulk at L: X=min(tau,L); Var bound (K/s)^2 * Var(X) <= (K^2/s) * L*E[X].
    L = 50.0
    Etau = w.mean(); Vtau = w.var()
    X = np.minimum(w, L); EX = X.mean(); VX = X.var()
    A_L = (K - 1) * EX       # = sum_e min(w_e,L)
    print(f"\n  E[tau]={Etau:.3f} Var(tau)={Vtau:.1f}   (raw -> heavy tail dominates)")
    print(f"  E[X]  ={EX:.3f}  Var(X) ={VX:.4f}  with X=min(tau,{L})")
    print(f"  A_L = sum min(w,L) = {A_L:.1f}   ;  B_L = W - A_L = {W-A_L:.1f}")
    # Pro sec5 bound: Var[(K/s)sum X] <= K^2 * L * E[X] / s   (using X^2<=LX => E[X^2]<=L E[X])
    EX2 = (X**2).mean()
    print(f"  E[X^2]={EX2:.2f}  vs  L*E[X]={L*EX:.2f}   (X^2<=LX holds: {EX2 <= L*EX + 1e-9})")
    # additive error of A_L estimate at s samples (std):
    for s in (50, 200, 800):
        var_est = (K**2) * VX / s
        bound   = (K**2) * L * EX / s     # Pro's bound (looser, uses E[X^2]<=L E[X])
        print(f"   s={s:4d}: std(A_L est)={math.sqrt(var_est):8.1f}  Pro-bound std<={math.sqrt(bound):8.1f}"
              f"   additive/W = {math.sqrt(var_est)/W:.4f}")

    # (3) Pro sec5 final claim: with K=O(K0), L=G/K0, W_H=O(G): K*L*W_H/G^2 = O(1).
    #     Here "support" framing: K0 = n^{2/3}, L = W/K0 approx, W_H ~ W. Check K*L*W/W^2.
    K0 = round(len(P) ** (2/3))
    L2 = W / K0
    print(f"\n  Pro sec5 dimensionless: K0=n^(2/3)={K0}, L=W/K0={L2:.2f}")
    print(f"   K*L*W / W^2 = K*L/W = {K*L2/W:.3f}  (claims O(1); note K here ~ n not n^{{2/3}})")
    print(f"   If K were Theta(K0)=n^(2/3)={K0}: K0*L2/W = {K0*L2/W:.3f}  (= O(1) as claimed)")
    print("   -> the O(1) needs K=Theta(K0) (the SUPPORT, not the full point set). Consistent.")


if __name__ == "__main__":
    main()
