"""
Step 2: is the P1 single-cell EMST cap ADDITIVE over k active cells, or could a
CORRELATED active set produce a SUPER-additive gap >> k*O(s sqrt p)?

We build a global instance: M cells in a (disjoint-projection) diagonal/permutation layout.
A subset of k cells is 'active' = heavy, the rest sparse. Compare to all-sparse.
Measure total EMST gap vs k. If gap grows linearly in k (slope ~1 in log-log near k small,
or gap/k roughly constant) -> additive. Super-additive would show gap/k INCREASING with k.

We also test an adversarial CORRELATED placement: active cells chosen to be mutually
adjacent / aligned so their heavy gadgets could in principle interact through the backbone.
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
    xs = np.linspace(lo, hi, k*k)
    ys = np.full(k*k, 0.5*s)
    return np.column_stack([xs, ys]) + np.array(origin)


def build_instance(origins, active_set, s, k):
    chunks = []
    for idx, o in enumerate(origins):
        if idx in active_set:
            chunks.append(heavy(o, s, k))
        else:
            chunks.append(sparse(o, s, k))
    return np.vstack(chunks)


def perm_origins(M, s, pitch=1.05, seed=0):
    rng = np.random.default_rng(seed)
    perm = rng.permutation(M)
    return [(i*pitch*s, perm[i]*pitch*s) for i in range(M)]

def diag_origins(M, s, pitch=1.05):
    # active cells adjacent along the diagonal -> maximal potential interaction
    return [(i*pitch*s, i*pitch*s) for i in range(M)]


if __name__ == "__main__":
    s = 1.0; k = 6; p = k*k
    M = 36
    origins = perm_origins(M, s, seed=1)
    base = build_instance(origins, set(), s, k)
    w_base = emst_weight(base)
    per_cell_max = s*math.sqrt(p)
    print(f"M={M} p={p}  w_all_sparse={w_base:.3f}  s*sqrt(p)={per_cell_max:.3f}")
    print(" k_active   gap      gap/k    gap/(k*s*sqrt(p))")
    rng = np.random.default_rng(5)
    for kact in (1, 2, 4, 8, 16, 24, 36):
        active = set(rng.choice(M, size=kact, replace=False).tolist())
        w = emst_weight(build_instance(origins, active, s, k))
        gap = w - w_base
        print(f"  {kact:3d}    {gap:8.3f}  {gap/kact:7.3f}   {gap/(kact*per_cell_max):.4f}")

    print("\n--- adversarial: active cells packed ADJACENT on the diagonal ---")
    dorig = diag_origins(M, s)
    base_d = emst_weight(build_instance(dorig, set(), s, k))
    print(f"  diag all-sparse w={base_d:.3f}")
    for kact in (1, 2, 4, 8, 16, 36):
        active = set(range(kact))  # first kact cells (adjacent)
        w = emst_weight(build_instance(dorig, active, s, k))
        gap = w - base_d
        print(f"  k={kact:3d}  gap={gap:8.3f}  gap/k={gap/kact:7.3f}  gap/(k*s*sqrt(p))={gap/(kact*per_cell_max):.4f}")
