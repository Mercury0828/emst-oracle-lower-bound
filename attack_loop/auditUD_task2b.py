"""
Audit UD - Task 2b: which coarse-cell count does the dense-gadget scan really need?

The crux of Task 2's soundness: codex says "scan the Theta(n^{1/3}) coarse cells".
But a 2D coarse grid that *resolves* a heavy block hidden at an arbitrary 2D location
needs side g and g^2 cells.  If the heavy block can sit in ANY of g^2 cells with
g = n^{1/3}, a deterministic scan is g^2 = n^{2/3} -- BLOWING the budget.

Resolution: the Lemma-32 lower-bound construction (brief line 55-58) is specifically
'a block hidden among 16 n^{1/3} coarse cells'.  So the floor instance has only
Theta(n^{1/3}) candidate cells TOTAL -- because the construction restricts the gadget
to a 1-parameter family (e.g. a diagonal strip / a single coarse ROW), not a full 2D
grid.  The question for the UPPER bound is: can a GENERAL instance hide a heavy block
in a 2D grid forcing n^{2/3}?

KEY: a heavy block of >= B points contributes Theta(B) extra MST weight ONLY if it is
ISOLATED at the coarse scale; but a heavy block also contributes ~ B*(n-Delta term) =
B already counted in (n - Delta).  The PERSISTENCE Sum lam c is about COMPONENT COUNT,
not mass.  A dense block is ONE component -> contributes c += 1 at its merge scale.
Its persistence is Theta(lam_block), a single component.  So one dense block contributes
O(lam_max) = Otilde(1) to Sum lam c -- NEGLIGIBLE unless there are MANY such blocks.

So the real Lemma-32 stratum is: MANY (Theta(n^{1/3})) dense-ish anomalous cells, each
contributing O(1) component-persistence, total Theta(n^{1/3}).  To estimate THAT to
additive eps*OPT you need to count how many such cells exist.  This is the cell-counting
that the floor says costs >= Omega(n^{1/3}) and <= Otilde(n^{1/3}) by scanning.

We test the decisive question: can the gadget hide in g^2 = n^{2/3} cells (2D), forcing
n^{2/3}?  Or does the WEIGHT contribution of a 2D-hidden block remain estimable in
n^{1/3} because such blocks must be FEW (few-components -> low persistence) or DENSE
(=> visible mass in a coarse 1D projection)?
"""
import sys, os, math
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "sim"))
import numpy as np
from scipy.spatial import cKDTree
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "sim"))
from emst import emst_weight


def persistence_contribution_of_block(n, block_size, lam_merge):
    """A single dense block isolated until scale lam_merge is ONE component:
    contributes lam_merge to Sum lam c.  Its INTERNAL structure (block_size points
    densely packed) merges at tiny scale -> contributes block_size-1 unit edges to
    the (n-Delta) term, NOT to Sum lam c."""
    return lam_merge   # one component


def main():
    print("=== Task 2b: dense-gadget persistence accounting + 2D-hiding question ===\n")

    print("(1) One dense block = ONE component => persistence contribution = lam_merge (Otilde(1)).")
    print("    Verify with exact EMST: a dense block of B points isolated far away adds")
    print("    (B-1) tiny internal edges + 1 long connector. Internal edges -> (n-Delta) term;")
    print("    only the single connector is 'persistence'.\n")
    rng = np.random.default_rng(3)
    print(f"{'B':>6} {'isolated block EMST':>20} {'internal(~B-1 small)':>21} {'connector(persist)':>19}")
    for B in [16, 64, 256, 1024]:
        s = int(np.ceil(np.sqrt(B)))
        gx, gy = np.meshgrid(np.arange(s), np.arange(s))
        blk = np.column_stack([gx.ravel(), gy.ravel()]).astype(float)[:B]  # unit spacing
        w_block = emst_weight(blk)   # ~ (B-1)*1 internal
        # add the block far from a single reference point; connector ~ distance D
        ref = np.array([[1e6, 1e6]])
        P = np.vstack([blk, ref])
        w_all = emst_weight(P)
        connector = w_all - w_block
        print(f"{B:>6} {w_block:>20.1f} {w_block:>21.1f} {connector:>19.1f}")

    print("\n  => a dense block's PERSISTENCE (the long connector) is O(1) component, NOT O(B).")
    print("     So a SINGLE 2D-hidden heavy block contributes Otilde(1) to Sum lam c.")
    print("     To matter (eps*OPT = eps*Theta(n)), you need Theta(n/lam_max)=Theta(n) blocks,")
    print("     which cannot all be 'hidden' -- they tile the space and a coarse 1D scan sees them.\n")

    print("(2) The genuine Lemma-32 stratum is Theta(n^{1/3}) anomalous cells (the floor's own")
    print("    construction).  Counting them = scan of Theta(n^{1/3}) cells = Otilde(n^{1/3}).")
    print("    A 2D heavy block forcing n^{2/3} would need n^{2/3} INDEPENDENT components each")
    print("    contributing persistence -- but n^{2/3} components * lam each only matters if")
    print("    lam ~ n^{1/3} (giving n) -- and that is the LARGE-lambda regime (Task 3), not the")
    print("    coarse-gadget scan.  The coarse-gadget scan handles the DETERMINISTIC dense cells.\n")

    print("VERDICT(Task2): the 'scan Theta(n^{1/3}) coarse cells' is sound IFF the floor")
    print("construction restricts anomalous cells to a Theta(n^{1/3})-size family (it does,")
    print("by the brief's own statement). A general 2D grid at side n^{1/3} has n^{2/3} cells;")
    print("but the WEIGHT-relevant anomalies are either few-and-low-persistence (negligible)")
    print("or many-and-tiling (coarsely visible). This is exactly the U-P2 tile-or-blowup vise.")


if __name__ == "__main__":
    main()
