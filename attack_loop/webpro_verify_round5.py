"""
FINAL numeric test of GPT-5.5-Pro round-5 (docs/webpro_round5_response.md §9): the c_j-vs-N_j accounting.
Support Q = a fully-occupied sqrt(K)xsqrt(K) fine-grid CARPET (so at floor scales N_j=Theta(K), c_j=1)
+ sparse satellite chains (a constant fraction of W_Q). Check BOTH per-scale budgets sum to ~ O~(sqrt K):
  candidate-root  ~ sum_j M_j*U_j/alpha_j^2   (uses U_j>=c_j, NOT N_j)   [eq 36]
  exploration     ~ sum_j N_j*U_j/alpha_j^2   (uses N_j<=K)              [eqs 38-44]
The round-2 leak (n^{2/3}) would show as these sums scaling like K (not sqrt K). We verify Sum/sqrt(K)
stays BOUNDED/flat as K grows (the carpet is the worst case for N_j: N_j=Theta(K) at the floor).

Run: sim/.venv/Scripts/python.exe attack_loop/webpro_verify_round5.py

⚠️ CAVEAT (2026-06-21): THIS TEST IS UNRELIABLE as written — the satellite placement (gap=4*scarp,
spreading sats over ~4*scarp^2 width) inflates the active-cover cell side delta enormously, which
inflates M_j=b(delta/a)^2 astronomically at fine scales. Result: BOTH sums grow ~K (cand ~K^2), but the
candidate-root term was ALREADY verified Õ(√K) by the round-4 cost audit (webpro_round4_auditCost.md,
n^0.28-0.32) — so the contradiction means the INSTANCE SCALING here is broken, NOT Pro's bound. Do NOT
draw conclusions from this run. A faithful rebuild must keep b*delta/G = O(1) (the packing) intact, i.e.
satellites must NOT blow up the bounding box relative to W_Q. The codex final audit runs its own numerics.
"""
import math, sys, os
import numpy as np
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'sim'))
from scipy.spatial import Delaunay


def build_carpet_satellites(scarp):
    """Carpet: scarp x scarp h-spaced grid (h=1). Satellites: a geometric chain far away."""
    h = 1.0
    gx, gy = np.meshgrid(np.arange(scarp), np.arange(scarp))
    carpet = np.column_stack([gx.ravel(), gy.ravel()]).astype(float) * h
    # satellites: ~scarp of them on a ray with geometric spacing, contributing a constant fraction
    x0 = carpet[:, 0].max() + 4 * scarp
    sats = []
    gap = 4.0 * scarp
    x = x0
    for j in range(scarp):
        sats.append([x, 0.0]); x += gap
    Q = np.vstack([carpet, np.array(sats)])
    return Q, h


def components_cellgraph(Q, a, r):
    """#components (c) and #nonempty cells (N) of the a-cell graph at threshold r (cells within r)."""
    ci = np.floor(Q[:, 0] / a).astype(int); cj = np.floor(Q[:, 1] / a).astype(int)
    cells = {}
    for k in range(len(Q)):
        cells.setdefault((int(ci[k]), int(cj[k])), len(cells))
    cl = list(cells.keys()); N = len(cl)
    idx = {c: i for i, c in enumerate(cl)}
    par = list(range(N))
    def f(x):
        while par[x] != x: par[x] = par[par[x]]; x = par[x]
        return x
    # adjacency: cells whose square-to-square min distance <= r. Use cell centers + conservative test.
    cxy = np.array([[(c[0] + 0.5) * a, (c[1] + 0.5) * a] for c in cl])
    # brute force is O(N^2); fine for the tested sizes
    for i in range(N):
        dx = cxy[:, 0] - cxy[i, 0]; dy = cxy[:, 1] - cxy[i, 1]
        d_centers = np.sqrt(dx * dx + dy * dy)
        # set-distance >= center-distance - sqrt(2)*a ; adjacent if set-dist <= r
        near = np.where(d_centers - math.sqrt(2) * a <= r)[0]
        for jx in near:
            if jx != i:
                ri, rj = f(i), f(int(jx))
                if ri != rj: par[ri] = rj
    comps = len({f(i) for i in range(N)})
    return comps, N


