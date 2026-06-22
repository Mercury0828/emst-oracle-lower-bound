"""
Gadgets + packings for the Phase-0 de-risking screens.

Faithful reconstruction of the source hard instance (Driemel et al., SoCG 2025,
arXiv:2504.15292 §6, verified from the PDF):
  - domain split into 16·n^{1/3} equal cells, each of side 4·n^{5/6};
  - HEAVY ("uniform") gadget: n^{2/3} points spread on a uniform grid filling a cell
    -> per-cell EMST cost Θ(n^{7/6}) ≈ (cell side)·sqrt(p);
  - SPARSE ("strip") gadget: n^{2/3} points along a 1D strip in the cell
    -> per-cell EMST cost Θ(n^{5/6}) ≈ (cell side);
  - heavy and sparse gadgets have the SAME number of points p (load-bearing: equal
    cardinality makes a fully-contained cell invisible to a counting query).

Here gadgets are parameterized by (p, s) so we can thin p toward ~n^{1/2} (the C1 screen)
and pack m of them on a sqrt(m) x sqrt(m) layout (the C2 screen). Absolute scale cancels in
every ratio we report; we fix s = 1.0 and a small inter-cell gap.

Phase-0 internal de-risking only — NOT a paper result.
"""
from __future__ import annotations

import math

import numpy as np


def _square_side(p: int) -> int:
    """Largest k with k*k <= p (used to lay out a near-square grid of p points)."""
    return max(1, int(math.isqrt(p)))


def heavy_gadget(p: int, origin=(0.0, 0.0), s: float = 1.0, margin: float = 0.05) -> np.ndarray:
    """`p` points on a near-uniform grid filling [0, s]^2 (the 'uniform'/heavy gadget).

    EMST(heavy) ~ s * sqrt(p)  (nearest-neighbour spacing ~ s/sqrt(p), p-1 edges)."""
    ox, oy = origin
    lo, hi = margin * s, (1.0 - margin) * s
    k = _square_side(p)
    xs = np.linspace(lo, hi, k)
    ys = np.linspace(lo, hi, k)
    gx, gy = np.meshgrid(xs, ys)
    pts = np.column_stack([gx.ravel(), gy.ravel()])
    # top up to exactly p points by jittering extra points onto the grid lattice
    if len(pts) < p:
        extra = p - len(pts)
        rng = np.random.default_rng(12345)
        idx = rng.integers(0, len(pts), size=extra)
        jitter = (rng.random((extra, 2)) - 0.5) * (hi - lo) / max(k - 1, 1) * 0.25
        pts = np.vstack([pts, pts[idx] + jitter])
    pts = pts[:p]
    return pts + np.array([ox, oy])


def sparse_gadget(p: int, origin=(0.0, 0.0), s: float = 1.0, margin: float = 0.05) -> np.ndarray:
    """`p` points evenly along a horizontal strip at mid-height (the 'strip'/sparse gadget).

    EMST(sparse) ~ s  (a path along a length-s segment)."""
    ox, oy = origin
    lo, hi = margin * s, (1.0 - margin) * s
    xs = np.linspace(lo, hi, p)
    ys = np.full(p, 0.5 * s)
    pts = np.column_stack([xs, ys])
    return pts + np.array([ox, oy])


def control_gadget(p: int, origin=(0.0, 0.0), s: float = 1.0, margin: float = 0.05) -> np.ndarray:
    """Negative control: a 'heavy' that is actually a strip (no heavy/sparse separation)."""
    return sparse_gadget(p, origin=origin, s=s, margin=margin)


# --------------------------------------------------------------------------------------
# C1: a global instance of m cells, one optionally heavy, the rest sparse.
# --------------------------------------------------------------------------------------
def build_global_instance(
    m: int,
    p: int,
    heavy_index: int | None,
    s: float = 1.0,
    pitch: float = 1.05,
    heavy_fn=heavy_gadget,
) -> np.ndarray:
    """sqrt(m) x sqrt(m) grid of cells; cell `heavy_index` gets a heavy gadget (or none)."""
    side = int(round(math.sqrt(m)))
    assert side * side == m, f"m={m} must be a perfect square"
    chunks = []
    for k in range(m):
        i, j = k % side, k // side
        origin = (i * pitch * s, j * pitch * s)
        if heavy_index is not None and k == heavy_index:
            chunks.append(heavy_fn(p, origin=origin, s=s))
        else:
            chunks.append(sparse_gadget(p, origin=origin, s=s))
    return np.vstack(chunks)


# --------------------------------------------------------------------------------------
# C2: a packing whose per-query coverage we measure. Each cell carries BOTH its heavy and
# its sparse realisation, so coverage(R) = #cells whose heavy/sparse swap changes |P n R|.
# --------------------------------------------------------------------------------------
def build_packing(m: int, p: int, layout: str = "grid", s: float = 1.0, pitch: float = 1.05,
                  seed: int = 0):
    """Return (heavy_xy, heavy_cell, sparse_xy, sparse_cell, cell_origins).

    layout='grid'        : cells on a sqrt(m) x sqrt(m) lattice (the source baseline packing).
    layout='permutation' : cell k at (k, pi(k)) -> disjoint x-bands AND disjoint y-bands
                           (a 'general position' variant: each axis-parallel line meets O(1)
                           cells). This is an obvious-variant probe, NOT the RS proof obligation.
    """
    origins = []
    if layout == "grid":
        side = int(round(math.sqrt(m)))
        assert side * side == m, f"m={m} must be a perfect square"
        for k in range(m):
            i, j = k % side, k // side
            origins.append((i * pitch * s, j * pitch * s))
    elif layout == "permutation":
        rng = np.random.default_rng(seed)
        perm = rng.permutation(m)
        for k in range(m):
            origins.append((k * pitch * s, perm[k] * pitch * s))
    else:
        raise ValueError(layout)

    hx, hc, sx, sc = [], [], [], []
    for k, origin in enumerate(origins):
        h = heavy_gadget(p, origin=origin, s=s)
        sp = sparse_gadget(p, origin=origin, s=s)
        hx.append(h); hc.append(np.full(len(h), k))
        sx.append(sp); sc.append(np.full(len(sp), k))
    return (
        np.vstack(hx), np.concatenate(hc),
        np.vstack(sx), np.concatenate(sc),
        np.array(origins),
    )
