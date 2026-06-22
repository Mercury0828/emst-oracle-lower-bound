"""
Verify the load-bearing claims of GPT-5.5-Pro's round-1 reply (docs/webpro_round1_response.md),
using EXACT EMST. Pro explicitly requested these checks.

(1) Exact multiset identity (Lemma 1): with random ranks and root r,
    tau(v) = min{ bottleneck(v,u) : u=r or pi(u)<pi(v) },  tau(r)=0,
    where bottleneck(v,u) = max edge weight on the (unique) MST path v->u.
    Claim: sorted{ tau(v) : v != r } == sorted{ MST edge weights }.
(2) Random-leader exploration cost on a size-s component ~ 1 + H_{s-1} (= O(log s)), not s.
(3) Rare-bridge instance: two dense grids separated by gap G=Theta(n) -> the death-time multiset
    has exactly ONE Theta(G) value (the tail obstruction).

Run: sim/.venv/Scripts/python.exe attack_loop/webpro_verify_round1.py
"""
import math, sys, os
import numpy as np
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'sim'))
from scipy.spatial import Delaunay


def mst_edges(points):
    """Return list of (i, j, weight) MST edges via Delaunay-candidate Kruskal (exact EMST)."""
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
    we = sorted(((math.dist(pts[i], pts[j]), i, j) for (i, j) in cand))
    parent = list(range(n))
    def find(x):
        while parent[x] != x:
            parent[x] = parent[parent[x]]; x = parent[x]
        return x
    edges = []
    for w, i, j in we:
        ri, rj = find(i), find(j)
        if ri != rj:
            parent[ri] = rj; edges.append((i, j, w))
            if len(edges) == n - 1:
                break
    return edges


def bottleneck_from(v, n, adj):
    """bottleneck(v,u) for all u: max edge on MST path v->u (BFS over the tree)."""
    INF = float('inf'); bott = [INF] * n; bott[v] = 0.0
    stack = [v]; seen = [False] * n; seen[v] = True
    while stack:
        x = stack.pop()
        for (y, w) in adj[x]:
            if not seen[y]:
                seen[y] = True; bott[y] = max(bott[x], w); stack.append(y)
    return bott


def check_multiset_identity(points, seed=0):
    pts = np.asarray(points, float); n = len(pts)
    edges = mst_edges(pts)
    adj = [[] for _ in range(n)]
    for (i, j, w) in edges:
        adj[i].append((j, w)); adj[j].append((i, w))
    rng = np.random.default_rng(seed)
    rank = rng.permutation(n)             # distinct ranks 0..n-1
    r = int(np.argmin(rank))              # root = global min rank (so root's S includes nothing lower)
    # actually root r is a fixed designated vertex; tau(r)=0. Use r = argmin(rank) as the natural root.
    tau = []
    for v in range(n):
        if v == r:
            continue
        bott = bottleneck_from(v, n, adj)
        Sv = [u for u in range(n) if (u == r or rank[u] < rank[v])]
        tau.append(min(bott[u] for u in Sv))
    tau_sorted = np.sort(np.array(tau))
    w_sorted = np.sort(np.array([w for (_, _, w) in edges]))
    ok = np.allclose(tau_sorted, w_sorted, atol=1e-9)
    return ok, tau_sorted, w_sorted


def exploration_cost(s, trials=20000, seed=1):
    """Random-leader exploration on a path component of size s: #vertices inspected before hitting a
    lower-ranked vertex (deterministic order = the path order from a uniform random start)."""
    rng = np.random.default_rng(seed); tot = 0
    for _ in range(trials):
        rank = rng.permutation(s)
        start = int(rng.integers(s))
        order = list(range(s)); order.remove(start); order = [start] + order  # p first, deterministic rest
        inspected = 1
        pr = rank[start]
        for u in order[1:]:
            if rank[u] < pr:
                break
            inspected += 1
        tot += inspected
    return tot / trials


def rare_bridge(n=2000, gap_factor=1.0):
    """Two unit grids of n/2 points each, separated horizontally by gap G ~ n. Report MST edge lengths."""
    h = n // 2; side = int(math.isqrt(h)); h = side * side
    gx, gy = np.meshgrid(np.arange(side), np.arange(side))
    block = np.column_stack([gx.ravel(), gy.ravel()]).astype(float)
    G = gap_factor * n
    left = block.copy()
    right = block.copy(); right[:, 0] += side + G
    pts = np.vstack([left, right])
    edges = mst_edges(pts)
    lens = np.sort(np.array([w for (_, _, w) in edges]))
    return lens, G


if __name__ == "__main__":
    print("=" * 70)
    print("(1) EXACT MULTISET IDENTITY  {tau(v):v!=r} == sorted MST edge weights")
    print("=" * 70)
    rng = np.random.default_rng(7)
    allok = True
    for trial in range(6):
        n = int(rng.integers(20, 130))
        pts = rng.random((n, 2)) * 100.0
        ok, ts, ws = check_multiset_identity(pts, seed=trial)
        allok &= ok
        print(f"  n={n:4d}  identity holds? {ok}   max|tau-w|={np.max(np.abs(ts-ws)):.2e}")
    print(f"  >>> ALL HOLD: {allok}")

    print("\n" + "=" * 70)
    print("(2) RANDOM-LEADER EXPLORATION COST  ~ 1 + H_{s-1}  (not s)")
    print("=" * 70)
    for s in [10, 50, 200, 1000]:
        H = 1 + sum(1.0 / j for j in range(1, s))   # 1 + H_{s-1}
        emp = exploration_cost(s)
        print(f"  s={s:5d}  empirical={emp:7.3f}  1+H_(s-1)={H:7.3f}  (s itself={s})")

    print("\n" + "=" * 70)
    print("(3) RARE BRIDGE: two grids, gap G~n  -> exactly ONE Theta(G) MST edge")
    print("=" * 70)
    for n in [800, 2000, 4500]:
        lens, G = rare_bridge(n)
        nbig = int(np.sum(lens > 0.5 * G))
        print(f"  n~{n:5d}  gap G={G:.0f}  largest MST edge={lens[-1]:.1f}  "
              f"#edges>G/2 = {nbig}  (2nd largest={lens[-2]:.2f})")
