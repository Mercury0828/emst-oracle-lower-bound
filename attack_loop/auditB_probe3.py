"""
Audit B - Escapes A(hierarchical) and D(multi-needle).

The DECOUPLE result in probe2 was an OVERLAP artifact. The real question for escape A:
can the heavy gadget's internal diameter exceed the inter-center spacing legitimately?
NO -- if gadget footprint > spacing, gadgets collide => points coincide across cells =>
the 'm disjoint candidate cells' structure (and the downstream counting argument) breaks.
So legitimately s <= spacing = L/k, and we are back to the scale-invariant CLUSTER rows.

Here we test the two structurally different escapes:

D (multi-needle / correlated): instead of ONE heavy cell, make HALF the cells heavy in
   YES and ALL sparse in NO. Global gap is now sum of m/2 excesses ~ (m/2)*s*sqrt(p),
   while w(P) ~ s*m. Fraction ~ sqrt(p) = constant?! Does this escape?
   BUT: the lower bound needs a NEEDLE to *locate*. A bulk shift is detectable by a few
   coarse queries. We measure ONLY the gap fraction here (feasibility of detectability),
   and reason separately about query cost.

A-hier (hierarchical sparse): sparse cells are tiny tight clusters (diam ~ sqrt(p)),
   placed so the inter-cluster backbone is a near-1D path (minimal). Does w(P) drop
   below sm, raising the single-heavy fraction?
"""
import sys, os, math
import numpy as np
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "sim"))
from emst import emst_weight


def heavy_grid(p, s, off):
    side = int(round(math.sqrt(p)))
    sp = s * 0.98 / side
    xs, ys = np.meshgrid(np.arange(side) * sp, np.arange(side) * sp)
    return np.column_stack([xs.ravel(), ys.ravel()])[:p] + off


def sparse_strip(p, s, off):
    xs = np.linspace(0, s * 0.98, p)
    return np.column_stack([xs, np.full(p, s * 0.5)]) + off


def sparse_tight(p, s, off):
    side = int(math.ceil(math.sqrt(p)))
    xs, ys = np.meshgrid(np.arange(side), np.arange(side))
    return (np.column_stack([xs.ravel(), ys.ravel()])[:p].astype(float)) + off


def centers(k, L):
    c = (np.arange(k) + 0.5) * (L / k)
    xs, ys = np.meshgrid(c, c)
    return np.column_stack([xs.ravel(), ys.ravel()])


def build(cen, s, p, heavy_set, sparse_fn):
    blocks = []
    for i, c in enumerate(cen):
        off = c - np.array([s / 2, s / 2])
        blocks.append(heavy_grid(p, s, off) if i in heavy_set else sparse_fn(p, s, off))
    return np.vstack(blocks)


def emst(P): return emst_weight(P)


if __name__ == "__main__":
    print("### Escape D: MULTI-NEEDLE (half cells heavy) -- gap fraction only ###")
    for k in (6, 8, 10):
        p = k * k; m = k * k
        Delta = float(m * p); s = Delta / k
        cen = centers(k, Delta)
        Ps = build(cen, s, p, set(), sparse_strip)
        half = set(range(0, m, 2))           # ~ m/2 heavy
        Ph = build(cen, s, p, half, sparse_strip)
        one = build(cen, s, p, {0}, sparse_strip)
        ws, wh, w1 = emst(Ps), emst(Ph), emst(one)
        print(f" k={k} m={m}: 1-needle frac={(w1-ws)/ws:.4f} | "
              f"{len(half)}-needle frac={(wh-ws)/ws:.4f}  (per-needle ~{(wh-ws)/ws/len(half):.4f})")

    print("\n### Escape A-hier: tight sparse clusters (minimize backbone) ###")
    for k in (6, 8, 10):
        p = k * k; m = k * k
        Delta = float(m * p); s = Delta / k
        cen = centers(k, Delta)
        Ps = build(cen, s, p, set(), sparse_tight)   # sparse = tight clusters
        one = build(cen, s, p, {0}, sparse_tight)
        ws, w1 = emst(Ps), emst(one)
        print(f" k={k} m={m}: sparse=tight-cluster, 1-heavy frac={(w1-ws)/ws:.4f}  "
              f"(w_sparse={ws:.3e}, backbone-dominated)")
