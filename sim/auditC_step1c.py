"""
Step 1c: The DECISIVE scaling test for Step 1's claim s <= O(n/M).

The solver's chain:  O(1) coverage  =>  disjoint x- and y-projections
                                    =>  M cells need M disjoint x-bands each of width >= s
                                    =>  total x-extent >= M*s  <= Delta = O(n)
                                    =>  M*s <= O(n)  =>  s <= O(n/M) = O(p).

CRITICAL: is "disjoint x-projection" really forced by O(1) coverage, or does bounded
(O(1)) x-projection MULTIPLICITY (not 1) suffice -- which only changes constants, NOT the
M*s <= O(Delta) scaling?

If max x-projection multiplicity is t, then summing cell widths: the x-axis [0,Delta] is
covered with multiplicity <= t, so M*s <= t*Delta. With t=O(1), still M*s <= O(Delta)=O(n).

So the binding fact is: O(1) coverage => O(1) projection multiplicity => M*s <= O(n).
We TEST the first implication empirically: across layouts, does coverage scale with
projection multiplicity? And can we get high projection multiplicity WITH O(1) coverage?

We search hard for a counterexample: a layout with HIGH x-projection multiplicity
(t = omega(1), so M*s >> Delta possible) yet O(1) adversarial coverage.
"""
from __future__ import annotations
import math
import numpy as np
from auditC_step1 import max_coverage
from auditC_step1b import projection_multiplicity, density


def report(name, origins, s, p=16, n_snap=12000):
    mc = max_coverage(origins, s, p, n_snap=n_snap)
    xm, ym = projection_multiplicity(origins, s)
    print(f"{name:42s} m={len(origins):4d} maxcov={mc:3d} xproj={xm:3d} yproj={ym:3d}")
    return mc, xm, ym


def layout_staircase_overlap(m, overlap_frac, s=1.0):
    """Cells on a diagonal but with x-intervals OVERLAPPING by overlap_frac.
    pitch_x = (1-overlap_frac)*s. As overlap_frac->1, x-projection multiplicity grows,
    packing M cells into x-extent ~ M*(1-overlap)*s << M*s. Tests: does coverage stay O(1)?"""
    px = (1 - overlap_frac) * s
    py = 1.05 * s
    return [(k*px, k*py) for k in range(m)], s


def layout_diag_tight(m, x_extent, s=1.0):
    """Force M cells into a fixed x-extent x_extent (so x-proj multiplicity ~ M*s/x_extent),
    y still a permutation/diagonal with full spread. If x_extent << M*s, projections collide."""
    px = x_extent / m
    py = 1.05 * s
    rng = np.random.default_rng(0)
    perm = rng.permutation(m)
    return [(k*px, perm[k]*py) for k in range(m)], s


if __name__ == "__main__":
    print("--- staircase with x-overlap (try to pack tight while keeping cov low) ---")
    for ov in (0.0, 0.5, 0.8, 0.9, 0.95):
        report(f"staircase ov={ov}", *layout_staircase_overlap(64, ov), n_snap=8000)

    print("\n--- diagonal forced into shrinking x_extent (m=64, s=1) ---")
    for xe in (64.0, 32.0, 16.0, 8.0, 4.0):
        # x_extent measured in units of s; multiplicity ~ 64*1/xe
        report(f"x_extent={xe}", *layout_diag_tight(64, xe), n_snap=8000)

    print("\n--- the key question: coverage vs x-projection multiplicity ---")
    print("If coverage tracks xproj multiplicity, then O(1) cov => O(1) mult => M*s<=O(Delta).")
