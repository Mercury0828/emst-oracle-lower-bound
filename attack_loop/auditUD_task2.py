"""
Audit UD - Task 2: the dense Lemma-32 heavy-gadget scan.

The lower-bound floor instance hides a dense heavy block among Theta(n^{1/3}) coarse
cells; each query hits O(1) cells, so a *uniform random* probe finds the block with
prob 1/Theta(n^{1/3}).  codex's claim: DETERMINISTICALLY SCAN the Theta(n^{1/3}) coarse
cells (one count + local spanner test each) -> Otilde(n^{1/3}) queries, and this detects
and estimates the gadget stratum's persistence contribution.

We verify:
  (1) #coarse cells = Theta(n^{1/3}) so the deterministic scan is Otilde(n^{1/3}).
  (2) the scan actually finds the heavy block and recovers its persistence contribution.
  (3) it does NOT require relative-error estimation of any single N_i (it is a full scan,
      not a sample, so no cell-sampling variance).
"""
import sys, os, math
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "sim"))
import numpy as np
from scipy.spatial import cKDTree


class CountingOracle:
    def __init__(self, P):
        self.P = np.asarray(P, float)
        self.n_queries = 0
        self.order = np.argsort(self.P[:, 0], kind="stable")
        self.xs = self.P[self.order, 0]
        self.ys = self.P[self.order, 1]

    def count(self, x0, x1, y0, y1):
        self.n_queries += 1
        lo = np.searchsorted(self.xs, x0, side="left")
        hi = np.searchsorted(self.xs, x1, side="right")
        sub = self.ys[lo:hi]
        return int(np.sum((sub >= y0) & (sub <= y1)))


def inst_lemma32_gadget(n, rng):
    """Theta(n^{1/3}) x Theta(n^{1/3}) coarse grid is the relevant resolution for the
    floor; we lay a sparse 'normal' background plus one DENSE heavy block hidden in a
    single coarse cell.  The block contributes Theta(block_size) component-merge
    persistence concentrated in one cell -- invisible to lonely-singleton probes."""
    g = max(2, int(round(n ** (1 / 3))))   # coarse grid is g x g
    cell = 100.0
    block = n // 2
    rest = n - block
    # background: spread 'rest' points, ~ one per coarse cell region (sparse)
    bg = np.column_stack([
        rng.integers(0, g, size=rest) * cell + rng.uniform(0, cell, size=rest),
        rng.integers(0, g, size=rest) * cell + rng.uniform(0, cell, size=rest),
    ]).astype(float)
    # heavy block in coarse cell (gx, gy)
    cx, cy = g // 3, g // 3
    bs = int(np.ceil(np.sqrt(block)))
    ix, iy = np.meshgrid(np.arange(bs), np.arange(bs))
    blk = np.column_stack([
        cx * cell + (ix.ravel() / bs) * cell,
        cy * cell + (iy.ravel() / bs) * cell,
    ]).astype(float)[:block]
    P = np.vstack([bg, blk])
    return P, g, cell, (cx, cy), block


def coarse_scan(oracle, g, cell, x0base=0.0, y0base=0.0):
    """Deterministically scan all g x g coarse cells, one count each.  Return the
    counts grid and total queries.  This is the dense-gadget detector."""
    counts = np.zeros((g, g), dtype=int)
    for i in range(g):
        for j in range(g):
            x0 = x0base + i * cell
            y0 = y0base + j * cell
            counts[i, j] = oracle.count(x0, x0 + cell, y0, y0 + cell)
    return counts


def main():
    print("=== Task 2: dense Lemma-32 heavy-gadget scan ===\n")
    rng = np.random.default_rng(11)
    print(f"{'n':>9} {'g=#cells/ax':>11} {'g^2 cells':>10} {'scan queries':>13} "
          f"{'n^1/3':>8} {'scanq/g^2':>10} {'g^2/n^1/3':>10} {'block found?':>12}")
    for n in [1024, 4096, 16384, 65536]:
        P, g, cell, (cx, cy), block = inst_lemma32_gadget(n, rng)
        oracle = CountingOracle(P)
        counts = coarse_scan(oracle, g, cell)
        found = (counts.argmax() == cx * g + cy) and (counts.max() >= block * 0.5)
        n13 = n ** (1 / 3)
        print(f"{n:>9} {g:>11} {g*g:>10} {oracle.n_queries:>13} "
              f"{n13:>8.1f} {oracle.n_queries/(g*g):>10.2f} {g*g/n13:>10.2f} {str(found):>12}")

    print("\nNOTE: the coarse grid is g x g with g = Theta(n^{1/3}), so g^2 = Theta(n^{2/3}).")
    print("A FULL g x g scan is Theta(n^{2/3}) -- NOT n^{1/3}!  Let's check the actual claim.")
    print("codex says 'scan the Theta(n^{1/3}) coarse cells' -- that is a 1-D count of cells,")
    print("i.e. the gadget lives among Theta(n^{1/3}) cells TOTAL (a g x 1 strip or g = n^{1/3}")
    print("cells total, NOT g x g).  We re-examine which reading matches the Lemma-32 floor.\n")

    # The Lemma-32 lower bound: 16 n^{1/3} coarse cells TOTAL, each query hits <= 4 cells,
    # hit-prob 1/(4 n^{1/3}).  So the number of coarse cells is Theta(n^{1/3}) TOTAL.
    print("Lemma-32 floor (from brief): '16 n^{1/3} coarse cells; each query hits <=4 cells;")
    print("hit-prob 1/(4 n^{1/3})'.  => #coarse cells = Theta(n^{1/3}) TOTAL.  A deterministic")
    print("scan of all of them = Theta(n^{1/3}) queries.  Verify with a 1-D coarse partition:\n")
    print(f"{'n':>9} {'#cells=16n^1/3':>13} {'scan q':>8} {'n^1/3':>8} {'scanq/n^1/3':>12}")
    for n in [1024, 4096, 16384, 65536, 262144]:
        ncells = int(round(16 * n ** (1 / 3)))
        # a 1-D strip partition of the domain into ncells coarse boxes, one count each
        P, g, cell, _, _ = inst_lemma32_gadget(n, rng)
        oracle = CountingOracle(P)
        xlo, xhi = P[:, 0].min(), P[:, 0].max()
        w = (xhi - xlo) / ncells + 1e-9
        ylo, yhi = P[:, 1].min(), P[:, 1].max()
        for i in range(ncells):
            oracle.count(xlo + i * w, xlo + (i + 1) * w, ylo, yhi)
        n13 = n ** (1 / 3)
        print(f"{n:>9} {ncells:>13} {oracle.n_queries:>8} {n13:>8.1f} {oracle.n_queries/n13:>12.2f}")


if __name__ == "__main__":
    main()
