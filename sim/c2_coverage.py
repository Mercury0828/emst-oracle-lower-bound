"""
(C2) Per-query coverage screen — THE decisive measurement (guide.md §6 Component 2, §7).

PRE-REGISTRATION (locked before running; see DESIGN_DECISIONS.md PR-C2):
  Build the baseline packing (m candidate gadgets on a sqrt(m) x sqrt(m) subgrid, one heavy);
  for an axis-aligned range-COUNTING query rectangle R measure its
      candidate-distinguishing-power = #candidate cells whose heavy/sparse flip changes |P n R|
  and report the MAX over rectangles (the adversarial tail), swept as m grows.
  EXPECTATION (guide's optimistic prior): max coverage flat / O(1) (at worst m^{o(1)}).
  FALSIFIER / strength-gate signal: max coverage grows POLYNOMIALLY with m (m^{Omega(1)})
      -> hitting bound Omega(m / coverage) caps the exponent below 1/2 (closes -> improves).
  Adversarial rectangles are the kill metric; random rectangles are a smoke check only.
  SECONDARY proxy: H(count ; hidden-index) for the worst R, reported as a RATIO to log m.
  CONTRAST: emptiness-query coverage on the same packing (hypothesis: <= counting coverage).

  A-priori note (honest, logged before the run): a single axis-parallel rectangle edge can
  slice an entire COLUMN of the sqrt(m) x sqrt(m) grid, partially covering all sqrt(m) cells in
  it; with equal-cardinality gadgets a fully-contained cell is invisible but a straddled one is
  not -> we EXPECT the baseline grid to show max coverage ~ sqrt(m) = m^{1/2} (polynomial), i.e.
  the residual risk realised on the baseline. We also screen a 'permutation' (general-position)
  layout where each axis-parallel line meets O(1) cells, to see whether O(1) coverage is even
  attainable in isolation (it does NOT validate C1 detectability under that layout — the coupled
  obligation). A baseline showing growth is a RED/YELLOW SCREEN, NOT proof the target is dead.

Phase-0 internal de-risking only — NOT a paper result.
"""
from __future__ import annotations

import math

import numpy as np

from gadgets import build_packing

P_PER_CELL = 16  # 4x4 heavy grid vs 16-point strip; coverage is about #cells straddled, not p


def _counts_in_rect(xy, cell, m, rect):
    x0, x1, y0, y1 = rect
    inside = (xy[:, 0] >= x0) & (xy[:, 0] <= x1) & (xy[:, 1] >= y0) & (xy[:, 1] <= y1)
    return np.bincount(cell[inside], minlength=m)


def coverage_counting(packing, m, rect) -> int:
    hx, hc, sx, sc, _ = packing
    ch = _counts_in_rect(hx, hc, m, rect)
    cs = _counts_in_rect(sx, sc, m, rect)
    return int(np.count_nonzero(ch != cs))


def coverage_emptiness(packing, m, rect) -> int:
    hx, hc, sx, sc, _ = packing
    eh = _counts_in_rect(hx, hc, m, rect) > 0
    es = _counts_in_rect(sx, sc, m, rect) > 0
    return int(np.count_nonzero(eh != es))


def _domain(packing):
    hx = packing[0]
    sx = packing[2]
    allp = np.vstack([hx, sx])
    return allp[:, 0].min() - 1.0, allp[:, 0].max() + 1.0, allp[:, 1].min() - 1.0, allp[:, 1].max() + 1.0


