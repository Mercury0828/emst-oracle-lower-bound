"""
Audit B escape probes for the C1 impossibility argument.

Solver's claim: gap/w(P) <= O(sqrt(p)/m), forcing c >= 2/3.
Two load-bearing bounds:
  (UB) one-cell gap <= O(s*sqrt(p))
  (LB) backbone w(P) >= c0 * s * m   (requires every tiling cell occupied & spread out)

We numerically test whether dropping frozen assumptions escapes the sqrt(p)/m cap,
at the TARGET regime p ~ n^{1/2}, m ~ n^{1/2}.

Model: m = k^2 cells tiling [Delta]^2, Delta ~ n, cell side s = Delta/k.
One-heavy vs all-sparse. gap_frac = (w_heavy - w_sparse)/w_sparse.
"""
import sys, os, math
import numpy as np
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "sim"))
from emst import emst_weight


def make_grid_cell_centers(k, s):
    cx = (np.arange(k) + 0.5) * s
    xs, ys = np.meshgrid(cx, cx)
    return np.column_stack([xs.ravel(), ys.ravel()])  # m = k^2 centers


def sparse_strip(p, s, offset):
    """p points on a horizontal line spanning the cell of side s (source SPARSE)."""
    xs = np.linspace(0, s * 0.98, p)
    pts = np.column_stack([xs, np.full(p, s * 0.5)])
    return pts + offset


def sparse_cluster(p, s, offset):
    """p points clustered at one spot (near-coincident). EMST ~ 0. Escape C."""
    # min spacing 1 (integer grid honesty) but tiny footprint
    side = int(math.ceil(math.sqrt(p)))
    xs, ys = np.meshgrid(np.arange(side), np.arange(side))
    pts = np.column_stack([xs.ravel(), ys.ravel()])[:p].astype(float)
    return pts + offset  # footprint ~ sqrt(p) x sqrt(p), spacing 1


def heavy_grid(p, s, offset):
    """p points on uniform grid filling cell of side s (source HEAVY). EMST ~ s*sqrt(p)."""
    side = int(round(math.sqrt(p)))
    sp = s * 0.98 / side
    xs, ys = np.meshgrid(np.arange(side) * sp, np.arange(side) * sp)
    pts = np.column_stack([xs.ravel(), ys.ravel()])
    if len(pts) > p:
        pts = pts[:p]
    return pts + offset


def build_instance(centers, s, p, heavy_idx, sparse_fn, heavy_fn):
    blocks = []
    for i, c in enumerate(centers):
        off = c - np.array([s / 2, s / 2])
        if i == heavy_idx:
            blocks.append(heavy_fn(p, s, off))
        else:
            blocks.append(sparse_fn(p, s, off))
    return np.vstack(blocks)


def run(k, p, sparse_fn, heavy_fn, label):
    m = k * k
    # Delta = n = m*p ; s = Delta/k
    n = m * p
    Delta = float(n)
    s = Delta / k
    centers = make_grid_cell_centers(k, s)
    P_sparse = build_instance(centers, s, p, -1, sparse_fn, heavy_fn)
    P_heavy = build_instance(centers, s, p, 0, sparse_fn, heavy_fn)
    w_s = emst_weight(P_sparse)
    w_h = emst_weight(P_heavy)
    frac = (w_h - w_s) / w_s if w_s > 0 else float("inf")
    print(f"[{label}] k={k} m={m} p={p} n={n} s={s:.1f} | w_sparse={w_s:.3e} "
          f"w_heavy={w_h:.3e} gap_frac={frac:.4f}  (sqrt(p)/m={math.sqrt(p)/m:.4f})")
    return frac


if __name__ == "__main__":
    print("=== TARGET regime p ~ n^{1/2}, m ~ n^{1/2}  (cell sizes scale so p=m approx) ===")
    # choose k so that p ~ m = k^2  -> p = k^2
    for k in (4, 6, 8, 10):
        m = k * k
        p = m  # p ~ m  => c = 1/2 regime (p=n^{1/2}, m=n^{1/2})
        print(f"\n-- k={k}, m=p={m} (n={m*p}) --")
        run(k, p, sparse_strip, heavy_grid, "STRIP vs GRID (source/naive)")
        run(k, p, sparse_cluster, heavy_grid, "CLUSTER vs GRID (escape C)")
