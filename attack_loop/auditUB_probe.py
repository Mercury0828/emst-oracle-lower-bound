"""
Audit UB probe: verify codex's round-2 obstruction (parts 1-3) AND probe the
importance-sampling crack (part 4) for the sub-sqrt(n) EMST counting-oracle question.

Run with sim/.venv/Scripts/python.exe
"""
import numpy as np
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "sim"))
from emst import emst_weight

rng = np.random.default_rng(12345)

print("="*78)
print("PART 1: islands+bulk variance barrier")
print("="*78)
# M = sqrt(n) islands at pairwise distance L = sqrt(n); plus dense bulk of n-M points.
# Verify (a) island contribution to Sum lambda_i c_i is Theta(n),
#        (b) point estimator X(p) value/probability, (c) variance ratio.
for n in (256, 1024, 4096, 16384):
    M = int(round(np.sqrt(n)))
    L = np.sqrt(n)
    # place islands on a line spaced L apart, far from a tight bulk
    # bulk: n-M points in a small box of side ~1 near origin region offset
    islands = np.column_stack([np.arange(M)*L + 10_000.0, np.zeros(M)])
    nb = n - M
    bulk = rng.random((nb, 2)) * 1.0  # unit box -> bulk MST ~ O(sqrt(nb))
    P = np.vstack([islands, bulk])
    w = emst_weight(P)
    # island-only contribution: the islands form a path of length (M-1)*L once
    # they connect; but in the CRT sum each island is its own component over the
    # band of scales [1, ~L]. Total persistence ~ sum over islands of (their NN dist).
    # Each island's NN distance is L (to next island) or distance-to-bulk (~10000) for the
    # nearest island -- here we want island NN ~ L, so islands contribute ~ M*L to MST?
    # Actually in MST the islands connect as a path: (M-1) edges of length L -> (M-1)*L.
    island_path = (M-1)*L
    print(f"n={n:6d} M={M:3d} L={L:7.1f}  MST={w:12.1f}  islandpath~(M-1)L={island_path:10.1f}"
          f"  ratio_island/n={island_path/n:.3f}")
