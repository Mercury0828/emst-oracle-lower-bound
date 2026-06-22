"""
Audit C round-2: adversarial tests of GPT-5.5-Pro's CLAIMED Õ(n^{1/3}) closure.
Focus targets:
  (3) W_Q = O(W) on snapped instances at the OPERATIVE grid (K_h = Theta(K_0)); report the constant.
  (4/6) global assembly identity W = A_L(P) + B_L(P) and B_L(Q) = W_Q - A_L(Q);
        does B_hat_L = W_Q - A_L(Q) on the support reconstruct B_L(P) within O(eps W)?
  (5) adversarial instances: one rare long bridge (Theta(W) on a single edge), serpent,
      MST-edges sitting at dyadic boundaries.
Uses EXACT EMST from sim/emst.py.
"""
import math, sys, os
import numpy as np
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'sim'))
from emst import emst_weight
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


def snap_centers(points, h):
    pts = np.asarray(points, float)
    idx = np.floor(pts / h).astype(np.int64)
    uniq = np.unique(idx, axis=0)
    return (uniq + 0.5) * h

def B_of(weights, L):
    long = weights[weights > L]
    return float(np.sum(long - L))

def A_of(weights, L):   # clipped bulk: sum of min(w,L) over MST edges
    return float(np.sum(np.minimum(weights, L)))


# ---- instances ----
def inst_random(n, rng):
    return rng.random((n, 2)) * n

def inst_bridge(n, rng):
    """Two dense unit-grid clusters separated by gap G=Theta(n). One heavy MST edge = Theta(W)."""
    half = n // 2
    side = int(math.isqrt(half))
    g = np.array([(i, j) for i in range(side) for j in range(half // side + 1)])[:half].astype(float)
    A = g.copy()
    B = g.copy(); B[:, 0] += side + 0.9 * n   # gap ~ 0.9n
    return np.vstack([A, B])

def inst_serpent(n, L, rng):
    m = n; step = 0.4 * L; cols = max(2, int(math.isqrt(m)))
    x = y = 0.0; dirn = 1; pts = []
    for i in range(m):
        pts.append((x, y)); x += dirn * step
        if (i + 1) % cols == 0:
            y += step; dirn *= -1
    return np.array(pts)

def find_operative_grid(P, W, K0, target_lo=0.7, target_hi=4.0):
    """Halve h (dyadic) until K_h in [target_lo*K0, target_hi*K0]; return (h, Kh)."""
    G = W
    L = G / K0
    # start at largest dyadic h <= 0.1*L  (alpha eps = 0.1)
    h = 0.1 * L
    # ensure dyadic-ish; just halve from a coarse start to find crossing
    h = L  # coarse: few cells
    for _ in range(40):
        Kh = len(snap_centers(P, h))
        if Kh >= target_lo * K0:
            if Kh <= target_hi * K0:
                return h, Kh
            # too many -> increase h
            h *= 1.3
        else:
            h /= 2.0
    return h, len(snap_centers(P, h))


if __name__ == "__main__":
    rng = np.random.default_rng(7)
    print("=" * 80)
    print("(T3) W_Q / W at the OPERATIVE grid  K_h=Theta(K_0),  K_0 = n^(2/3)")
    print("=" * 80)
    for name, P in [("random-n1000", inst_random(1000, rng)),
                    ("random-n3000", inst_random(3000, rng)),
                    ("serpent-n1500", inst_serpent(1500, 50.0, rng)),
                    ("bridge-n1000",  inst_bridge(1000, rng)),
                    ("bridge-n2000",  inst_bridge(2000, rng))]:
        n = len(P); W = emst_weight(P); K0 = round(n ** (2/3))
        h, Kh = find_operative_grid(P, W, K0)
        Q = snap_centers(P, h); WQ = emst_weight(Q)
        L = W / K0
        print(f"  {name:14s} n={n:5d} W={W:10.1f} K0={K0:4d}  h={h:8.2f} K_h={Kh:5d}"
              f"  W_Q={WQ:10.1f}  W_Q/W={WQ/W:6.3f}  h/L={h/L:.3f}")

    print("\n" + "=" * 80)
    print("(T4) ASSEMBLY IDENTITY:  reconstruct B_L(P) as B_L(Q)=W_Q-A_L(Q); compare to true B_L(P)")
    print("     and full W = A_L(P)+B_L(P).  L = W/K0 (operative).")
    print("=" * 80)
    for name, P in [("random-n2000", inst_random(2000, rng)),
                    ("serpent-n1500", inst_serpent(1500, 50.0, rng)),
                    ("bridge-n1500",  inst_bridge(1500, rng))]:
        n = len(P); wP = mst_edge_weights(P); W = wP.sum(); K0 = round(n ** (2/3))
        L = W / K0
        h, Kh = find_operative_grid(P, W, K0)
        Q = snap_centers(P, h); wQ = mst_edge_weights(Q); WQ = wQ.sum()
        BP = B_of(wP, L); AP = A_of(wP, L)
        BQ = B_of(wQ, L); AQ = A_of(wQ, L)
        # Pro's final estimator target: B_hat_L = W_Q - A_L(Q) = B_L(Q)
        recon = WQ - AQ
        print(f"  {name:14s} L={L:8.2f} h={h:7.2f} K_h={Kh:5d}")
        print(f"      W={W:9.1f}=A_P({AP:8.1f})+B_P({BP:8.1f})   check={AP+BP:9.1f}")
        print(f"      W_Q={WQ:9.1f}  A_Q={AQ:8.1f}  B_Q=W_Q-A_Q={recon:8.1f}")
        print(f"      |B_Q - B_P|/W = {abs(recon-BP)/W:.4f}   (must be O(eps))")
        # Full reconstruction Pro uses in sec.7: W_hat = A_L(P) + (W_Q - A_L(Q))
        Whatfull = AP + (WQ - AQ)
        print(f"      W_hat=A_P+(W_Q-A_Q)={Whatfull:9.1f}   |W_hat-W|/W={abs(Whatfull-W)/W:.4f}")

    print("\n" + "=" * 80)
    print("(T5) RARE BRIDGE: is the Theta(W) heavy edge preserved in B_L(Q)? (tail not destroyed)")
    print("=" * 80)
    for n in [800, 1500, 3000]:
        P = inst_bridge(n, rng); wP = mst_edge_weights(P); W = wP.sum(); K0 = round(n**(2/3))
        L = W / K0
        h, Kh = find_operative_grid(P, W, K0)
        Q = snap_centers(P, h); wQ = mst_edge_weights(Q)
        heavyP = wP[wP > L]; heavyQ = wQ[wQ > L]
        print(f"  bridge-n{n:4d} W={W:9.1f} L={L:7.2f} h={h:7.2f} K_h={Kh:4d}")
        print(f"      #long_P={len(heavyP)} max_P={wP.max():9.1f}  #long_Q={len(heavyQ)} max_Q={wQ.max():9.1f}")
        print(f"      B_P={B_of(wP,L):9.1f}  B_Q={B_of(wQ,L):9.1f}  rel|dB|/W={abs(B_of(wQ,L)-B_of(wP,L))/W:.4f}")