def _adversarial_rects(packing, n_cuts=240, n_snap=6000, seed=7):
    """Worst-case family. The adversarial coverage of an axis-aligned rectangle is driven by how
    many cells its 4 boundary edges straddle, AND by the EDGE POSITION inside a cell: a vertical
    edge at a cell centre splits the strip symmetrically (heavy-count = sparse-count, NOT covered),
    so the true worst case needs OFF-CENTRE edges snapped to actual point coordinates (where the
    heavy 4x4 grid jumps by 4 but the strip increments by ~1). This is the gate-1 audit correction:
    the earlier half-plane/centre-cut family understated the constant (found ~2*sqrt(m); the true
    worst case is ~4*sqrt(m)).

    Families:
      - vertical / horizontal half-planes and thin slabs (1 straddling edge);
      - COORDINATE-SNAPPED random rectangles: all 4 edges drawn from midpoints between adjacent
        actual point coordinates (the tight 4-edge adversary used by the gate-1 audit).
    """
    xlo, xhi, ylo, yhi = _domain(packing)
    allp = np.vstack([packing[0], packing[2]])
    xsnap = np.unique(allp[:, 0]); ysnap = np.unique(allp[:, 1])
    xmid = (xsnap[:-1] + xsnap[1:]) / 2.0 if len(xsnap) > 1 else xsnap
    ymid = (ysnap[:-1] + ysnap[1:]) / 2.0 if len(ysnap) > 1 else ysnap
    xs = np.linspace(xlo, xhi, n_cuts)
    ys = np.linspace(ylo, yhi, n_cuts)
    rects = []
    BIG = 1e9
    for a in xs:
        rects.append((-BIG, a, -BIG, BIG))            # vertical half-planes
    for b in ys:
        rects.append((-BIG, BIG, -BIG, b))            # horizontal half-planes
    for i in range(0, n_cuts - 1, max(1, n_cuts // 60)):
        rects.append((xs[i], xs[i + 1], -BIG, BIG))   # thin vertical slabs
    # coordinate-snapped random rectangles (the tight 4-edge adversary)
    rng = np.random.default_rng(seed)
    ax = np.sort(rng.choice(xmid, size=(n_snap, 2)), axis=1)
    ay = np.sort(rng.choice(ymid, size=(n_snap, 2)), axis=1)
    for t in range(n_snap):
        rects.append((ax[t, 0], ax[t, 1], ay[t, 0], ay[t, 1]))
    return rects


def _mi_ratio_for_rect(packing, m, rect) -> float:
    """H(count ; uniform hidden index)/log m for a fixed R. count is a deterministic function
    of which single cell is heavy, so MI(index;count)=H(count)<=log m. Report the ratio."""
    hx, hc, sx, sc, _ = packing
    base = _counts_in_rect(sx, sc, m, rect)            # all-sparse counts per cell
    total_sparse = int(base.sum())
    ch = _counts_in_rect(hx, hc, m, rect)              # heavy counts per cell
    # if cell k is the (only) heavy one, global count = total_sparse - base[k] + ch[k]
    counts = total_sparse - base + ch                  # length m, one per hidden index
    vals, freq = np.unique(counts, return_counts=True)
    pr = freq / freq.sum()
    H = float(-(pr * np.log2(pr)).sum())
    denom = math.log2(m) if m > 1 else 1.0
    return H / denom if denom > 0 else 0.0


def _fit_slope(ms, ys) -> float:
    ms = np.asarray(ms, float); ys = np.asarray(ys, float)
    good = ys > 0
    if good.sum() < 2:
        return float("nan")
    return float(np.polyfit(np.log(ms[good]), np.log(ys[good]), 1)[0])


def measure(m, layout, p=P_PER_CELL, seed=0, n_random=400):
    packing = build_packing(m, p, layout=layout, seed=seed)
    adv = _adversarial_rects(packing)
    cov_counting = [coverage_counting(packing, m, r) for r in adv]
    cov_empty = [coverage_emptiness(packing, m, r) for r in adv]
    j = int(np.argmax(cov_counting))
    worst_rect = adv[j]
    # random rectangles (SMOKE check only)
    rng = np.random.default_rng(1000 + m)
    xlo, xhi, ylo, yhi = _domain(packing)
    rnd = []
    for _ in range(n_random):
        a, b = sorted(rng.uniform(xlo, xhi, 2))
        c, d = sorted(rng.uniform(ylo, yhi, 2))
        rnd.append(coverage_counting(packing, m, (a, b, c, d)))
    rnd = np.array(rnd)
    return dict(
        m=m, layout=layout, p=p, sqrt_m=round(math.sqrt(m), 3),
        adv_max_counting=int(max(cov_counting)),
        adv_max_emptiness=int(max(cov_empty)),
        mi_ratio_worst=round(_mi_ratio_for_rect(packing, m, worst_rect), 4),
        random_mean=round(float(rnd.mean()), 3),
        random_ci95=round(float(1.96 * rnd.std(ddof=1) / math.sqrt(len(rnd))), 3),
        random_max=int(rnd.max()),
    )


def run(ms=None) -> dict:
    if ms is None:
        ms = [16, 36, 64, 100, 144, 196, 256]
    grid = [measure(m, "grid") for m in ms]
    perm = [measure(m, "permutation") for m in ms]
    out = dict(
        p_per_cell=P_PER_CELL, ms=ms,
        grid=grid, permutation=perm,
        grid_counting_slope=_fit_slope(ms, [r["adv_max_counting"] for r in grid]),
        perm_counting_slope=_fit_slope(ms, [r["adv_max_counting"] for r in perm]),
        grid_emptiness_slope=_fit_slope(ms, [r["adv_max_emptiness"] for r in grid]),
    )
    return out


if __name__ == "__main__":
    import json
    print(json.dumps(run(), indent=2))
