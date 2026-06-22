"""
Exact Euclidean MST weight in 2D.

For Euclidean points in the plane the MST is a subgraph of the Delaunay triangulation,
so we extract candidate edges from `scipy.spatial.Delaunay` and run Kruskal / union-find.
For tiny or (near-)collinear inputs (where Delaunay is ill-defined) we fall back to the
complete graph. This gives the EXACT EMST weight (the screens are internal de-risking; we
never approximate the EMST itself).

Phase-0 internal de-risking only (guide.md §7) — NOT a paper result.
"""
from __future__ import annotations

import numpy as np

from scipy.spatial import Delaunay
try:
    from scipy.spatial import QhullError  # type: ignore  (scipy >= 1.8)
except Exception:  # pragma: no cover
    QhullError = Exception  # type: ignore


def _union_find_mst_weight(n: int, edges: np.ndarray, weights: np.ndarray) -> float:
    """Kruskal over the given (i, j) edges with precomputed Euclidean weights."""
    order = np.argsort(weights, kind="stable")
    parent = np.arange(n)
    rank = np.zeros(n, dtype=np.int64)

    def find(x: int) -> int:
        root = x
        while parent[root] != root:
            root = parent[root]
        while parent[x] != root:
            parent[x], x = root, parent[x]
        return root

    total = 0.0
    used = 0
    for idx in order:
        i = int(edges[idx, 0])
        j = int(edges[idx, 1])
        ri, rj = find(i), find(j)
        if ri == rj:
            continue
        if rank[ri] < rank[rj]:
            ri, rj = rj, ri
        parent[rj] = ri
        if rank[ri] == rank[rj]:
            rank[ri] += 1
        total += float(weights[idx])
        used += 1
        if used == n - 1:
            break
    return total


def _complete_graph_edges(n: int) -> np.ndarray:
    iu, ju = np.triu_indices(n, k=1)
    return np.column_stack([iu, ju]).astype(np.int64)


def _delaunay_edges(points: np.ndarray) -> np.ndarray:
    tri = Delaunay(points)
    simp = tri.simplices  # (nsimplex, 3)
    e = np.vstack([simp[:, [0, 1]], simp[:, [1, 2]], simp[:, [0, 2]]])
    e.sort(axis=1)
    e = np.unique(e, axis=0)
    return e.astype(np.int64)


def emst_weight(points: np.ndarray) -> float:
    """Exact Euclidean MST weight of a 2D point set."""
    pts = np.asarray(points, dtype=float)
    n = len(pts)
    if n <= 1:
        return 0.0
    if n <= 3:
        edges = _complete_graph_edges(n)
    else:
        try:
            edges = _delaunay_edges(pts)
        except QhullError:
            edges = _complete_graph_edges(n)
        except Exception:
            edges = _complete_graph_edges(n)
    d = pts[edges[:, 0]] - pts[edges[:, 1]]
    weights = np.sqrt(np.einsum("ij,ij->i", d, d))
    return _union_find_mst_weight(n, edges, weights)


def _brute_force_mst_weight(points: np.ndarray) -> float:
    """Complete-graph Kruskal; used only to cross-check `emst_weight` on small n."""
    pts = np.asarray(points, dtype=float)
    n = len(pts)
    if n <= 1:
        return 0.0
    edges = _complete_graph_edges(n)
    d = pts[edges[:, 0]] - pts[edges[:, 1]]
    weights = np.sqrt(np.einsum("ij,ij->i", d, d))
    return _union_find_mst_weight(n, edges, weights)


if __name__ == "__main__":
    rng = np.random.default_rng(0)
    for n in (4, 10, 50, 200):
        p = rng.random((n, 2)) * 100.0
        a = emst_weight(p)
        b = _brute_force_mst_weight(p)
        assert abs(a - b) < 1e-6, (n, a, b)
        print(f"n={n:4d}  emst={a:.4f}  (matches brute force)")
    print("emst.py self-check OK")
