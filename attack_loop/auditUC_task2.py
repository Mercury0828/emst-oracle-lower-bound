"""
Task 2: Test the projection/slab repair on codex's filament.

For the SAME filament (diagonal and snake variants):
 - compute 1-D x-projection and y-projection of island positions.
 - Is the filament DENSE in some axis projection / thin axis-aligned slab?
 - Specifically: do width-lambda full-height vertical slabs (or horizontal) each
   contain ~O(1) islands? If so, O(polylog) random slabs + within-slab counting
   recover persistence in o(sqrt n)?

We implement a slab-based importance-sampling estimator over a range-COUNTING oracle
and measure query count vs n.
"""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "sim"))
import numpy as np
from emst import emst_weight
from scipy.spatial import cKDTree


def build_filament(N, variant="diagonal", seed=0):
    lam = float(N)
    n = N * N
    islands = []
    if variant == "diagonal":
        for k in range(N):
            islands.append((k * lam + lam / 2, k * lam + lam / 2))
    elif variant == "snake":
        # boustrophedon over a grid of g_rows x g_cols cells with N cells total.
        # to span both axes, use a snake covering sqrt(N) x sqrt(N)? That only gives N cells
        # but each cell side lambda. consecutive in-row distance = lambda, row-jump = lambda.
        g = N  # N cells in one row -> snake of 1 row is just a line. Use a true 2D snake:
        gr = int(round(np.sqrt(N)))
        gc = int(np.ceil(N / gr))
        cnt = 0
        for r in range(gr):
            cols = range(gc) if r % 2 == 0 else range(gc - 1, -1, -1)
            for c in cols:
                if cnt >= N:
                    break
                islands.append((c * lam + lam / 2, r * lam + lam / 2))
                cnt += 1
    islands = np.array(islands, dtype=float)
    m = n - N
    s = int(np.ceil(np.sqrt(m)))
    X0 = N * lam + 10 * lam
    xs = np.arange(s)
    gx, gy = np.meshgrid(xs, xs)
    bulk = np.column_stack([gx.ravel() + X0, gy.ravel()]).astype(float)[:m]
    P = np.vstack([islands, bulk])
    return P, islands, bulk, lam, n


def projection_slab_density(islands, lam, axis=0):
    """
    Partition the island-coordinate range on `axis` into width-lambda slabs.
    Return: max islands in any slab, mean over NONEMPTY slabs, #nonempty slabs, #islands.
    """
    coord = islands[:, axis]
    lo, hi = coord.min(), coord.max()
    nslabs = int(np.ceil((hi - lo) / lam)) + 1
    counts = np.zeros(nslabs, dtype=int)
    for c in coord:
        b = int((c - lo) // lam)
        counts[b] += 1
    nonempty = counts[counts > 0]
    return counts.max(), nonempty.mean(), len(nonempty), len(islands)


def main():
    print("=== Task 2: projection / slab density of the filament ===")
    for variant in ["diagonal", "snake"]:
        print(f"\n--- variant = {variant} ---")
        print(f"{'N':>4} {'n':>7} | {'x:maxslab':>9} {'x:#ne':>6} | "
              f"{'y:maxslab':>9} {'y:#ne':>6} | {'#islands':>8}")
        for N in [8, 16, 32, 64]:
            P, islands, bulk, lam, n = build_filament(N, variant=variant)
            xmax, xmean, xne, ni = projection_slab_density(islands, lam, axis=0)
            ymax, ymean, yne, _ = projection_slab_density(islands, lam, axis=1)
            print(f"{N:>4} {n:>7} | {xmax:>9} {xne:>6} | {ymax:>9} {yne:>6} | {ni:>8}")
    print()
    print("Reading: if EITHER axis has 'maxslab' large (Theta(N)) the filament is DENSE")
    print("in that projection -> a width-lambda slab on that axis contains many islands,")
    print("so O(polylog) random slabs on that axis each return a big count -> slab repair WORKS.")
    print("If BOTH axes have maxslab = O(1), no single slab is dense -> slab repair in doubt.")


if __name__ == "__main__":
    main()
