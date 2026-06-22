"""
Task 3 (ADVERSARIAL): is there an ALL-SPARSE filament defeating slabs too?

Want N = sqrt(n) singleton islands simultaneously:
 (i)  pairwise >= lambda           (isolated => persistence lambda each => Theta(n) total)
 (ii) NO scatter-blowup            (MST contribution Theta(n); consecutive ~lambda apart)
 (iii) sparse in 2-D area density  (Theta(1/sqrt n) lambda-box hit-rate)
 (iv) sparse in BOTH x-projection AND y-projection
      (every width-lambda vertical slab and every height-lambda horizontal slab has O(1) islands)

Candidate constructions:
  A. DIAGONAL          (islands on y=x, cell (k,k))
  B. HILBERT curve     (space-filling through N x N lambda-grid)
  C. RANDOM PERMUTATION-MATRIX  (a permutation pi: island k at cell (k, pi(k)); one per row & col)
     -- but permutation alone does NOT guarantee consecutive ~lambda apart (ii). We test ii.
  D. "double-resolution" diagonal scaled so x and y each span full Delta.

We test (i)-(iv) numerically with exact EMST and the range-counting oracle, and we
measure: for a CONNECTED-COST curve (consecutive ~lambda apart), MUST some axis slab be dense?
"""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "sim"))
import numpy as np
from emst import emst_weight
from scipy.spatial import cKDTree


# ---------------- constructions ----------------

def cell_center(gx, gy, lam):
    return (gx * lam + lam / 2.0, gy * lam + lam / 2.0)


def diagonal_cells(N):
    return [(k, k) for k in range(N)]


