"""
Task 1: Verify codex's FILAMENT instance numerically with exact EMST.

Construction (codex):
  n = N^2, Delta = Theta(n), lambda = N = sqrt(n).
  Place N singleton "islands" pairwise ~lambda apart ALONG A DIAGONAL/SNAKE
  through an N x N grid of lambda-cells.
  Add n - N points as a dense connected bulk (MST cost Theta(n)).

Verify:
 (a) each island is isolated until scale Theta(lambda) (nearest other point >= ~lambda),
     so persistence ~ lambda and filament contributes Sum ~ N*lambda = Theta(n).
 (b) consecutive islands ~lambda apart => NO scatter-blowup (total MST stays Theta(n)).
 (c) uniform 2D lambda-box probe hits an island's empty-lambda-neighborhood w.p. Theta(1/N).
"""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "sim"))
import numpy as np
from emst import emst_weight
from scipy.spatial import cKDTree


def build_filament(N, seed=0, bulk_side=None):
    """
    N islands on a diagonal/snake through an N x N grid of lambda-cells.
    lambda = N. Grid cell (gx,gy) center at (gx*lambda + lambda/2, gy*lambda + lambda/2).
    Snake path: row-by-row boustrophedon so consecutive islands are ~lambda apart.
    Bulk: dense connected block of n-N points placed in a far corner region,
    sized so its own MST cost is Theta(n) and it doesn't interfere with islands.
    """
    rng = np.random.default_rng(seed)
    lam = float(N)
    n = N * N

    # --- snake path of N islands through the N x N grid of lambda-cells ---
    # We take the main DIAGONAL is too short (only N cells but they'd be sqrt(2)*lambda apart,
    # still Theta(lambda) and pairwise >= lambda). But codex says "diagonal/snake".
    # Use a snake that visits N cells: first row left->right gives N cells exactly.
    # Simpler & faithful: put island k at cell (k, k) diagonal? That's N cells, pairwise
    # consecutive distance sqrt(2)*lambda. Endpoints far apart but path-cost = (N-1)*sqrt2*lam.
    # To be safe we use a snake along ONE ROW would only span N cells in x and 1 in y.
    # codex: "diagonal/snake through an N x N grid" -> use full boustrophedon of N points
    # but spread so x and y both vary. We'll do diagonal: cell (k,k).
    islands = []
    for k in range(N):
        cx = k * lam + lam / 2.0
        cy = k * lam + lam / 2.0
        islands.append((cx, cy))
    islands = np.array(islands, dtype=float)

    # --- bulk: dense connected block ---
    # Place a sqrt(n-N) x sqrt(n-N) unit-spacing block far from the islands' bbox.
    m = n - N
    s = int(np.ceil(np.sqrt(m)))
    # bulk occupies [X0, X0+s] x [0, s] with unit spacing -> connected, MST ~ m
    X0 = N * lam + 10 * lam  # far to the right of the islands
    xs = np.arange(s)
    gx, gy = np.meshgrid(xs, xs)
    bulk = np.column_stack([gx.ravel() + X0, gy.ravel()]).astype(float)[:m]

    P = np.vstack([islands, bulk])
    return P, islands, bulk, lam, n


def nearest_neighbor_dists(islands, P):
    """For each island, distance to nearest OTHER point in P."""
    tree = cKDTree(P)
    d, idx = tree.query(islands, k=2)  # k=2: self + nearest other
    return d[:, 1]


def lonely_box_hit_rate(P, islands, lam, n_probes=20000, seed=1):
    """
    Uniformly-random 2D lambda-box probe over the bounding box of ALL points.
    Probe = axis-aligned lambda x lambda box at random position.
    'Hits an island's empty-lambda-neighborhood' := box contains exactly that island
    and no other point (occupancy==1, the island).
    We measure: P(a random lambda-box contains exactly 1 point AND that point is an island).
    """
    rng = np.random.default_rng(seed)
    tree = cKDTree(P)
    xmin, ymin = P.min(axis=0)
    xmax, ymax = P.max(axis=0)
    island_set = set(map(tuple, islands.tolist()))
    hits = 0
    for _ in range(n_probes):
        x0 = rng.uniform(xmin - lam, xmax)
        y0 = rng.uniform(ymin - lam, ymax)
        # points in [x0,x0+lam] x [y0,y0+lam]
        idx = tree.query_ball_point([x0 + lam / 2, y0 + lam / 2], r=lam / 2, p=np.inf)
        if len(idx) == 1:
            pt = tuple(P[idx[0]].tolist())
            if pt in island_set:
                hits += 1
    return hits / n_probes


def main():
    print("=== Task 1: codex FILAMENT instance, exact EMST ===")
    print(f"{'N':>4} {'n':>7} {'lam':>6} {'w_MST':>12} {'w/n':>7} "
          f"{'minNNisl':>9} {'persist~Nlam':>12} {'persist/n':>9} {'hitrate':>10} {'1/N':>8}")
    for N in [8, 12, 16, 24, 32]:
        P, islands, bulk, lam, n = build_filament(N)
        w = emst_weight(P)
        nn = nearest_neighbor_dists(islands, P)
        min_nn = nn.min()
        # persistence of each island ~ its death scale ~ nearest-neighbor dist / something.
        # island persists as singleton until it can merge: death scale ~ min NN dist.
        persist = nn.sum()  # sum of death scales ~ sum of NN distances
        Nlam = N * lam
        hit = lonely_box_hit_rate(P, islands, lam, n_probes=20000)
        print(f"{N:>4} {n:>7} {lam:>6.1f} {w:>12.1f} {w/n:>7.2f} "
              f"{min_nn:>9.2f} {persist:>12.1f} {persist/n:>9.3f} {hit:>10.5f} {1.0/N:>8.4f}")

    print()
    print("Interpretation:")
    print(" (a) minNNisl >= ~lambda  => islands isolated until scale Theta(lambda).")
    print(" (b) w_MST/n = O(1) constant  => NO scatter blowup (would be n^{1/4} if blown up).")
    print(" (c) hitrate ~ 1/N = Theta(1/sqrt(n))  => uniform 2D box probe rarely hits an island.")


if __name__ == "__main__":
    main()