def active_cover_b_delta(Q, q):
    """Subdivide dyadic from the bounding box until >= q nonempty cells; return (b, delta)."""
    ox, oy = Q[:, 0].min(), Q[:, 1].min()
    span = max(Q[:, 0].max() - ox, Q[:, 1].max() - oy) + 1.0
    delta = span
    while True:
        ci = np.floor((Q[:, 0] - ox) / delta).astype(int)
        cj = np.floor((Q[:, 1] - oy) / delta).astype(int)
        b = len(set(zip(ci.tolist(), cj.tolist())))
        if b >= q or delta < 1e-9:
            return b, delta
        delta /= 2.0


if __name__ == "__main__":
    print("Carpet+satellites: check candidate-root (c_j) AND exploration (N_j<=K) budgets ~ O~(sqrt K).")
    print(f"{'scarp':>6} {'K':>7} {'b':>6} {'sqrtK':>6} {'Wq':>10} || "
          f"{'cand/ (TsqrtK)':>15} {'expl/(TsqrtK)':>14} || {'cand/(T*K)':>11} {'expl/(T*K)':>11}")
    beta = 0.25; sigma = beta / 32
    for scarp in [16, 24, 32, 45]:
        Q, h = build_carpet_satellites(scarp)
        K = len(Q); sqrtK = math.sqrt(K)
        # exact W_Q (MST) and G = W_Q (use the true value as the guess for the accounting test)
        pts = Q; n = len(pts); tri = Delaunay(pts)
        we = []
        for s in tri.simplices:
            for x in range(3):
                for y in range(x + 1, 3):
                    u, v = int(s[x]), int(s[y]); we.append((math.dist(pts[u], pts[v]), u, v))
        we.sort(); par = list(range(n))
        def f(x):
            while par[x] != x: par[x] = par[par[x]]; x = par[x]
            return x
        Wq = 0.0; used = 0
        for w, u, v in we:
            ru, rv = f(u), f(v)
            if ru != rv: par[ru] = rv; Wq += w; used += 1
            if used == n - 1: break
        G = Wq
        b, delta = active_cover_b_delta(Q, math.ceil(sqrtK))
        diam = float(max(np.ptp(Q[:, 0]), np.ptp(Q[:, 1])) * math.sqrt(2))
        r0 = max(h, beta * G / (32 * K))
        # geometric scales
        rs = []
        r = r0
        while r < diam:
            rs.append(r); r *= (1 + sigma)
        T = max(1, len(rs))
        cand_sum = 0.0; expl_sum = 0.0
        for r in rs:
            a = h if (h > sigma * r / 128) else max(h, 2 ** math.floor(math.log2(sigma * r / 64)))
            if a > delta:      # coarse scale: explicit, no sampling cost
                continue
            c_j, N_j = components_cellgraph(Q, a, r)
            M_j = b * (delta / a) ** 2
            U_j = 1 + G / r
            alpha_j = beta * G / (32 * T * sigma * r)
            cand_sum += M_j * U_j / (alpha_j ** 2)          # candidate-root (Pro uses U_j>=c_j)
            expl_sum += N_j * U_j / (alpha_j ** 2)          # exploration (uses N_j<=K)
        print(f"{scarp:>6} {K:>7} {b:>6} {sqrtK:>6.0f} {Wq:>10.0f} || "
              f"{cand_sum/(T*sqrtK):>15.3f} {expl_sum/(T*sqrtK):>14.3f} || "
              f"{cand_sum/(T*K):>11.4f} {expl_sum/(T*K):>11.4f}")
    print("\nReading: cols 'cand/(T sqrtK)' and 'expl/(T sqrtK)' should stay BOUNDED/flat as K grows")
    print("(=> both budgets are O~(sqrt K)). If instead 'cand/(T*K)' or 'expl/(T*K)' were flat (and the")
    print("sqrtK-normalized cols grew like sqrtK), that would be the n^{2/3} leak. The carpet maximizes")
    print("N_j=Theta(K) at the floor, so it is the worst case for the exploration (N_j) accounting.")