def hilbert_d2xy(order, d):
    """Convert Hilbert distance d to (x,y) on a 2^order x 2^order grid."""
    x = y = 0
    s = 1
    t = d
    while s < (1 << order):
        rx = 1 & (t // 2)
        ry = 1 & (t ^ rx)
        # rotate
        if ry == 0:
            if rx == 1:
                x = s - 1 - x
                y = s - 1 - y
            x, y = y, x
        x += s * rx
        y += s * ry
        t //= 4
        s *= 2
    return x, y


def hilbert_cells(N):
    """N cells along a Hilbert curve through a 2^order x 2^order grid (>= N x N)."""
    order = int(np.ceil(np.log2(max(N, 2))))
    side = 1 << order
    total = side * side
    # subsample the Hilbert curve to get N cells spread over the full grid,
    # keeping consecutive samples ~1 grid-cell? No -- to keep pairwise>=lambda we
    # take every (total/N)-th point; but that breaks consecutive-lambda. Instead we
    # want N cells that are a CONTIGUOUS Hilbert run scaled so each step ~ lambda.
    # Simpler faithful test: take the first N Hilbert cells of a sqrt(N) x sqrt(N) grid
    # (so the curve genuinely fills a 2D region, consecutive cells adjacent => lambda apart).
    sub_order = int(np.ceil(np.log2(max(int(np.ceil(np.sqrt(N))), 2))))
    cells = []
    for d in range(N):
        x, y = hilbert_d2xy(sub_order, d)
        cells.append((x, y))
    return cells


def permutation_cells(N, seed=0):
    """Permutation matrix: island k at (k, pi(k)). One per row & col -> both projections O(1)."""
    rng = np.random.default_rng(seed)
    pi = rng.permutation(N)
    return [(k, int(pi[k])) for k in range(N)]


def sorted_permutation_cells(N, seed=0):
    """
    A permutation whose points are then visited in nearest-neighbor / sorted order is
    irrelevant for the geometry; the SET is what matters. Same set as permutation_cells.
    """
    return permutation_cells(N, seed)


# ---------------- instance builder ----------------

def build_instance(cells, N, with_bulk=True, seed=0):
    lam = float(N)
    n = N * N
    islands = np.array([cell_center(gx, gy, lam) for (gx, gy) in cells], dtype=float)
    if not with_bulk:
        return islands, None, islands, lam, n
    m = n - len(cells)
    s = int(np.ceil(np.sqrt(m)))
    # place bulk far away, beyond the island bbox on +x
    X0 = islands[:, 0].max() + 10 * lam
    xs = np.arange(s)
    gx, gy = np.meshgrid(xs, xs)
    bulk = np.column_stack([gx.ravel() + X0, gy.ravel()]).astype(float)[:m]
    P = np.vstack([islands, bulk])
    return P, islands, bulk, lam, n


# ---------------- measurements ----------------

def pairwise_min(islands):
    tree = cKDTree(islands)
    d, _ = tree.query(islands, k=2)
    return d[:, 1].min(), d[:, 1].max()


def consecutive_dists(islands):
    """distance between island k and k+1 along the construction order (the 'curve')."""
    d = np.linalg.norm(np.diff(islands, axis=0), axis=1)
    return d.min(), d.max(), d.mean()


def island_mst_cost(islands):
    return emst_weight(islands)


def slab_max(islands, lam, axis):
    coord = islands[:, axis]
    lo, hi = coord.min(), coord.max()
    nslabs = int(np.ceil((hi - lo) / lam)) + 2
    counts = np.zeros(nslabs, dtype=int)
    for c in coord:
        counts[int((c - lo) // lam)] += 1
    return counts.max()


def box_hit_rate(P, islands, lam, n_probes=20000, seed=1):
    rng = np.random.default_rng(seed)
    tree = cKDTree(P)
    xmin, ymin = P.min(axis=0)
    xmax, ymax = P.max(axis=0)
    iset = set(map(tuple, islands.tolist()))
    hits = 0
    for _ in range(n_probes):
        cx = rng.uniform(xmin, xmax)
        cy = rng.uniform(ymin, ymax)
        idx = tree.query_ball_point([cx, cy], r=lam / 2, p=np.inf)
        if len(idx) == 1 and tuple(P[idx[0]].tolist()) in iset:
            hits += 1
    return hits / n_probes


def main():
    constructions = {
        "diagonal": diagonal_cells,
        "hilbert": hilbert_cells,
        "permutation": lambda N: permutation_cells(N, seed=0),
    }
    for name, fn in constructions.items():
        print(f"\n================ construction = {name} ================")
        print(f"{'N':>4} {'n':>7} {'lam':>5} | {'minPair/lam':>11} | "
              f"{'consecMax/lam':>13} {'consecMean/lam':>14} | "
              f"{'islMST':>9} {'islMST/n':>9} | {'xSlabMax':>8} {'ySlabMax':>8} | {'boxHit':>8} {'1/N':>7}")
        for N in [8, 16, 32, 64]:
            cells = fn(N)
            islands = np.array([cell_center(gx, gy, float(N)) for (gx, gy) in cells], dtype=float)
            lam = float(N)
            mn, mx = pairwise_min(islands)
            cmn, cmx, cmean = consecutive_dists(islands)
            imst = island_mst_cost(islands)
            n = N * N
            xs = slab_max(islands, lam, 0)
            ys = slab_max(islands, lam, 1)
            # build with bulk for hit-rate over full domain
            P, isl2, bulk, lam2, n2 = build_instance(cells, N, with_bulk=True)
            hit = box_hit_rate(P, islands, lam, n_probes=15000)
            print(f"{N:>4} {n:>7} {lam:>5.0f} | {mn/lam:>11.3f} | "
                  f"{cmx/lam:>13.3f} {cmean/lam:>14.3f} | "
                  f"{imst:>9.1f} {imst/n:>9.3f} | {xs:>8} {ys:>8} | {hit:>8.5f} {1.0/N:>7.4f}")

    print("\nKEY TEST (iv): xSlabMax and ySlabMax.")
    print("  If BOTH are O(1) -> construction is ALL-SPARSE in axis slabs (slab repair fails on it),")
    print("    PROVIDED (i) minPair/lam>=1, (ii) consecMax/lam=O(1) & islMST/n=O(1).")
    print("  If for every all-sparse construction (ii) FAILS (consecMax/lam grows or islMST/n grows),")
    print("    then connected-cost forces a dense slab -> slab repair WORKS.")


if __name__ == "__main__":
    main()
