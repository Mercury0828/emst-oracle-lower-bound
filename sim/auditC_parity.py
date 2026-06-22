"""
The decisive test for the parity/high-order-correlation escape (Steps 5/6 core).

Idea of the escape: LOW and HIGH worlds have IDENTICAL low-order (O(1)-cell) marginals,
including adjacent-pair marginals, so no O(1)-coverage query distinguishes them; but they
differ in a global PARITY of cell-states, and that parity shifts EMST by Theta(w).

The solver argues this is impossible because EMST is ~local/Lipschitz: flipping one cell
changes w by ~its local influence (independent of others), so w = sum of local terms + small
residual; a parity (which is a high-order function) cannot be expressed by / cannot move a
sum-of-local-terms by Theta(w).

We test the QUANTITATIVE claim: define f(x) = EMST as a function of the cell-state vector
x in {sparse=0, heavy=1}^M (spread permutation layout). Estimate the "non-local" energy:
  - the mean and the FIRST-ORDER (additive) approximation f_lin(x) = w0 + sum_i a_i x_i
  - residual R(x) = f(x) - f_lin(x).  If ||R|| << gap, EMST is essentially additive and
    NO function of x with vanishing low-order marginals (like global parity) can be detected
    by EMST either -> the LOW/HIGH EMST gap of a parity coupling is tiny -> escape fails.

We estimate a_i by single-flip increments from all-sparse, then measure residual on random x.
"""
from __future__ import annotations
import math
import numpy as np
import sys
sys.path.insert(0, ".")
from emst import emst_weight


def heavy(origin, s, k):
    lo, hi = 0.05*s, 0.95*s
    xs = np.linspace(lo, hi, k); ys = np.linspace(lo, hi, k)
    gx, gy = np.meshgrid(xs, ys)
    return np.column_stack([gx.ravel(), gy.ravel()]) + np.array(origin)

def sparse(origin, s, k):
    lo, hi = 0.05*s, 0.95*s
    xs = np.linspace(lo, hi, k*k); ys = np.full(k*k, 0.5*s)
    return np.column_stack([xs, ys]) + np.array(origin)

def perm_origins(M, s, pitch=1.05, seed=0):
    rng = np.random.default_rng(seed)
    perm = rng.permutation(M)
    return [(i*pitch*s, perm[i]*pitch*s) for i in range(M)]

def build(origins, x, s, k):
    chunks = [heavy(o,s,k) if x[i] else sparse(o,s,k) for i,o in enumerate(origins)]
    return np.vstack(chunks)


if __name__ == "__main__":
    s = 1.0; k = 5; M = 25
    origins = perm_origins(M, s, seed=3)
    x0 = np.zeros(M, dtype=int)
    w0 = emst_weight(build(origins, x0, s, k))
    # additive coefficients a_i via single flip from all-sparse
    a = np.zeros(M)
    for i in range(M):
        xi = x0.copy(); xi[i] = 1
        a[i] = emst_weight(build(origins, xi, s, k)) - w0
    print(f"w0(all sparse)={w0:.3f}, mean a_i={a.mean():.4f}, full-heavy additive pred gap={a.sum():.3f}")
    w_full = emst_weight(build(origins, np.ones(M,int), s, k))
    print(f"actual full-heavy gap={w_full-w0:.3f}  (additive predicts {a.sum():.3f}) "
          f"ratio={(w_full-w0)/a.sum():.4f}")

    # residual of additive model on random states
    rng = np.random.default_rng(11)
    res = []
    for _ in range(60):
        x = (rng.random(M) < 0.5).astype(int)
        w = emst_weight(build(origins, x, s, k))
        lin = w0 + a @ x
        res.append(w - lin)
    res = np.array(res)
    gap_scale = a.sum()  # the Theta(w) gap a parity would need to fake
    print(f"\nresidual R(x)=f-f_lin over random x:  mean={res.mean():.4f} std={res.std():.4f} "
          f"max|R|={np.abs(res).max():.4f}")
    print(f"residual std / full-gap = {res.std()/gap_scale:.4f}  "
          f"max|R| / full-gap = {np.abs(res).max()/gap_scale:.4f}")
    print("Interpretation: a global-parity LOW/HIGH coupling with matched low-order marginals")
    print("can move EMST by at most ~||residual||; if that is << gap, the parity escape FAILS.")

    # Direct parity test: LOW = even-weight x's, HIGH = odd-weight x's, same per-coordinate
    # marginal (1/2). Compare E[EMST] under the two. (small-M exact-ish via sampling)
    even_w, odd_w = [], []
    for _ in range(400):
        x = (rng.random(M) < 0.5).astype(int)
        w = emst_weight(build(origins, x, s, k))
        if x.sum() % 2 == 0: even_w.append(w)
        else: odd_w.append(w)
    ew, ow = np.mean(even_w), np.mean(odd_w)
    print(f"\nE[EMST | even parity]={ew:.3f}  E[EMST | odd parity]={ow:.3f}  diff={abs(ew-ow):.4f}")
    print(f"parity-induced EMST gap / full-gap = {abs(ew-ow)/gap_scale:.5f}")
