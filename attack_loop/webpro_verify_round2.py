"""
Verify the numerically-checkable claims of GPT-5.5-Pro's round-2 CLAIMED CLOSURE
(docs/webpro_round2_response.md), using EXACT EMST. Pro explicitly requested these.

Lemma 1 (packing):    K_h <= 8W/h + 4   (K_h = #nonempty h-cells, W = w(MST(P))).
Lemma 2 (interleave): for t>=delta=sqrt(2)*h,  c_P(t+delta) <= c_Q(t) <= c_P(t-delta),
                      where Q = distinct h-cell centers, c_X(t) = #single-linkage components at thr t.
Snapping:             |B_L(Q) - B_L(P)| <= O(alpha*eps*W) for h <= alpha*eps*L,
                      where B_L(X) = sum_{e in MST(X), w_e>L} (w_e - L).
Instances incl. Pro's adversarial one: serpentine L-connected chain + dense islands + unequal occupancy.

Run: sim/.venv/Scripts/python.exe attack_loop/webpro_verify_round2.py
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
        try:
            tri = Delaunay(pts); E = set()
            for s in tri.simplices:
                for a in range(3):
                    for b in range(a + 1, 3):
                        i, j = int(s[a]), int(s[b]); E.add((min(i, j), max(i, j)))
            cand = list(E)
        except Exception:
            cand = [(i, j) for i in range(n) for j in range(i + 1, n)]
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


def W_of(points):
    return float(mst_edge_weights(points).sum())

def c_of(weights, t):           # #components at threshold t  = 1 + #{MST edges > t}
    return 1 + int(np.sum(weights > t))

def B_of(weights, L):           # sum of excess of long edges above L
    long = weights[weights > L]
    return float(np.sum(long - L))

def snap_centers(points, h):    # distinct h-cell centers
    pts = np.asarray(points, float)
    idx = np.floor(pts / h).astype(np.int64)
    uniq = np.unique(idx, axis=0)
    return (uniq + 0.5) * h


# ---------------- instances ----------------
def inst_random(n, rng):
    return rng.random((n, 2)) * n           # spread ~ n

def inst_islands(n, L, rng, k_islands=8):
    """k dense islands at separations L, 2L, 4L,... + a serpentine L-connected chain."""
    pts = []
    # serpentine chain: ~ n/2 points, consecutive step 0.4*L (so L-connected), boustrophedon
    m = n // 2; step = 0.4 * L; cols = max(2, int(math.isqrt(m)))
    x = y = 0.0; dirn = 1
    for i in range(m):
        pts.append((x, y)); x += dirn * step
        if (i + 1) % cols == 0:
            y += step; dirn *= -1
    base = np.array(pts)
    # dense islands of unequal occupancy, far apart (separations 1.5L, 3L, 6L,...)
    rest = n - len(base); per = max(1, rest // k_islands)
    cx = base[:, 0].max() + 2 * L
    isl = []
    for j in range(k_islands):
        occ = max(1, int(per * (0.3 + 1.4 * rng.random())))   # unequal occupancy
        c = np.array([cx + (1.5 * L) * (2 ** j), (j % 3) * 3 * L])
        isl.append(c + rng.random((occ, 2)) * 0.3)            # dense cluster (size 0.3 << L)
    P = np.vstack([base] + isl)
    return P


if __name__ == "__main__":
    rng = np.random.default_rng(11)
    print("=" * 78)
    print("(L1) PACKING  K_h <= 8W/h + 4")
    print("=" * 78)
    ok1 = True
    for name, P in [("random-n800", inst_random(800, rng)),
                    ("random-n1500", inst_random(1500, rng)),
                    ("islands-n1200", inst_islands(1200, L=60.0, rng=rng))]:
        W = W_of(P)
        for h in [5, 15, 40, 100, 250]:
            Kh = len(snap_centers(P, h)); bound = 8 * W / h + 4
            good = Kh <= bound + 1e-6; ok1 &= good
            print(f"  {name:14s} h={h:6.1f}  K_h={Kh:5d}  8W/h+4={bound:9.1f}  {'OK' if good else 'VIOLATED'}")
    print(f"  >>> Lemma 1 holds on all: {ok1}")

    print("\n" + "=" * 78)
    print("(L2) FILTRATION INTERLEAVING  c_P(t+d) <= c_Q(t) <= c_P(t-d),  d=sqrt(2) h")
    print("=" * 78)
    ok2 = True
    P = inst_islands(1000, L=50.0, rng=rng); wP = mst_edge_weights(P); W = wP.sum()
    for h in [8.0, 20.0]:
        Q = snap_centers(P, h); wQ = mst_edge_weights(Q); d = math.sqrt(2) * h
        for t in [30.0, 50.0, 80.0, 150.0, 300.0]:
            lo = c_of(wP, t + d); mid = c_of(wQ, t); hi = c_of(wP, t - d)
            good = (lo <= mid <= hi); ok2 &= good
            print(f"  h={h:5.1f} t={t:6.1f}  c_P(t+d)={lo:4d} <= c_Q(t)={mid:4d} <= c_P(t-d)={hi:4d}  "
                  f"{'OK' if good else 'VIOLATED'}")
    print(f"  >>> Lemma 2 holds on all: {ok2}")

    print("\n" + "=" * 78)
    print("(SNAP) |B_L(Q) - B_L(P)| <= O(alpha*eps*W)  for h <= alpha*eps*L")
    print("=" * 78)
    P = inst_islands(1400, L=64.0, rng=rng); wP = mst_edge_weights(P); W = wP.sum()
    K0 = round(len(P) ** (2 / 3)); L = W / K0
    print(f"  n={len(P)}  W={W:.1f}  K0=n^(2/3)={K0}  L=W/K0={L:.2f}")
    for alpha_eps in [0.5, 0.2, 0.1, 0.05]:
        h = alpha_eps * L
        Q = snap_centers(P, h); wQ = mst_edge_weights(Q)
        BP = B_of(wP, L); BQ = B_of(wQ, L)
        rel = abs(BQ - BP) / W
        print(f"  h={h:6.2f} (a*eps={alpha_eps:4.2f})  B_L(P)={BP:9.1f}  B_L(Q)={BQ:9.1f}  "
              f"|dB|/W={rel:.4f}  K_h={len(Q)}")
    print("  (expect |dB|/W to shrink ~ linearly with h=alpha*eps*L)")
