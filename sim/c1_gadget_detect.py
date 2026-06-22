"""
(C1) Gadget-detectability screen  (guide.md §6 Component 1, §7).

PRE-REGISTRATION (locked before running; see DESIGN_DECISIONS.md PR-C1):
  Build the source uniform(heavy)/strip(sparse) gadgets as a frozen anchor; reconfirm their
  heavy/sparse EMST-cost separation; then THIN the per-cell budget p toward ~n^{1/2}.
  Quantity measured: the heavy-vs-sparse GLOBAL w(P) gap as a fraction of total w(P),
      gap_frac(n, theta) = ( w(one-heavy) - w(all-sparse) ) / w(all-sparse),
  sweeping p = n^theta with theta in [1/2, 2/3] (so m = n^{1-theta} cells), at several n.
  EXPECTATION: gap_frac stays >= a fixed eps (form: a constant fraction of w(P)).
  FALSIFIER / kill signal: gap_frac shrinks below eps and KEEPS shrinking as p -> n^{1/2}.
  NEGATIVE CONTROL: with heavy := strip (no separation), gap_frac ~ 0.
  SCALE CAVEAT: at a few thousand points the p-budgets differ by only a small factor; the
  screen shows the TREND, not the asymptotic crossover.

  A-priori note (honest, logged before the run): the naive source gadget has heavy/sparse
  ratio ~ sqrt(p) while keeping gap_frac = Theta(1) needs ratio ~ m; as p -> n^{1/2} the
  naive ratio sqrt(p)=n^{1/4} falls short of m=n^{1/2}, so we EXPECT the baseline gap_frac to
  decline. A declining baseline is a finding that localises the C1 burden (the attacker must
  design a more point-efficient heavy gadget), NOT proof the target is dead.

Phase-0 internal de-risking only — NOT a paper result.
"""
from __future__ import annotations

import math

import numpy as np

from emst import emst_weight
from gadgets import build_global_instance, heavy_gadget, control_gadget

EPS = 0.10  # illustrative (1 +/- eps) detectability threshold (a fixed constant)


def _round_perfect_square(x: float) -> int:
    k = max(1, int(round(math.sqrt(x))))
    return k * k


def gap_fraction(n_target: int, theta: float, heavy_fn=heavy_gadget) -> dict:
    """One sweep point: p ~ n^theta, m = n/p (rounded to a perfect square)."""
    p = max(4, int(round(n_target ** theta)))
    p = _round_perfect_square(p)               # heavy needs a square grid
    m = max(4, _round_perfect_square(n_target / p))
    n_actual = m * p
    heavy_idx = (int(round(math.sqrt(m))) // 2) * (int(round(math.sqrt(m))) + 1)  # ~center cell
    heavy_idx = min(heavy_idx, m - 1)

    pts_sparse = build_global_instance(m, p, heavy_index=None)
    pts_heavy = build_global_instance(m, p, heavy_index=heavy_idx, heavy_fn=heavy_fn)
    w_sparse = emst_weight(pts_sparse)
    w_heavy = emst_weight(pts_heavy)
    frac = (w_heavy - w_sparse) / w_sparse if w_sparse > 0 else float("nan")
    return dict(
        n_target=n_target, theta=round(theta, 4), p=p, m=m, n_actual=n_actual,
        w_sparse=w_sparse, w_heavy=w_heavy, gap_frac=frac,
        detectable=bool(frac >= EPS),
    )


def run(thetas=None, ns=None) -> dict:
    if thetas is None:
        thetas = [0.50, 0.5417, 0.5833, 0.625, 0.667]
    if ns is None:
        ns = [2025, 4096, 8100]
    rows = []
    for n in ns:
        for th in thetas:
            rows.append(gap_fraction(n, th))
    # negative control at the densest n, swept over theta (heavy := strip)
    control = [gap_fraction(max(ns), th, heavy_fn=control_gadget) for th in thetas]
    # smallest point-budget (largest theta-as-fraction-of-n, i.e. smallest p exponent) at which
    # detectability still survives, per n
    smallest = {}
    for n in ns:
        surviving = [r for r in rows if r["n_target"] == n and r["detectable"]]
        if surviving:
            best = min(surviving, key=lambda r: r["p"])
            smallest[n] = dict(p=best["p"], theta=best["theta"], gap_frac=best["gap_frac"])
        else:
            smallest[n] = None
    return dict(eps=EPS, rows=rows, control=control, smallest_detectable_budget=smallest)


if __name__ == "__main__":
    import json
    out = run()
    print(json.dumps(out, indent=2))
