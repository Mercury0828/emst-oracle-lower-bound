"""
DECISIVE TEST of GPT-5.5-Pro round-4 (docs/webpro_round4_response.md): does the EMPTY-CELL SPATIAL
leader estimator recover w(MST(Q)) on the round-3 satellite instance, where support-POINT sampling
failed? Pro's claim: sample SPATIAL cells (incl empty) uniformly within the active cover; E[Z]=c,
Var(Z)<=M*c; the rare satellites occupy distinct spatial cells at their scale and are caught.

Checks:
 (I)  Empty-cell leader identity on a known graph: E[Z]=c, Var(Z) ~ M*c - c^2.
 (II) FULL spatial estimator on the satellite instance: reconstruct W_Q via
      hat W_Q = (K-1)h + sum_j d_j (hat c_j - 1), spatial-cell sampling at each scale; compare to exact
      W_Q AND to the (failing) point-sampling estimator. Report accuracy + #spatial samples.

Run: sim/.venv/Scripts/python.exe attack_loop/webpro_verify_round4.py
"""
import math, sys, os
import numpy as np
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'sim'))
from scipy.spatial import Delaunay


def mst_weight(points):
    pts = np.asarray(points, float); n = len(pts)
    if n <= 1: return 0.0
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
    par = list(range(n))
    def f(x):
        while par[x] != x: par[x] = par[par[x]]; x = par[x]
        return x
    W = 0.0; used = 0
    for w, i, j in we:
        ri, rj = f(i), f(j)
        if ri != rj:
            par[ri] = rj; W += w; used += 1
            if used == n - 1: break
    return W


def n_components(points, t):
    """exact #single-linkage components of `points` at threshold t (via MST: 1 + #edges>t)."""
    pts = np.asarray(points, float); n = len(pts)
    if n <= 1: return n
    tri = Delaunay(pts); E = set()
    for s in tri.simplices:
        for a in range(3):
            for b in range(a + 1, 3):
                i, j = int(s[a]), int(s[b]); E.add((min(i, j), max(i, j)))
    we = sorted((math.dist(pts[i], pts[j]), i, j) for (i, j) in E)
    par = list(range(n))
    def f(x):
        while par[x] != x: par[x] = par[par[x]]; x = par[x]
        return x
    long = 0; used = 0
    for w, i, j in we:
        ri, rj = f(i), f(j)
        if ri != rj:
            par[ri] = rj
            if w > t: long += 1
            used += 1
            if used == n - 1: break
    return 1 + long


# ---------- (I) empty-cell leader identity on a path graph ----------
def leader_identity_check(N, M, trials, rng):
    """Occupied 'cells' = a path of N nodes (so c=1 component). Embed in M candidate cells.
    Z = M if sampled cell occupied & it is the min-rank node of its component, else 0. E[Z]=c=1."""
    Zs = np.empty(trials)
    for t in range(trials):
        rank = rng.permutation(N)
        leader = int(np.argmin(rank))          # the single component's min-rank node
        X = rng.integers(M)                    # uniform candidate cell (0..N-1 occupied, rest empty)
        Zs[t] = M if (X < N and X == leader) else 0
    return Zs.mean(), Zs.var()


# ---------- (II) satellite instance ----------
def build_Q(s):
    K = s * s; h = float(s); D = float(s * s)
    nA = K - s; side = int(math.isqrt(nA)); nA = side * side
    gx, gy = np.meshgrid(np.arange(side), np.arange(side))
    A = np.column_stack([gx.ravel(), gy.ravel()]).astype(float) * h
    x0 = A[:, 0].max() + D
    sat = np.array([[x0 + j * D, 0.0] for j in range(K - nA)])
    return np.vstack([A, sat]), K, h, D, len(sat)


def estimate_c_spatial(Q, comp_label, r, a, origin, ncellsx, ncellsy, k, rng):
    """Spatial-cell leader estimator of #components at threshold r.
    Candidate cells: a grid of ncellsx*ncellsy cells of side a covering the active region (origin).
    Sample k cells uniformly; Z=M if the cell is OCCUPIED and is its component's min-rank cell."""
    M = ncellsx * ncellsy
    # map each Q point to its a-cell index; group points by occupied cell; cell -> component label
    ci = np.floor((Q[:, 0] - origin[0]) / a).astype(int)
    cj = np.floor((Q[:, 1] - origin[1]) / a).astype(int)
    inb = (ci >= 0) & (ci < ncellsx) & (cj >= 0) & (cj < ncellsy)
    cellid = ci * ncellsy + cj
    occ = {}                                   # cellid -> a representative component label (min over its pts)
    for idx in np.where(inb)[0]:
        cid = int(cellid[idx]); lab = int(comp_label[idx])
        if cid not in occ: occ[cid] = lab
        else: occ[cid] = min(occ[cid], lab)
    # assign each occupied cell a random rank; a cell is a 'leader' iff it has the min rank in its component
    cells = list(occ.keys())
    comp_of_cell = {c: occ[c] for c in cells}
    rank = {c: rng.random() for c in cells}
    comp_min = {}
    for c in cells:
        lab = comp_of_cell[c]
        if lab not in comp_min or rank[c] < rank[comp_min[lab]]:
            comp_min[lab] = c
    leaders = set(comp_min.values())
    occset = set(cells)
    Zsum = 0.0
    for _ in range(k):
        X = int(rng.integers(M))
        if X in occset and X in leaders:
            Zsum += M
    return Zsum / k                            # estimate of #occupied-cell components at this a-scale


if __name__ == "__main__":
    rng = np.random.default_rng(4)
    print("=" * 74)
    print("(I) EMPTY-CELL LEADER IDENTITY  E[Z]=c (=1 here),  Var(Z) ~ M*c - c^2")
    print("=" * 74)
    for (N, M) in [(50, 200), (200, 5000), (1000, 50000)]:
        m, v = leader_identity_check(N, M, 20000, rng)
        print(f"  N={N:5d} M={M:6d}  E[Z]={m:6.3f} (target 1.0)  Var={v:11.1f}  M*c-c^2={M-1:11d}")

    print("\n" + "=" * 74)
    print("(II) SPATIAL ESTIMATOR on the round-3 SATELLITE instance: recover W_Q?")
    print("=" * 74)
    for s in [32, 64, 96]:
        Q, K, h, D, nsat = build_Q(s)
        WQ = mst_weight(Q)
        # exact MST-edge lengths to know the satellite tail
        # geometric thresholds r_j from h to diam; cell a_j = max(h, sigma*r_j)
        sigma = 0.25
        diam = float(np.ptp(Q[:, 0]) + np.ptp(Q[:, 1]))
        rs = []
        r = h
        while r < diam:
            rs.append(r); r *= (1 + sigma)
        # exact cluster-count integral (ground truth) and spatial estimate
        WQ_int = (K - 1) * h
        WQ_hat = (K - 1) * h
        total_samples = 0
        # precompute exact components at each r via union-find label
        for r in rs:
            d = sigma * r
            a = max(h, sigma * r)
            # exact component labels of Q at threshold r (for the leader test + ground truth c)
            # (use MST: components at threshold r)
            c_exact = n_components(Q, r)
            WQ_int += d * (c_exact - 1)
            # build component labels of Q at threshold r
            # cheap union-find on Delaunay edges <= r
            pts = Q; n = len(pts)
            tri = Delaunay(pts); par = list(range(n))
            def f(x):
                while par[x] != x: par[x] = par[par[x]]; x = par[x]
                return x
            for smp in tri.simplices:
                for ii in range(3):
                    for jj in range(ii + 1, 3):
                        u, w_ = int(smp[ii]), int(smp[jj])
                        if math.dist(pts[u], pts[w_]) <= r:
                            ru, rw = f(u), f(w_)
                            if ru != rw: par[ru] = rw
            comp_label = np.array([f(i) for i in range(n)])
            # active region = bounding box of Q; candidate a-cells covering it
            ox, oy = pts[:, 0].min(), pts[:, 1].min()
            ncx = int((pts[:, 0].max() - ox) / a) + 2
            ncy = int((pts[:, 1].max() - oy) / a) + 2
            M = ncx * ncy
            # sample count: enough to estimate c to additive d-share of W_Q (cap for tractability)
            k = min(4000, max(200, int(0.5 * M)))   # bounded; measures behavior, not the asymptotic budget
            chat = estimate_c_spatial(pts, comp_label, r, a, (ox, oy), ncx, ncy, k, rng)
            WQ_hat += d * (chat - 1)
            total_samples += k
        print(f"  s={s:3d} K={K:5d}  W_Q={WQ:10.0f}  exact_integral={WQ_int:10.0f}  "
              f"spatial_hat={WQ_hat:10.0f}  hat/W_Q={WQ_hat/WQ:5.2f}  (sat tail ~{nsat*D/WQ:.2f} of W_Q)")
    print("\nReading: if spatial_hat/W_Q ~ 1 (recovers the satellite tail) with bounded samples, the")
    print("SPATIAL-cell estimator defeats the round-3 counterexample (point-sampling missed the tail).")
    print("(k is capped here for tractability; the test checks RECOVERY/accuracy, not the exact budget.)")
